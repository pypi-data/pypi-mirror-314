import threading
from concurrent import futures

# from redis import ConnectionPool, StrictRedis
from ws4redis.redis import getRedisClient, getPoolStatus
from objict import nobjict


from .models import redis, Task, TASK_STATE_STARTED
from .transports import email, http, sftp, sms, s3
from rest import helpers
from rest.log import getLogger
from rest import settings
import time


TQ_WORKERS = settings.get("TQ_WORKERS", 4)
TQ_SUBSCRIBE = settings.get("TQ_SUBSCRIBE", [])

logger = None

# use threads or processes
# because tasks are general heavy IO bound threads are probably more efficient
USE_THREADS = True

import multiprocessing
CPU_COUNT = multiprocessing.cpu_count()

if not USE_THREADS:
    # only use the number of cpus we have if using process
    TQ_WORKERS = min(TQ_WORKERS, CPU_COUNT)

class WorkManager(object):
    def __init__(self, worker_count=TQ_WORKERS, subscribe_to=TQ_SUBSCRIBE, **kwargs):
        self.worker_count = worker_count
        self.subscribe_to = subscribe_to
        self.logger = kwargs.get("logger", None)
        self.service = kwargs.get("service", None)
        self.client = None
        self.pubsub = None
        self._scheduled_tasks = {}
        self._running_count = 0
        self._pending_count = 0
        self.is_running = False
        self.host_channel = f"tq:host:{settings.HOSTNAME}"
        self.lock = threading.RLock()
        if not self.logger:
            self.logger = getLogger("root", filename="tq_worker.log")
        self.logger.info("starting manager, workers: {}".format(self.worker_count))
        self.logger.info("handling: {}".format(self.subscribe_to))
        if USE_THREADS:
            self._pool = futures.ThreadPoolExecutor(max_workers=self.worker_count)
        else:
            self._pool = futures.ProcessPoolExecutor(max_workers=self.worker_count)

    def updateCounts(self):
        self.logger.info("running: {} --- pending: {}".format(self._running_count, self._pending_count))

    def addTask(self, task):
        if task.is_stale:
            self.logger.warning("task({}) is now stale".format(task.id))
            task.failed("stale")
            return
        if task.id in self._scheduled_tasks:
            self.logger.error("task({}) is alrleady scheduled".format(task.id))
            return
        task.manager = self
        with self.lock:
            task.worker_running = False
            self._scheduled_tasks[task.id] = task
            self._pending_count += 1
            task.future = self._pool.submit(self.on_run_task, task)
        self.updateCounts()

    def addEvent(self, event):
        # self.logger.info("processing event", event)
        if event.type == "subscribe":
            # confirmation we subscribed
            self.logger.info("succesfully subscribed to: {}".format(event.channel))
            return

        self.logger.info(f"new_event@{event.channel}")

        if event.channel == "tq_restart":
            self.restart()
            return
        
        if event.data:
            event.data = nobjict.fromJSON(event.data)
        
        if event.channel == self.host_channel:
            self.on_host_event(event)
            return

        try:
            task = Task.FromEvent(event)
        except Exception:
            # this most likely means the db connection is broken!
            self.logger.exception("FromEvent")
            # recommend a restart
            self.logger.warning("db error? forcing a restart...")
            self.restart()
            return

        if not task:
            self.logger.warning("event has no task", event)
            return
        if event.channel == "tq_cancel":
            self.logger.info("cancel request received")
            try:
                self.cancelTask(task, event.data.reason)
            except Exception:
                self.logger.exception("during cancelTask")
            return
        self.addTask(task)

    def cancelTask(self, task, reason=None):
        cached_task = self._scheduled_tasks.get(task.id, None)
        if not cached_task:
            # task is not scheduled
            self.logger.warning("canceling non scheduled task({})".format(task.id))
            task.state = -2
            task.reason = reason
            task.save()
            return
        if not hasattr(cached_task, "future"):
            self.removeTask(cached_task)
            self.logger.error("task has no future!")
            return
        task = cached_task
        if task.future.running():
            # right now we don't support canceling a running task but we will try!
            self.logger.warning("attempting to stop running task({})".format(task.id))
            if self.killWorker(task._thread_id):
                time.sleep(2.0)
                if task.future.done():
                    self.logger.info("succesfully killed task({}@{})".format(task.id, task._thread_id))
                    task.state = -2
                    task.reason = reason
                    task.save()
                else:
                    self.logger.warning("failed to kill worker")
            else:
                self.logger.warning("failed to kill worker")
        else:
            if task.future.cancel():
                self.logger.info("succesfully canceled task({})".format(task.id))
                task.state = -2
                task.reason = reason
                task.save()
                self.removeTask(task)
                return
            else:
                self.logger.error("failed to cancel task({})".format(task.id))

    def killWorker(self, thread_id):
        import ctypes
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            return False
        return True

    def removeTask(self, task):
        try:
            with self.lock:
                del self._scheduled_tasks[task.id]
                self._pending_count -= 1
                self.updateCounts()
        except Exception:
            pass

    def processBacklog(self):
        tasks = Task.objects.filter(state__in=[0, 1, 2])
        for task in tasks:
            if task.channel in self.subscribe_to:
                if task.cancel_requested:
                    self.logger.info("task has cancel request {}".format(task.id))
                    task.state = -2
                    if not task.reason:
                        task.reason = "task canceled"
                    task.save()
                    continue
                self.logger.debug("resubmitting job {}".format(task.id))
                self.addTask(task)
            else:
                self.logger.warning("ignore job {}:{}".format(task.id, task.channel))

    def _on_webrequest(self, task):
        if http.REQUEST(task):
            task.completed()
        elif task.attempts < task.max_attempts:
            # -1 will auto calculate retry with back off
            # lets report the issue
            task.notifyError(reason=task.reason)
            task.retry_later(from_now_secs=-1)
        else:
            task.failed("max attempts")

    def _on_hookrequest(self, task):
        if task.model == "tq_email_request":
            resp = email.SEND(task)
        elif task.model == "tq_sms_request":
            resp = sms.SEND(task)
        elif task.model == "tq_sftp_request":
            resp = sftp.SEND(task)
        elif task.model == "tq_s3_request":
            resp = s3.UPLOAD(task)
        if resp:
            task.completed()
        elif task.attempts < task.max_attempts:
            task.retry_later(from_now_secs=-1)
        else:
            task.failed()

    def on_host_event(self, event):
        action = event.data.action
        if action == "ping":
            redis.publish(
                event.data.response_channel,
                dict(action="pong", hostname=settings.HOSTNAME))
        elif action == "restart":
            redis.publish(
                event.data.response_channel,
                dict(action="restarting", hostname=settings.HOSTNAME))
            self.restart() 
        elif action == "get_stats":
            data = nobjict(action="stats", hostname=settings.HOSTNAME)
            data.uptime = time.time() - self.started_at
            data.workers = self.worker_count
            data.subscribed = self.subscribe_to
            data.running = self._running_count
            data.pending = self._pending_count
            data.scheduled = len(self._scheduled_tasks.keys())
            data.pool = dict(**getPoolStatus())
            redis.publish(event.data.response_channel, data)

    def on_task_started(self, task):
        with self.lock:
            task.worker_running = True
            self._running_count += 1
            self._pending_count -= 1
            self.updateCounts()

    def on_task_ended(self, task):
        with self.lock:
            task.worker_running = False
            del self._scheduled_tasks[task.id]
            self._running_count -= 1
            self.updateCounts()

    def on_run_task(self, task):
        self.logger.info("running task({})".format(task.id))

        # check if its canceled
        try:
            self.on_task_started(task)
            task.refresh_from_db()
            task._thread_id = threading.current_thread().ident
            self.logger.debug("running on thread:{}".format(task._thread_id))
            if task.state not in [0, 1, 2, 10] or task.cancel_requested:
                self.logger.info("task({}) was canceled?".format(task.id))
                self.on_task_ended(task)
                return

            if task.is_stale:
                self.logger.warning("task({}) is now stale".format(task.id))
                task.failed("stale")
                self.on_task_ended(task)
                return
        except Exception as err:
            self.logger.exception(err)
            return

        handler = None
        if task.model == "tq_web_request":
            handler = self._on_webrequest
        elif task.model in ["tq_sftp_request", "tq_email_request", "tq_sms_request", "tq_s3_request"]:
            handler = self._on_hookrequest
        else:
            try:
                handler = task.getHandler()
            except Exception as err:
                self.logger.exception(err)
                task.log_exception(err)
                task.failed(str(err))
                self.on_task_ended(task)
                return

        if handler is None:
            self.logger.error("failed to find handler: task({})".format(task.id))
            task.failed("failed to find handler")
            self.on_task_ended(task)
            return

        # self.logger.debug("task.started()")
        task.started()
        try:
            # self.logger.debug("task({}) calling handler".format(task.id))
            handler(task)
            if task.state == TASK_STATE_STARTED:
                task.completed()
            # self.logger.debug("task({}) handler finished".format(task.id))
        except Exception as err:
            self.logger.exception(err, "task({}) had exception".format(task.id))
            task.log_exception(err)
            if "connection already closed" in str(err).lower():
                # this is a nasty little bug in django when forking django db connections
                # we will schedule the task to retry later
                task.retry_later()
                # let us try and close db connections?
                hack_closeDjangoDB()
                # or should we restart the task queue?
            else:
                task.failed(str(err))
        except SystemExit:
            self.logger.error("task({}) was killed".format(task.id))
        finally:
            self.on_task_ended(task)
        self.logger.info("task({}) finished with state {}".format(task.id, task.state))

    def run_forever(self):
        self.logger.info("starting work manager...")
        self.__open()
        self.logger.info("listening for incoming events...")
        while self.is_running:
            for event in self.pubsub.listen():
                if self.is_running:
                    # self.logger.debug("new event", event)
                    try:
                        event = nobjict.fromdict(event)
                        event.channel = helpers.toString(event.channel)
                        self.addEvent(event)
                    except Exception as err:
                        self.logger.exception(err)
        self.__close()

    def restart(self):
        if self.service:
            self.is_running = False
            self.stop(timeout=30.0)
            self.service.restart()

    def __open(self):
        if self.client is not None:
            return
        self.started_at = time.time()
        self.is_running = True
        self.client = getRedisClient()
        self.pubsub = self.client.pubsub()
        self.__subscribe()

    def __subscribe(self):
        if self.host_channel not in self.subscribe_to:
            self.subscribe_to.append(self.host_channel)
        for key in self.subscribe_to:
            self.logger.info("subscribing to: {}".format(key))
            self.pubsub.subscribe(key)
        self.pubsub.subscribe("tq_cancel")
        self.pubsub.subscribe("tq_restart")
        self.client.sadd("tq:host:online", settings.HOSTNAME)

    def __unsubscribe(self):
        self.client.srem("tq:host:online", settings.HOSTNAME)
        for key in self.subscribe_to:
            self.pubsub.unsubscribe(key)
        self.pubsub.unsubscribe("tq_cancel")
        self.pubsub.unsubscribe("tq_restart")

    def __close(self):
        if self.client is None:
            return

        self.__unsubscribe()
        self.client = None
        self.pubsub = None
        self.logger.info("closed")

    def stop(self, timeout=30.0):
        self.updateCounts()
        self.logger.info("stopping, canceling pending tasks...")
        self.is_running = False
        # we need to cancel all futures not running:
        try:
            redis.publish("tq_cancel", {"pk":1})
            with self.lock:
                self.updateCounts()
                for key, task in list(self._scheduled_tasks.items()):
                    if not hasattr(task, "future"):
                        continue
                    if not task.future.running():
                        task.future.cancel()
                self.updateCounts()
        except Exception as err:
            self.logger.exception(err)

        self.logger.info("waiting for {} running tasks, timeout: {}".format(self._running_count, timeout))
        time.sleep(1.0)
        self.__close()
        timeout_at = time.time() + timeout
        while self._running_count > 0 and time.time() < timeout_at:
            # we are waiting for all jobs to finish
            time.sleep(1.0)

        self.updateCounts()
        if self._running_count:
            self.logger.error("timedout waiting for long running tasks, stopping anyway")
            # lets set all to failed that are running
            for pk, task in list(self._scheduled_tasks.items()):
                if task.worker_running:
                    if task.current_runtime >= 300:
                        task.failed("killed because task is taking to long to run")
                    else:
                        task.retry_later("worker engine restarting")
        else:
            self.logger.info("all tasks complete and workers stopped!")


def hack_closeDjangoDB():
    from django.db import connections
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()


