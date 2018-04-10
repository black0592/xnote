# encoding=utf-8
# @author xupingmao 
# @modified 2018/04/10 00:12:21

'''
xnote系统配置
- 约定目录叫 XXX_DIR
- 文件叫 XXX_FILE
'''
import os
import time
from collections import OrderedDict

__version__ = "1.0"
__author__ = "xupingmao (578749341@qq.com)"
__copyright__ = "(C) 2016-2017 xupingmao. GNU GPL 3."
__contributors__ = []

##################################
# 系统配置项
##################################

# 开发者模式,会展示更多的选项和信息,会开启实验性功能
DEV_MODE = False
# 开启调试
DEBUG = False
# 调试盒子模型，针对某些不方便调试的浏览器
DEBUG_HTML_BOX = False
PORT = "1234"
SITE_HOME = None
minthreads = 10
# 打开浏览器
OPEN_IN_BROWSER = False
# 启用数据库的缓存搜索
USE_CACHE_SEARCH = False
# 文件系统使用urlencode方式,适用于只支持ASCII字符的系统
USE_URLENCODE = False
# 初始化脚本
INIT_SCRIPT = None
# 记录位置信息，可通过脚本配置打开
RECORD_LOCATION = False
# 菜单配置
MENU_LIST = []

# 处理器目录
HANDLERS_DIR = "handlers"
# 工具目录
TOOLS_DIR   = "handlers/tools"
WORKING_DIR = os.path.dirname(__file__)
WEBDIR      = os.path.join(WORKING_DIR, "static")
UPLOAD_DIR  = os.path.join(WORKING_DIR, "static", "upload")
PLUGINS_DIR = os.path.join(WORKING_DIR, "plugins")
LOG_DIR     = os.path.join(WORKING_DIR, "log")


# 用户数据的地址
DATA_PATH   = os.path.join(WORKING_DIR, "data")
DATA_DIR    = DATA_PATH
SCRIPTS_DIR = os.path.join(DATA_DIR, "scripts")
DB_DIR      = os.path.join(WORKING_DIR, "db")
CONFIG_DIR  = os.path.join(DATA_DIR, "config")

# 其他标记

# 测试用的flag,开启会拥有admin权限
IS_TEST  = False
# 开启性能分析
OPEN_PROFILE = False
PROFILE_PATH_SET = set(["/file/view"])
# 静音停止时间
MUTE_END_TIME = None
# 资料相关
# 分页数量
PAGE_SIZE = 30
IP_BLACK_LIST = ["192.168.56.1"] # this is vbox ip

# max file size to sync or backup
MAX_FILE_SIZE = 10 * 1024 ** 2


FS_HIDE_FILES = True
# 文件管理扩展的选项 Storage(name=, url=)
FS_OPT_BTNS = []
# 文本文件后缀
FS_TEXT_EXT_LIST = [
    ".java",  # Java
    ".scala",
    ".c",     # C语言
    ".h",
    ".cpp",   # C++
    ".hpp",
    ".vm",    # velocity
    ".vim",   # VIM文件
    ".html",  # HTML
    ".htm",
    ".js",    # JavaScript
    ".json",  
    ".css", 
    ".xml",   # XML
    ".xsd",   # XML schema
    ".csv",   # csv table
    ".proto", # proto buf
    ".py",    # Python
    ".txt",   # Text
    ".lua",   # Lua
    ".rb",    # Ruby
    ".go",    # Go
    ".m",     # Objective-C, Matlab
    ".conf",  # configuration
    ".sh",     # Linux shell
    ".bat",    # Windows shell
    ".cmd",    # Windows shell
    ".command", # Mac shell
    ".sql",     # sql
    ".ini",
    ".rc",
    ".properties",
    ".gradle",
    ".md"
]

# 通知公告
_notice_list = []
# 搜索历史
search_history = None
# 笔记访问历史
note_hisotry = None

# 配置项
_config = {}

def makedirs(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)


