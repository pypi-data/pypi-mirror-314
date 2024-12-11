import json, os
import datetime
import uuid, requests
import calendar, time

from ryry import store 
from ryry import utils 
from ryry import taskUtils 
from ryry import constant 

def _aigc_post(func, params, files={}, timeout=10):
    s = requests.session()
    try:
        requests.adapters.DEFAULT_RETRIES = 2
        s.keep_alive = False
        s.headers.update({'Connection':'close'})
        s.headers.update({'Usertoken':"0cce7cfe3629e16ee9b3ea8563305d3a15c524804da1861db07c2c867d79da63"})
        if len(files) <= 0:
            s.headers.update({'Content-Type':'application/json'})
            res = s.post(url=f"https://api.dalipen.com/{func}", json=params, timeout=timeout, verify=False)
        else:
            res = s.post(url=f"https://api.dalipen.com/{func}", data=params, files=files, timeout=timeout, verify=False)
        if res.status_code == 200:
            result_data = json.loads(res.content)
            res.close()
            if result_data["code"] == 0:
                return 0, "", result_data["data"]
            else:
                return result_data["code"], result_data["msg"], ""
        else:
            raise Exception(f'''request {func} status_code={res.status_code}''')
    except Exception as e:
        return -1, str(e), ""
    finally:
        s.close()
    return -1, "", ""
    
#======================================== Task Function ==============================
def _extend():
    extInfo = store.readDeviceInfo()
    extInfo["app"] = constant.app_name + " " + constant.app_version
    extInfo["host"] = utils.get_hostname()
    return json.dumps(extInfo)

def GetTask():
    widget_map = []
    map = store.widgetMap()
    for it in map:
        if isinstance(map[it], (dict)):
            if map[it]["isBlock"] == False:
                widget_map.append(it)
        else:
            widget_map.append(it)
    req = {
        "widget_map": json.dumps(widget_map),
        "limit": 1,
        "extend": _extend()
    }
    r1, r2, r3 = _aigc_post("aigc/task/getTask", req)
    if r1 != 0:
        return []
    datas = []
    for it in r3:
        datas.append({
            "taskUUID": it["task_uuid"],
            "config": it["config"],
            "data": it["data"],
            "timeout": it["timeout"],
        })
    #Previous tasks may have failed due to network problems, so collect and resend
    retryLastTaskNotify()
    return datas

TASK_NOTIFY_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"task_notify_data.json")
def saveTaskNotifyData(taskUUID, status, msg, dataStr):
    taskUtils.taskPrint(taskUUID, f"save {taskUUID} to next notify")
    data = []
    try:
        if not os.path.exists(TASK_NOTIFY_DATA):
            with open(TASK_NOTIFY_DATA, 'w') as f:
                json.dump([], f)
        with open(TASK_NOTIFY_DATA, 'r') as f:
            data = json.load(f)
    except:
        pass
    try:
        data.append({
            "taskUUID":taskUUID,
            "status":status,
            "msg":msg,
            "dataStr":dataStr,
            "pts": calendar.timegm(time.gmtime())
        })
        with open(TASK_NOTIFY_DATA, 'w') as f:
            json.dump(data, f)
    except:
        pass
def resetLastTaskNotify(taskUUID):
    data = []
    try:
        if os.path.exists(TASK_NOTIFY_DATA):
            with open(TASK_NOTIFY_DATA, 'r') as f:
                data = json.load(f)
    except:
        pass
    try:
        newData = []
        for it in data:
            if it["taskUUID"] != taskUUID:
                newData.append(it)
        with open(TASK_NOTIFY_DATA, 'w') as f:
            json.dump(newData, f)
    except:
        pass
def retryLastTaskNotify():
    data = []
    try:
        if os.path.exists(TASK_NOTIFY_DATA):
            with open(TASK_NOTIFY_DATA, 'r') as f:
                data = json.load(f)
    except:
        pass
    try:
        newData = []
        for it in data:
            msg = it["msg"]
            fail_count = 0
            if "fail_count" in it:
                fail_count = it["fail_count"]
            else:
                it["fail_count"] = 0
            pts = 0
            if "pts" in it:
                pts = it["pts"]
            if abs(calendar.timegm(time.gmtime())-pts) < 10: #notify late after 10 sec
                newData.append(it)
                continue
            if fail_count < 10:
                if TaskNotify(it["taskUUID"], it["status"], f"{msg} *", it["dataStr"], False) == False:
                    it["fail_count"] += 1
                    newData.append(it)
        with open(TASK_NOTIFY_DATA, 'w') as f:
            json.dump(newData, f)
    except:
        pass
    
def TaskNotify(taskUUID, status, msg, dataStr, failSaveNotify=True):
    req = {
        "task_uuid": taskUUID,
        "status": status,
        "msg": msg,
        "dataStr": dataStr
    }
    r1, r2, r3 = _aigc_post("aigc/task/taskNotify", req)
    if r1 != 0:
        if failSaveNotify:
            #tasks may have failed due to network problems, so collect and resend
            saveTaskNotifyData(taskUUID, status, msg, dataStr)
        return False
    return r3
  
