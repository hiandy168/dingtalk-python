#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/11/28 下午3:16
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : test_ding.py
# @Software: PyCharm
import unittest
from extensions import cache
from datetime import datetime
from dingtalk import DingTalkApp
from config import current_config
from dateutil.relativedelta import relativedelta

__author__ = 'blackmatrix'


class DingTalkTestCase(unittest.TestCase):

    def setUp(self):
        self.app = DingTalkApp(name='vcan', cache=cache,
                               corp_id=current_config.DING_CORP_ID,
                               corp_secret=current_config.DING_CORP_SECRET)

    # 获取 access token
    def test_get_access_token(self):
        access_token = self.app.get_access_token()
        assert access_token is not None

    # 获取 jsapi ticket
    def test_get_jsapi_ticket(self):
        jsapi_ticket = self.app.get_jsapi_ticket()
        assert jsapi_ticket is not None

    # 获取系统标签
    def test_get_label_groups(self):
        label_groups = self.app.get_label_groups()
        assert label_groups
        label_groups = self.app.run('dingtalk.corp.ext.listlabelgroups', size=20, offset=0)
        assert label_groups
        return label_groups

    # 获取用户
    def test_get_user_list(self):
        dept_list = self.app.get_dempartment_list()
        dept_id = dept_list[0]['id']
        user_list = self.app.get_user_list(dept_id)
        return user_list

    # 获取部门
    def test_get_dempartment_list(self):
        dept_list = self.app.get_dempartment_list()
        return dept_list

    # 获取外部联系人
    def test_get_ext_list(self):
        ext_list = self.app.get_ext_list()
        assert ext_list is not None

    # 新增外部联系人
    def test_add_contact(self):
        # 获取标签
        label_groups = self.app.get_label_groups()
        label_ids = [v for label_group in label_groups for labels in label_group['labels'] for k, v in labels.items() if k == 'id']
        # 获取部门
        dept_list = self.app.get_dempartment_list()
        dept_ids = [dept['id'] for dept in dept_list]
        # 获取用户
        user_list = self.app.get_user_list(dept_ids[0])
        user_ids = [user['userid'] for user in user_list]
        contact = {'title': '开发工程师',
                   'share_deptids': dept_ids[1:3],
                   'label_ids': label_ids[0:3],
                   'remark': '备注内容',
                   'address': '地址内容',
                   'name': '张三',
                   'follower_userid': user_ids[0],
                   'state_code': '86',
                   'company_name': '企业名',
                   'share_userids': user_ids[0:2],
                   'mobile': '13058888888'}
        result = self.app.add_corp_ext(contact)
        assert result is not None

    # 测试新增工作流实例
    def test_bmps_create(self):
        args = {'process_code': 'PROC-FF6Y4BE1N2-B3OQZGC9RLR4SY1MTNLQ1-91IKFUAJ-4',
                'originator_user_id': '112322273839908294',
                'dept_id': '49381153',
                'approvers': ['112322273839908294'],
                'form_component_values': [{'value': '哈哈哈哈', 'name': '姓名'},
                                          {'value': '哈哈哈哈', 'name': '部门'},
                                          {'value': '哈哈哈哈', 'name': '加班事由'}]}
        resp = self.app.create_bpms_instance(**args)
        assert resp

    # 测试获取工作流实例列表
    def test_bpms_list(self):
        """

        刚刚发起流程时，返回情况
        **********************
        [
            {'title': '阿三的测试流程',
             'originator_dept_id': '49381153',
             'approver_userid_list': {'string': ['112322273839908294']},
             'status': 'RUNNING',
             'process_instance_id': 'a97b96c4-6e91-40a7-9e74-658224dd5c1a',
             'originator_userid': '112322273839908294',
             'create_time': '2017-12-06 10:28:19',
             'process_instance_result': '',
             'form_component_values':
                 {'form_component_value_vo':
                     [{'value': '哈哈哈哈', 'name': '姓名'},
                      {'value': '哈哈哈哈', 'name': '部门'},
                      {'value': '哈哈哈哈', 'name': '加班事由'}]
                 }
            }
        ]
        第一次审批同意时
        **********************
        [
            {'create_time': '2017-12-06 10:28:19',
             'originator_dept_id': '49381153',
             'process_instance_id': 'a97b96c4-6e91-40a7-9e74-658224dd5c1a',
             'approver_userid_list': {'string': ['112322273839908294']},
             'title': '阿三的测试流程',
             'status': 'RUNNING',
             'process_instance_result': 'agree',
             'form_component_values':
                 {'form_component_value_vo':
                     [{'value': '哈哈哈哈', 'name': '姓名'},
                      {'value': '哈哈哈哈', 'name': '部门'},
                      {'value': '哈哈哈哈', 'name': '加班事由'}]
                 },
             'originator_userid': '112322273839908294'}
        ]
        第二次审批同意时
        **********************
        [
            {'create_time': '2017-12-06 10:28:19',
             'approver_userid_list': {'string': ['112322273839908294']},
             'process_instance_result': 'agree',
             'form_component_values':
                {'form_component_value_vo':
                    [{'name': '姓名', 'value': '哈哈哈哈'},
                     {'name': '部门', 'value': '哈哈哈哈'},
                     {'name': '加班事由', 'value': '哈哈哈哈'}]},
             'process_instance_id': 'a97b96c4-6e91-40a7-9e74-658224dd5c1a',
             'originator_dept_id': '49381153',
             'title': '阿三的测试流程',
             'status': 'RUNNING',
             'originator_userid': '112322273839908294'}]}
        最后一次审批通过时
        **********************
        [
            {'create_time': '2017-12-06 10:28:19',
             'process_instance_result': 'agree',
             'status': 'COMPLETED',
             'process_instance_id': 'a97b96c4-6e91-40a7-9e74-658224dd5c1a',
             'title': '阿三的测试流程',
             'originator_userid': '112322273839908294',
             'originator_dept_id': '49381153',
             'approver_userid_list': {'string': ['112322273839908294']},
             'form_component_values':
                {'form_component_value_vo':
                    [{'name': '姓名', 'value': '哈哈哈哈'},
                     {'name': '部门', 'value': '哈哈哈哈'},
                     {'name': '加班事由', 'value': '哈哈哈哈'}]},
             'finish_time': '2017-12-06 10:41:54'
            }
        ]
        :return:
        """
        start_date = datetime.now() - relativedelta(month=1)
        data = self.app.get_bpms_instance_list(process_code='PROC-FF6Y4BE1N2-B3OQZGC9RLR4SY1MTNLQ1-91IKFUAJ-4',
                                               start_time=start_date)
        assert data

    # 测试钉钉实例绑定的方法
    def test_dingtalk_methods(self):
        methods = self.app.methods
        assert methods


if __name__ == '__main__':
    pass
