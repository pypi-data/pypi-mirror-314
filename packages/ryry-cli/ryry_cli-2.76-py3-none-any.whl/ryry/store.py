import os
import json

def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner

@singleton
class Store(object):

    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"data.json")
        
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                json.dump({}, f)
                
    def read(self):
        with open(self.path, 'r') as f:
            data = json.load(f)
            
        return data
    
    def write(self, data):
        with open(self.path, 'w') as f:
            json.dump(data, f)
    
#============================== widget ================================
def isCreateWidget():
    sp = Store()
    read_data = sp.read()
    if "isCreateWidget" in read_data:
        return read_data["isCreateWidget"]
    else:
        return False
    
def finishCreateWidget():
    sp = Store()
    read_data = sp.read()
    read_data["isCreateWidget"] = False
    sp.write(read_data)

def widgetMap():
    sp = Store()
    read_data = sp.read()
    if "widgets" in read_data:
        return read_data["widgets"]
    else:
        return {}
    
def insertWidget(widget_id, name, path):
    sp = Store()
    read_data = sp.read()
    if "widgets" not in read_data:
        read_data["widgets"] = {}
    widgetsMap = read_data["widgets"]
    if widget_id in widgetsMap:
        widgetsMap[widget_id]["path"] = path
    else:
        widgetsMap[widget_id] = {
            "isBlock": False,
            "path" : path,
            "name" : name
        }
    for k in list(widgetsMap.keys()):
        if isinstance(widgetsMap[k], (dict)):
            if os.path.exists(widgetsMap[k]["path"]) == False:
                del widgetsMap[k]
        else:
            if os.path.exists(widgetsMap[k]) == False:
                del widgetsMap[k]
    sp.write(read_data)

def removeWidget(widget_id):
    sp = Store()
    read_data = sp.read()
    if "widgets" not in read_data:
        read_data["widgets"] = {}
    widgetsMap = read_data["widgets"]
    if widget_id in widgetsMap:
        del widgetsMap[widget_id]
    sp.write(read_data)
    
def disableWidget(widget_id):
    sp = Store()
    read_data = sp.read()
    if "widgets" not in read_data:
        read_data["widgets"] = {}
    widgetsMap = read_data["widgets"]
    if widget_id in widgetsMap:
        if isinstance(widgetsMap[widget_id], (dict)):
            widgetsMap[widget_id]["isBlock"] = True
        else:
            path = widgetsMap[widget_id]
            widgetsMap[widget_id] = {
                "isBlock": True,
                "path" : path
            }
    sp.write(read_data)

def enableWidget(widget_id):
    sp = Store()
    read_data = sp.read()
    if "widgets" not in read_data:
        read_data["widgets"] = {}
    widgetsMap = read_data["widgets"]
    if widget_id in widgetsMap:
        if isinstance(widgetsMap[widget_id], (dict)):
            widgetsMap[widget_id]["isBlock"] = False
        else:
            path = widgetsMap[widget_id]
            widgetsMap[widget_id] = {
                "isBlock": False,
                "path" : path
            }
    sp.write(read_data)
    
#============================== device id ================================

def writeDeviceInfo(data):
    sp = Store()
    read_data = sp.read()
    read_data["deviceInfo"] = data
    sp.write(read_data)
    
cache_device_info = None
def readDeviceInfo():
    global cache_device_info
    if cache_device_info == None:
        sp = Store()
        read_data = sp.read()
        if "deviceInfo" in read_data:
            cache_device_info = read_data["deviceInfo"]
        else:
            cache_device_info = {}
    return cache_device_info

def is_multithread():
    return get_multithread() > 1

def get_multithread():
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "multi_thread.config")
    try:
        with open(env_file, 'r', encoding='UTF-8') as f:
            n = int(f.read())
            return n
    except:
        return 1
    
def save_multithread(n):
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "multi_thread.config")
    try:
        with open(file, 'w') as f:
            f.write(str(n))
    except:
        pass