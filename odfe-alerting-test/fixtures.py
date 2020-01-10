# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

# Description:
# This is a test fixture, which provides a fixed baseline upon which tests can reliably and repeatedly execute
# In particular, this file provides a Elasticsearch object with all things configured
# so that tests can use this to communicate with Elasticsearch.

from pytest import fixture
import requests
import string
from test_data import *
import json
import random
import re

es_url = 'https://localhost:9200/'
alert_url = 'https://localhost:9200/_opendistro/_alerting/monitors'
index_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
print(index_name)


@fixture()
def get_request():
    r = create_get_request_obj(node_url=es_url)
    return r


@fixture()
def get_cat_nodes():
    node_url = es_url + '_cat/nodes?v'
    r = create_get_request_obj(node_url=node_url)
    return r


@fixture()
def create_index():
    node_url = es_url + index_name
    r = requests.put(url=node_url, auth=('admin', 'admin'), verify=False, timeout=3)
    return r


@fixture()
def create_index_mapping():
    node_url = es_url + index_name + '/' + '_mappings'
    r = requests.put(url=node_url, auth=('admin', 'admin'), verify=False, headers=req_headers,
                     data=json.dumps(index_payload), timeout=3)
    return r


@fixture()
def load_test_data():
    node_url = es_url + index_name + '/' + '_doc/'
    r = requests.post(url=node_url, params=params, auth=('admin', 'admin'), verify=False, headers=req_headers,
                      data=json.dumps(test_data), timeout=3)
    return r


@fixture()
def create_monitor():
    alarm_data_v2 = json.dumps(alarm_data)
    alarm_data_v3 = re.sub(r'test_index', index_name, alarm_data_v2)
    r = requests.post(url=alert_url, auth=('admin', 'admin'), verify=False, headers=req_headers, data=alarm_data_v3,
                      timeout=3)
    return r

'''
@fixture()
def get_monitor_id():
    srch_url = es_url + "_opendistro/_alerting/monitors/_search"
    srch_mon = requests.get(url=srch_url, auth=('admin', 'admin'), verify=False, timeout=3, headers=req_headers,
                            data=json.dumps(srch_payload))
    monitors = srch_mon.json()
    tot_hits = monitors['hits']['hits']
    if tot_hits > 0:
        monitor_id = tot_hits[0]['_id']
    else:
        monitor_id = None
'''


@fixture()
def search_triggered_alerts():
    trg_url = es_url + ".opendistro-alerting-alerts/_search?pretty"
    r = requests.get(url=trg_url, auth=('admin', 'admin'), verify=False, timeout=3, headers=req_headers,
                     data=json.dumps(trg_data))
    return r


def create_get_request_obj(node_url, params=None, headers=None):
    req = requests.get(url=node_url, auth=('admin', 'admin'), verify=False, timeout=3, params=params, headers=headers)
    return req
