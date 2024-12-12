# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-09-07 22:15
# @Author : 毛鹏
import platform

if platform.system() == 'Windows':
    from mangokit.mango import Mango
elif platform.system() == 'Linux':
    from mangokit.mango import Mango
else:
    raise ImportError("Unsupported operating system")

from mangokit.tools.base_request import *
from mangokit.tools.log_collector import set_log
from mangokit.tools.data_processor import *
from mangokit.tools.database import *
from mangokit.models.models import *
from mangokit.tools.decorator import *
from mangokit.tools.notice import *
from mangokit.enums.enums import *
from mangokit.exceptions import MangoKitError

__all__ = [
    'DataProcessor',
    'DataClean',
    'ObtainRandomData',
    'CacheTool',
    'CodingTool',
    'EncryptionTool',
    'JsonTool',
    'RandomCharacterInfoData',
    'RandomNumberData',
    'RandomStringData',
    'RandomTimeData',

    'MysqlConingModel',
    'ResponseModel',
    'EmailNoticeModel',
    'TestReportModel',
    'WeChatNoticeModel',

    'CacheValueTypeEnum',
    'NoticeEnum',

    'MysqlConnect',
    'SQLiteConnect',
    'requests',
    'async_requests',
    'set_log',
    'WeChatSend',
    'EmailSend',

    'singleton',
    'convert_args',

    'Mango',

    'MangoKitError',
]
