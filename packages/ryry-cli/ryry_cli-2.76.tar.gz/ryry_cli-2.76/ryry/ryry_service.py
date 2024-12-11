import sys, os, time, signal, subprocess, logging, json, platform, socket, calendar
from logging.handlers import RotatingFileHandler
from urllib.parse import *
from datetime import datetime, timedelta
from threading import Thread
from pkg_resources import get_distribution

from ryry import store
from ryry import ryry_webapi
from ryry import utils
from ryry import taskUtils
from ryry import ryry_widget
from ryry import ryry_server_socket as TaskConnector

thisFileDir = os.path.dirname(os.path.abspath(__file__)) 
pid_file = os.path.join(thisFileDir, "ryryService.pid")
stop_file = os.path.join(thisFileDir, "stop.now")
stop_thread_file = os.path.join(thisFileDir, "stop.thread")
all_thread_stoped = os.path.join(thisFileDir, "all_stoped.now")
def notify_other_stoped():
    with open(all_thread_stoped, 'w') as f:
        f.write("")

class LogStdout(object):
    def __init__(self):
        self.stdout = sys.stdout
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        logFilePath = f"{os.path.dirname(os.path.abspath(__file__))}/log.log"
        file_handler = RotatingFileHandler(logFilePath, maxBytes=1024*1024*20, backupCount=30)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(fmt='%(asctime)s - %(message)s', 
                                    datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def write(self, message):
        if message != '\n':
            self.logger.info(message)
        self.stdout.write(message)

    def flush(self):
        self.stdout.flush()

    def __del__(self):
        self.close()

    def close(self):
        sys.stdout = self.stdout

class ryryService:
    def __init__(self):
        self.THEADING_LIST = []

    def start(self, threadNum=1):
        if os.path.exists(pid_file):
            #check pre process is finish successed!
            with open(pid_file, 'r') as f:
                pre_pid = str(f.read())
            if len(pre_pid) > 0:
                if utils.process_is_zombie_but_cannot_kill(int(pre_pid)):
                    print(f'start service fail! pre process {pre_pid} is uninterruptible sleep')
                    taskUtils.notifyWechatRobot({
                        "msgtype": "text",
                        "text": {
                            "content": f"机器<{socket.gethostname()}>无法启动服务 进程<{pre_pid}>为 uninterruptible sleep"
                        }
                    })
                    return False
        #1: service init 
        sys.stdout = LogStdout()
        with open(pid_file, 'w') as f:
            f.write(str(os.getpid()))
        signal.signal(signal.SIGTERM, self.stop)
        store.save_multithread(threadNum)
        store.writeDeviceInfo(utils.deviceInfo())
        TaskConnector._clearTask()
        #2: service step
        executor = TaskConnector.RyryTaskExecutor()
        self.THEADING_LIST.append(executor)
        self.THEADING_LIST.append(TaskConnector.RyryShortConnectThread(executor))
        self.THEADING_LIST.append(ryryStateThread())
        self.THEADING_LIST.append(ryryPackageThread())
        #3: service step
        while (os.path.exists(stop_file) == False):
            time.sleep(10)
        print("prepare stop")
        with open(stop_thread_file, 'w') as f:
            f.write("")
        for t in self.THEADING_LIST:
            t.markStop()
        for t in self.THEADING_LIST:
            t.join()
        if pid_file and os.path.exists(pid_file):
            os.remove(pid_file)
        #4: clean
        if os.path.exists(stop_thread_file):
            os.remove(stop_thread_file)
        if os.path.exists(stop_file):
            os.remove(stop_file)
        taskUtils.offlineNotify()
        print("ryryService has ended!")
        utils.check_restart()
        sys.stdout.close()

    def is_running(self):
        if pid_file and os.path.exists(pid_file):
            with open(pid_file, 'r', encoding='UTF-8') as f:
                pid = int(f.read())
                try:
                    if utils.process_is_alive(pid):
                        return True
                    else:
                        return False
                except OSError:
                    return False
        else:
            return False
        
    def stop(self, signum=None, frame=None):
        with open(stop_file, 'w') as f:
            f.write("")
        print("ryryService waiting stop...")
        taskUtils.restartNotify("手动")
        while os.path.exists(stop_file):
            time.sleep(1)
        print("ryryService has ended!")
    
class ryryPackageThread(Thread):
    def __init__(self):
        super().__init__()
        self.name = f"ryryPackageThread"
        if platform.system() == 'Windows':
            self.time_task_file = os.path.join(thisFileDir, "update_ryry.bat")
        elif platform.system() == 'Linux' or platform.system() == 'Darwin':
            self.time_task_file = os.path.join(thisFileDir, "update_ryry.sh")
        if os.path.exists(self.time_task_file):
            os.remove(self.time_task_file)
        self.last_check_time = calendar.timegm(time.gmtime())
        self.start()
    def getCommandResult(self, cmd):
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            if result.returncode == 0:
                return result.stdout.decode(encoding="utf8", errors="ignore").replace("\n","").strip()
        except subprocess.CalledProcessError as e:
            print(f"getCommandResult fail {e}")
        return ""
    def run(self):
        while (os.path.exists(stop_thread_file) == False):
            time.sleep(10)
            if calendar.timegm(time.gmtime()) - self.last_check_time > 300:
                self.last_check_time = calendar.timegm(time.gmtime())
                try:
                    #update widget
                    ryry_widget.UpdateWidgetFromPypi()
                except Exception as ex:
                    print(f'update widget fail, {ex}')

                # if platform.system() != 'Darwin':
                #     try:
                #         #update cli
                #         remote_version = ryry_widget._remote_package_version("ryry-cli")
                #         simple = "https://pypi.python.org/simple/"
                #         local_version, local_path = ryry_widget._local_package_info("ryry-cli")
                #         if ryry_widget.compare_versions(remote_version, local_version) > 0:
                #             print("start update progress...")
                #             utils.begin_restart("auto upgrade ryry-cli", True, simple)
                #             device_id = utils.generate_unique_id()
                #             machine_name = socket.gethostname()
                #             ver = get_distribution("ryry-cli").version
                #             taskUtils.notifyWechatRobot({
                #                 "msgtype": "text",
                #                 "text": {
                #                     "content": f"机器<{machine_name}[{device_id}]>[{ver}] ryry-cli开始升级[{local_version}]->[{remote_version}]"
                #                 }
                #             })
                #             break
                #     except Exception as ex:
                #         print(f'update ryry-cli fail, {ex}')
            time.sleep(10)
        print(f"   PackageChecker stop")
        notify_other_stoped() #because other thread is waiting some signal to close
    def markStop(self):
        print(f"   PackageChecker waiting stop")

class ryryStateThread(Thread):
    def __init__(self):
        super().__init__()
        self.name = f"ryryStateThread"
        self.daemon = True
        self.tik_time = 30.0
        self.start()
    def run(self):
        taskUtils.onlineNotify()
        while (os.path.exists(stop_thread_file) == False):
            time.sleep(self.tik_time)
            try:
                task_config = TaskConnector._getTaskConfig()
                if task_config["last_task_pts"] > 0:
                    cnt = (calendar.timegm(time.gmtime()) - task_config["last_task_pts"]) #second
                    if cnt >= (60*60) and cnt/(60*60)%1 <= self.tik_time/3600:
                        taskUtils.idlingNotify(cnt)
                        #clear trush
                        for root,dirs,files in os.walk(thisFileDir):
                            for file in files:
                                if file.find(".") <= 0:
                                    continue
                                ext = file[file.rindex("."):]
                                if ext in [ ".in", ".out" ]:
                                    os.remove(os.path.join(thisFileDir, file))
                            if root != files:
                                break
            except:
                time.sleep(60)
        print(f"   StateChecker stop")
    def markStop(self):
        print(f"   StateChecker waiting stop")
        