# Copyright 2013 IBM Corp.
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

from tempest_lib import decorators

from tempest.api.compute import base
from tempest.common import fixed_network
from tempest.common.utils import data_utils
from tempest.common import waiters
from tempest import test


class ServersAdminTestJSON(base.BaseV2ComputeAdminTest):

    """
    Tests Servers API using admin privileges
    """

    _host_key = 'OS-EXT-SRV-ATTR:host'

    @classmethod
    def setup_clients(cls):
        super(ServersAdminTestJSON, cls).setup_clients()
        cls.client = cls.os_adm.servers_client
        cls.non_admin_client = cls.servers_client
        cls.flavors_client = cls.os_adm.flavors_client

    @classmethod
    def resource_setup(cls):
        super(ServersAdminTestJSON, cls).resource_setup()

        cls.s1_name = data_utils.rand_name('server')
        server = cls.create_test_server(name=cls.s1_name,
                                        wait_until='ACTIVE')
        cls.s1_id = server['id']

        cls.s2_name = data_utils.rand_name('server')
        server = cls.create_test_server(name=cls.s2_name,
                                        wait_until='ACTIVE')
        cls.s2_id = server['id']

    @test.idempotent_id('7a1323b4-a6a2-497a-96cb-76c07b945c71')
    def test_reset_network_inject_network_info(self):
        # Reset Network of a Server
        server = self.create_test_server(wait_until='ACTIVE')
        self.client.reset_network(server['id'])
        # Inject the Network Info into Server
        self.client.inject_network_info(server['id'])
