import os, time, json
from urllib.parse import *
import threading
from datetime import datetime, timedelta
import calendar
from threading import Thread, current_thread, Lock
import uuid
import queue
import subprocess, platform

from ryry import store
from ryry import ryry_webapi
from ryry import task 
from ryry import constant 
from ryry import utils
from ryry import taskUtils

thisFileDir = os.path.dirname(os.path.abspath(__file__))

class RyryTaskExecutor(Thread):
    THEADING_LIST = []
    max_counter = 1
    cur_counter = 0
    is_running = False
    task_queue = None
    ttt = 0
    
    def appendTask(self, data, callback):
        self.cur_counter+=1
        self.task_queue.put([data, callback])
        try:
            taskUUID = data["taskUUID"]
            taskUtils.taskPrint(taskUUID, f"{current_thread().name} === addQueue task : {taskUUID}")
        except:
            pass
            
    def idlePower(self):
        return self.max_counter - self.cur_counter
    
    def isWorking(self):
        return self.cur_counter > 0
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = f"RyryTaskExecutor"
        self.task_queue = queue.Queue()
        self.max_counter = store.get_multithread()
        self.is_running = True
        self.THEADING_LIST = []
        self.start()

    def taskRunning(self):
        while self.is_running:
            try:
                data, callback = self.task_queue.get()
                if data is None: 
                    break
                try:
                    taskUUID = data["taskUUID"]
                    domain = ""
                    params_tmp = json.loads(data["data"])
                    if "domain" in params_tmp:
                        domain = params_tmp["domain"]
                    timeout = 600
                    if "timeout" in data:
                        timeout = data["timeout"]
                    taskUtils.taskPrint(taskUUID, f"{current_thread().name} === receive task : {taskUUID}")
                    _appendTask(taskUUID, domain)
                    is_ok, msg, result = task.runTask(data, timeout)
                    if is_ok == False:
                        taskUtils.notifyTaskFail(taskUUID, msg)
                    self.cur_counter-=1
                    callback(taskUUID, is_ok, msg, result)
                    _removeTask(taskUUID)
                except Exception as e:
                    taskUtils.taskPrint(taskUUID, f"{current_thread().name} === task exception : {e}")
                    taskUtils.notifyScriptError(taskUUID)
                finally:
                    taskUtils.taskPrint(taskUUID, None)
                self.task_queue.task_done()
            except Exception as ex:
                taskUtils.taskPrint(None, f"{current_thread().name} === exception : {ex}")
                pass
        print(f"   {current_thread().name} taskRunning stop")

    def run(self):
        for idx in range(0, self.max_counter):
            self.THEADING_LIST.append(Thread(name=f"exector-{idx}",target=self.taskRunning))
        for t in self.THEADING_LIST:
            t.start()
        while self.is_running:
            time.sleep(5)
        for t in self.THEADING_LIST:
            t.join()
        print(f"   {self.name} stop!")

    def markStop(self):
        self.is_running = False
        print(f"   {self.name} waiting stop")
        for _ in range(self.max_counter*2):
            self.task_queue.put([None, None])
        print(f"   {self.name} stop")

lock = Lock()
task_config_file = os.path.join(thisFileDir, f"task_config.txt")
def _readTaskConfig():
    if os.path.exists(task_config_file) == False:
        with open(task_config_file, 'w') as f:
            json.dump({
                "last_task_pts": 0
            }, f)
    with open(task_config_file, 'r') as f:
        data = json.load(f)
    return data
def _saveTaskConfig(data):
    with open(task_config_file, 'w') as f:
        json.dump(data, f)
def _appendTask(taskUUID, subDomain):
    lock.acquire()
    task_config = _readTaskConfig()
    task_config[taskUUID] = {
        "pts": calendar.timegm(time.gmtime()),
        "domain": subDomain
    }
    task_config["last_task_pts"] = task_config[taskUUID]["pts"]
    _saveTaskConfig(task_config)
    lock.release() 
def _clearTask():
    lock.acquire()
    task_config = {
        "last_task_pts": 0
    }
    _saveTaskConfig(task_config)
    lock.release() 
def _removeTask(taskUUID):
    lock.acquire()
    task_config = _readTaskConfig()
    if taskUUID in task_config:
        del task_config[taskUUID]
    _saveTaskConfig(task_config)
    lock.release() 
def _taskCreateTime(taskUUID):
    pts = 0
    lock.acquire()
    task_config = _readTaskConfig()
    if taskUUID in task_config:
        pts = task_config[taskUUID]["pts"]
    lock.release()
    return pts 
def _getTaskConfig():
    lock.acquire()
    task_config = _readTaskConfig()
    lock.release() 
    return task_config

class RyryShortConnectThread(Thread):
    is_running = False
    executor: RyryTaskExecutor = None

    def __init__(self, executor):
        super().__init__()
        self.name = f"RyryShortConnectThread"
        self.is_running = True
        self.executor = executor
        self.start()
    
    def taskCallback(self, taskUUID, is_ok, msg, result):
        ryry_webapi.TaskNotify(taskUUID, is_ok, msg, result)

    def run(self):
        print(f"   {self.name} start")
        min_wait_time = 2
        max_wait_time = 30
        wait_time = min_wait_time
        consecutive_step = 2
        consecutive_failures = 0
        max_consecutive_failures = 10
        
        while (self.is_running):
            try:
                if self.executor.idlePower() == 0:
                    time.sleep(1)
                    continue
                datas = ryry_webapi.GetTask()
                for it in datas:
                    self.executor.appendTask(it, self.taskCallback)
                    
                # if task empty -> full, set wait_time = max -> min
                if len(datas) > 0:
                    consecutive_failures = 0
                    wait_time = max(min_wait_time, wait_time - consecutive_step)
                else:
                    consecutive_failures += 1
                    if consecutive_failures >= max_consecutive_failures:
                        wait_time = min(max_wait_time, wait_time + consecutive_step)
                        consecutive_failures = 0
            except Exception as ex:
                taskUtils.taskPrint(None, f"{self.name} === exception : {ex}")
            time.sleep(wait_time)
            
        print(f"   {self.name} stop")

    def markStop(self):
        print(f"   {self.name} waiting stop")
        self.is_running = False