def TaskUpdateProgress(taskUUID, progress, dataStr):
    req = {
        "task_uuid": taskUUID,
        "progress": progress,
    }
    r1, r2, r3 = _aigc_post("aigc/task/taskProgress", req)
    if r1 != 0:
        return False
    return True

def TaskCancel(taskUUID):
    req = {
        "task_uuid": taskUUID,
    }
    r1, r2, r3 = _aigc_post("aigc/task/taskCancel", req)
    if r1 != 0:
        return False
    return True

def _upload(localFilePath, ext, keep_it_always=False):
    with open(localFilePath, "rb") as f:
        files = { 'file':f }
        params = { 'ext':ext }
        if keep_it_always:
            r1, r2, r3 = _aigc_post("upload/datanet", params, files=files,timeout=100)
        else:
            r1, r2, r3 = _aigc_post("upload/create", params, files=files,timeout=100)
    if r1 != 0:
        raise Exception(f"upload fail!, reason={r2}")
    return r3

def upload(localFilePath, ext, keep_it_always=False):
    try:
        return _upload(localFilePath, ext, keep_it_always)
    except:
        pass
    from mecord import upload as mecord_upload
    try:
        return mecord_upload.upload(localFilePath, None, "sg")
    except:
        pass
    try:
        return mecord_upload.upload(localFilePath, None, "test")
    except:
        pass
    try:
        import hashlib
        import hmac
        import base64
        timestamp = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")        
        content_type = "application/octet-stream"
        
        random_name = ''.join(str(uuid.uuid4()).split('-'))
        object_key = f"temp/{random_name}.{ext}"
        bucket = "p-template-hk"
        resource = f"/{bucket}/{object_key}"
        endpoint = "oss-cn-hongkong.aliyuncs.com"        
        string_to_sign = f"PUT\n\n{content_type}\n{timestamp}\n{resource}"    
        signature = base64.b64encode(
            hmac.new("sZDIL9uhqTgeQOkAjpbSOFm0259fwZ".encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha1).digest()
        ).decode('utf-8')        
        url = f"https://{bucket}.{endpoint}/{object_key}"
        headers = {
            "Date": timestamp,
            "Authorization": f"OSS LTAI5t6YZQo4MZV6LWwt4Rnj:{signature}",
            "Content-Type": content_type
        }
        with open(localFilePath, "rb") as file:
            file_data = file.read()
        response = requests.put(url, data=file_data, headers=headers)
        if response.status_code == 200:
            return url
    except:
        pass
    raise Exception("all upload target is fail!")

def uploadWidget(widget_id, name, whl, ext, version):
    with open(whl, "rb") as f:
        files = { 'file':f }
        params = {
            'widget_id':widget_id,
            'name':name,
            'version':version,
            'ext':ext
        }
        r1, r2, r3 = _aigc_post("aigc/task/publishWidget", params, files=files, timeout=300)
    if r1 != 0:
        raise Exception(f"upload widget fail!, reason={r2}")
    return r3

def CreateWidgetUUID():
    req = {}
    r1, r2, r3 = _aigc_post("aigc/task/createWidget", req)
    if r1 != 0:
        raise Exception(f"CreateWidgetUUID fail!, reason={r2}")
    return r3

#======================================== Task Function ==============================
def createTask(widget_name, params):
    req = {
        "widget_name": widget_name,
        "widget_data": json.dumps(params),
        "extend": _extend()
    }
    r1, r2, r3 = _aigc_post("aigc/task/createTask", req)
    if r1 != 0:
        raise Exception(f"create task fail!, reason={r2}")
    return r3

def findWidget(name):
    req = {
        "name": name
    }
    r1, r2, r3 = _aigc_post("aigc/task/findWidget", req)
    if r1 != 0:
        return "", "", ""
    for it in r3:
        widget_id = it["widget_id"]
        widget_name = it["name"]
        version = it["version"]
        package = it["package"]
        if widget_name.strip().lower() == name.strip().lower():
            return widget_id, version, package
    return "", "", ""

def getAutoDeployWidget():
    req = {}
    r1, r2, r3 = _aigc_post("aigc/task/getAutoDeployWidget", req)
    result = []
    if r1 != 0:
        return result
    for it in r3:
        widget_id = it["widget_id"]
        widget_name = it["name"]
        version = it["version"]
        package = it["package"]
        result.append([widget_id, widget_name, version, package])
    return result

def checkTask(checkUUID):
    req = {
        "task_uuid": checkUUID
    }
    r1, r2, r3 = _aigc_post("aigc/task/checkTask", req)
    if r1 != 0:
        return False, False, "server fail", 0
    if r3["status"] < 2:
        return False, False, "", r3["progress"]
    elif r3["status"] == 2:
        return True, True, json.loads(r3["task_result"]), r3["progress"]
    elif r3["status"] == 3:
        return True, False, r3["fail_reason"], r3["progress"]