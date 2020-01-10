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

from fixtures import *


def test_es_run(get_request):
    assert get_request.status_code == 200


def test_cat_nodes(get_cat_nodes):
    assert get_cat_nodes.status_code == 200


def test_create_index(create_index):
    assert create_index.status_code == 200


def test_create_mapping(create_index_mapping):
    assert create_index_mapping.json() == {'acknowledged': True}


def test_create_alarm(create_monitor):
    assert create_monitor.status_code == 201


def test_load_data(load_test_data):
    assert load_test_data.status_code == 201


def test_alert_trigger(search_triggered_alerts):
    assert search_triggered_alerts.status_code == 200
