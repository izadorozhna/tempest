# Copyright 2012 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import sys

from tempest_lib import exceptions as lib_exc
import testtools

from tempest.api.compute import base
from tempest.common.utils import data_utils
from tempest.common import waiters
from tempest import config
from tempest import test

CONF = config.CONF


class ServersNegativeTestJSON(base.BaseV2ComputeTest):

    credentials = ['primary', 'alt']

    def setUp(self):
        super(ServersNegativeTestJSON, self).setUp()
        try:
            waiters.wait_for_server_status(self.client, self.server_id,
                                           'ACTIVE')
        except Exception:
            self.__class__.server_id = self.rebuild_server(self.server_id)

    def tearDown(self):
        self.server_check_teardown()
        super(ServersNegativeTestJSON, self).tearDown()

    @classmethod
    def setup_clients(cls):
        super(ServersNegativeTestJSON, cls).setup_clients()
        cls.client = cls.servers_client
        cls.alt_client = cls.os_alt.servers_client

    @classmethod
    def resource_setup(cls):
        super(ServersNegativeTestJSON, cls).resource_setup()
        server = cls.create_test_server(wait_until='ACTIVE')
        cls.server_id = server['id']

    @test.attr(type=['negative'])
    @test.idempotent_id('7f70a4d1-608f-4794-9e56-cb182765972c')
    def test_invalid_access_ip_v4_address(self):
        # An access IPv4 address must match a valid address pattern

        IPv4 = '1.1.1.1.1.1'
        self.assertRaises(lib_exc.BadRequest,
                          self.create_test_server, accessIPv4=IPv4)

    @test.attr(type=['negative'])
    @test.idempotent_id('5226dd80-1e9c-4d8a-b5f9-b26ca4763fd0')
    def test_invalid_ip_v6_address(self):
        # An access IPv6 address must match a valid address pattern

        IPv6 = 'notvalid'

        self.assertRaises(lib_exc.BadRequest,
                          self.create_test_server, accessIPv6=IPv6)

    @test.attr(type=['negative'])
    @test.idempotent_id('4e72dc2d-44c5-4336-9667-f7972e95c402')
    def test_create_with_invalid_network_uuid(self):
        # Pass invalid network uuid while creating a server

        networks = [{'fixed_ip': '10.0.1.1', 'uuid': 'a-b-c-d-e-f-g-h-i-j'}]

        self.assertRaises(lib_exc.BadRequest,
                          self.create_test_server,
                          networks=networks)

    @test.attr(type=['negative'])
    @test.idempotent_id('c5fa6041-80cd-483b-aa6d-4e45f19d093c')
    def test_create_with_nonexistent_security_group(self):
        # Create a server with a nonexistent security group

        security_groups = [{'name': 'does_not_exist'}]
        self.assertRaises(lib_exc.BadRequest,
                          self.create_test_server,
                          security_groups=security_groups)
