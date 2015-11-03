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

from tempest.api.compute import base
from tempest.common.utils import data_utils
from tempest.common import waiters
from tempest import test


class ServersTestJSON(base.BaseV2ComputeTest):

    @classmethod
    def setup_clients(cls):
        super(ServersTestJSON, cls).setup_clients()
        cls.client = cls.servers_client

    def tearDown(self):
        self.clear_servers()
        super(ServersTestJSON, self).tearDown()

    @test.idempotent_id('89b90870-bc13-4b73-96af-f9d4f2b70077')
    def test_update_access_server_address(self):
        # The server's access addresses should reflect the provided values
        server = self.create_test_server(wait_until='ACTIVE')

        # Update the IPv4 and IPv6 access addresses
        self.client.update_server(server['id'],
                                  accessIPv4='1.1.1.1',
                                  accessIPv6='::babe:202:202')
        waiters.wait_for_server_status(self.client, server['id'], 'ACTIVE')

        # Verify the access addresses have been updated
        server = self.client.show_server(server['id'])['server']
        self.assertEqual('1.1.1.1', server['accessIPv4'])
        self.assertEqual('::babe:202:202', server['accessIPv6'])

    @test.idempotent_id('38fb1d02-c3c5-41de-91d3-9bc2025a75eb')
    def test_create_server_with_ipv6_addr_only(self):
        # Create a server without an IPv4 address(only IPv6 address).
        server = self.create_test_server(accessIPv6='2001:2001::3')
        waiters.wait_for_server_status(self.client, server['id'], 'ACTIVE')
        server = self.client.show_server(server['id'])['server']
        self.assertEqual('2001:2001::3', server['accessIPv6'])
