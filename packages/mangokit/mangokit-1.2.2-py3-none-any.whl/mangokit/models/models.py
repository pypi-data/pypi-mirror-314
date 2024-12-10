# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2023-11-08 15:48
# @Author : 毛鹏

from pydantic import BaseModel


class ResponseModel(BaseModel):
    response_time: float
    headers: dict
    status_code: int
    text: str
    json_data: dict | str | None


class MysqlConingModel(BaseModel):
    host: str
    port: int
    user: str
    password: str
    database: str | None = None


class EmailNoticeModel(BaseModel):
    send_user: str
    email_host: str
    stamp_key: str
    send_list: list


class TestReportModel(BaseModel):
    test_suite_id: int | None = None
    project_id: int
    project_name: str
    test_environment: str
    case_sum: int
    success: int
    success_rate: float
    warning: int
    fail: int
    execution_duration: int | float
    test_time: str


class WeChatNoticeModel(BaseModel):
    webhook: str