class Storage(dict):
    """
    A Storage object is like a dictionary except `obj.foo` can be used
    in addition to `obj['foo']`.
    
        >>> o = storage(a=1)
        >>> o.a
        1
        >>> o['a']
        1
        >>> o.a = 2
        >>> o['a']
        2
        >>> o.errKey
        None
    """
    def __init__(self, default_value=None, **kw):
        self.default_value = default_value
        super(Storage, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            return self.default_value
    
    def __setattr__(self, key, value): 
        self[key] = value
    
    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __deepcopy__(self, memo):
        return Storage(**self)
    
    def __repr__(self):     
        return '<MyStorage ' + dict.__repr__(self) + '>'


def init(path):
    """
    初始化系统配置项,启动时必须调用
    """
    global DATA_PATH
    global DATA_DIR
    global DB_PATH
    global DB_FILE
    global DICT_FILE
    global BACKUP_DIR
    global APP_DIR
    global TMP_DIR
    global SCRIPTS_DIR
    global CODE_ZIP
    global DATA_ZIP
    global TRASH_DIR
    global LOG_PATH
    global LOG_FILE

    DATA_PATH = path
    DATA_DIR  = path
    # 数据库地址
    DB_PATH      = os.path.join(DATA_PATH, "data.db")
    DICT_FILE    = os.path.join(DATA_DIR, "dictionary.db")
    # 备份数据地址
    BACKUP_DIR   = os.path.join(DATA_PATH, "backup")
    # APP地址
    APP_DIR      = os.path.join(DATA_PATH, "app")
    TMP_DIR      = os.path.join(DATA_PATH, "tmp")
    SCRIPTS_DIR  = os.path.join(DATA_DIR, "scripts")
    CODE_ZIP     = os.path.join(DATA_DIR, "code.zip")
    DATA_ZIP     = os.path.join(DATA_DIR, "data.zip")
    TRASH_DIR    = os.path.join(DATA_DIR, "trash")
    LOG_PATH     = os.path.join(DATA_DIR, "xnote.log")
    DB_FILE      = DB_PATH
    LOG_FILE     = LOG_PATH

    makedirs(DATA_DIR)
    makedirs(TMP_DIR)
    makedirs(SCRIPTS_DIR)
    makedirs(TRASH_DIR)


def get(name, default_value=None):
    """获取配置，如果不存在返回default值"""
    value = globals().get(name)
    if value is not None:
        return value
    value = _config.get(name)
    if value is not None:
        return value

    if value is None:
        return default_value
    return value

def set(name, value):
    _config[name] = value

def get_config():
    return _config
    
def has_config(key, subkey = None):
    group_value = get(key)
    if group_value is None:
        return False
    if subkey is None:
        return True
    return subkey in group_value
    
def has(key):
    return has_config(key)
        
class Properties(object): 
    """Properties 文件处理器"""
    def __init__(self, fileName, ordered = True): 
        self.ordered = ordered
        self.fileName = fileName
        self.properties = None
        self.properties_list = None
        self.load_properties()

    def new_dict(self):
        if self.ordered:
            return OrderedDict()
        else:
            return {}

    def _set_dict(self, strName, dict, value): 
        strName = strName.strip()
        value = value.strip()

        if strName == "":
            return

        if(strName.find('.')>0): 
            k = strName.split('.')[0] 
            dict.setdefault(k, self.new_dict()) 
            self._set_dict(strName[len(k)+1:], dict[k], value)
            return
        else: 
            dict[strName] = value 
            return 
    def load_properties(self): 
        self.properties = self.new_dict()
        self.properties_list = self.new_dict()
        with open(self.fileName, 'r', encoding="utf-8") as pro_file: 
            for line in pro_file.readlines(): 
                line = line.strip().replace('\n', '') 
                if line.find("#")!=-1: 
                    line=line[0:line.find('#')] 
                if line.find('=') > 0: 
                    strs = line.split('=') 
                    strs[1]= line[len(strs[0])+1:] 
                    self._set_dict(strs[0], self.properties,strs[1]) 
                    self.properties_list[strs[0].strip()] = strs[1].strip()
        return self.properties

    def get_properties(self):
        return self.properties

    def get_property(self, key, default_value=None):
        return self.properties_list.get(key, default_value)

    def reload(self):
        self.load_properties()

def is_mute():
    """是否静音"""
    return MUTE_END_TIME is not None and time.time() < MUTE_END_TIME

def add_notice(user=None,
        message=None, 
        link=None,
        year=None, 
        month=None, 
        day=None,
        wday=None):
    """
    添加通知事件, 条件为None默认永真，比如user为None，向所有用户推送
    """
    _notice_list.append(Storage(user=user, year=year, month=month, day=day, wday=wday, message=message, link=link))

def get_notice_list(type='today', user=None):
    """
    获取通知列表,user不为空时通过它过滤
    - today 今天的通知
    - all 所有的通知
    """
    tm = time.localtime()
    def today_filter(todo):
        year  = tm.tm_year
        month = tm.tm_mon
        day  = tm.tm_mday
        wday = tm.tm_wday + 1
        if todo.user != None and user != todo.user:
            return False
        if todo.year != None and todo.year != year:
            return False
        if todo.month != None and todo.month != month:
            return False
        if todo.day != None and todo.day != day:
            return False
        if todo.wday != None and todo.wday != wday:
            return False
        return True
    if type == 'today':
        return list(filter(today_filter, _notice_list))
    if type == "all":
        return _notice_list

def clear_notice_list():
    global _notice_list
    _notice_list = [] # Py2 do not have clear method

init(DATA_DIR)