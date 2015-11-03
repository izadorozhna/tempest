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

import testtools

from tempest.api.compute import base
from tempest.common import waiters
from tempest import config
from tempest import test

CONF = config.CONF


class DeleteServersTestJSON(base.BaseV2ComputeTest):

    # NOTE: Server creations of each test class should be under 10
    # for preventing "Quota exceeded for instances"

    @classmethod
    def setup_clients(cls):
        super(DeleteServersTestJSON, cls).setup_clients()
        cls.client = cls.servers_client

    @test.idempotent_id('925fdfb4-5b13-47ea-ac8a-c36ae6fddb05')
    def test_delete_active_server(self):
        # Delete a server while it's VM state is Active
        server = self.create_test_server(wait_until='ACTIVE')
        self.client.delete_server(server['id'])
        waiters.wait_for_server_termination(self.client, server['id'])
