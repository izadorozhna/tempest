# Copyright 2013 OpenStack Foundation
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

from tempest.api.network import base
from tempest_lib.common.utils import data_utils
from tempest import test
from tempest.test import attr


class LoadBalancerJSON(base.BaseNetworkTest):
    _interface = 'json'

    """
    Tests the following operations in the Neutron API using the REST client for
    Neutron:
        create vIP, and Pool
        show vIP
        list vIP
        update vIP
        delete vIP
        update pool
        delete pool
        show pool
        list pool
        health monitoring operations
    """

    @classmethod
    def setUpClass(cls):
        super(LoadBalancerJSON, cls).setUpClass()
        cls.network = cls.create_network()
        cls.name = cls.network['name']
        cls.subnet = cls.create_subnet(cls.network)
        pool_name = data_utils.rand_name('pool-')
        vip_name = data_utils.rand_name('vip-')
        cls.pool = cls.create_pool(pool_name, "ROUND_ROBIN",
                                   "HTTP", cls.subnet)
        cls.vip = cls.create_vip(vip_name, "HTTP", 80, cls.subnet, cls.pool)
        cls.member = cls.create_member(80, cls.pool)
        cls.health_monitor = cls.create_health_monitor(4, 3, "TCP", 1)

    @attr(type='smoke')
    @test.idempotent_id('daac3592-b129-4814-9cbb-5425b11d1a7c')
    def test_list_vips(self):
        # Verify the vIP exists in the list of all vIPs
        resp, body = self.client.list_vips()
        self.assertEqual('200', resp['status'])
        vips = body['vips']
        found = None
        for n in vips:
            if (n['id'] == self.vip['id']):
                found = n['id']
        msg = "vIPs list doesn't contain created vip"
        self.assertIsNotNone(found, msg)

    @test.idempotent_id('0974a490-6dba-4afb-9802-fbc19f53b02f')
    def test_create_update_delete_pool_vip(self):
        # Creates a vip
        name = data_utils.rand_name('vip-')
        resp, body = self.client.create_pool(data_utils.rand_name("pool-"),
                                             "ROUND_ROBIN", "HTTP",
                                             self.subnet['id'])
        pool = body['pool']
        resp, body = self.client.create_vip(name, "HTTP", 80,
                                            self.subnet['id'], pool['id'])
        self.assertEqual('201', resp['status'])
        vip = body['vip']
        vip_id = vip['id']
        # Verification of vip update
        new_name = "New_vip"
        resp, body = self.client.update_vip(vip_id, new_name)
        self.assertEqual('200', resp['status'])
        updated_vip = body['vip']
        self.assertEqual(updated_vip['name'], new_name)
        # Verification of vip delete
        resp, body = self.client.delete_vip(vip['id'])
        self.assertEqual('204', resp['status'])
        # Verification of pool update
        new_name = "New_pool"
        resp, body = self.client.update_pool(pool['id'], new_name)
        self.assertEqual('200', resp['status'])
        updated_pool = body['pool']
        self.assertEqual(updated_pool['name'], new_name)
        # Verification of pool delete
        resp, body = self.client.delete_pool(pool['id'])
        self.assertEqual('204', resp['status'])

    @attr(type='smoke')
    @test.idempotent_id('2ab933e8-2a00-4608-af1f-eafa34330b3a')
    def test_show_vip(self):
        # Verifies the details of a vip
        resp, body = self.client.show_vip(self.vip['id'])
        self.assertEqual('200', resp['status'])
        vip = body['vip']
        self.assertEqual(self.vip['id'], vip['id'])
        self.assertEqual(self.vip['name'], vip['name'])

    @attr(type='smoke')
    @test.idempotent_id('bf477221-e7e0-41a7-8510-20e3f157b95c')
    def test_show_pool(self):
        # Verifies the details of a pool
        resp, body = self.client.show_pool(self.pool['id'])
        self.assertEqual('200', resp['status'])
        pool = body['pool']
        self.assertEqual(self.pool['id'], pool['id'])
        self.assertEqual(self.pool['name'], pool['name'])

    @attr(type='smoke')
    @test.idempotent_id('18448348-78fb-4635-a8e9-f86206466415')
    def test_list_pools(self):
        # Verify the pool exists in the list of all pools
        resp, body = self.client.list_pools()
        self.assertEqual('200', resp['status'])
        pools = body['pools']
        self.assertIn(self.pool['id'], [p['id'] for p in pools])

    @attr(type='smoke')
    @test.idempotent_id('90a9482c-4d84-4a4d-9698-df004f965cbd')
    def test_list_members(self):
        # Verify the member exists in the list of all members
        resp, body = self.client.list_members()
        self.assertEqual('200', resp['status'])
        members = body['members']
        self.assertIn(self.member['id'], [m['id'] for m in members])

    @attr(type='smoke')
    @test.idempotent_id('f8fa7c9e-ddac-4056-8509-42e2c5fc0a05')
    def test_create_update_delete_member(self):
        # Creates a member
        resp, body = self.client.create_member("10.0.9.46", 80,
                                               self.pool['id'])
        self.assertEqual('201', resp['status'])
        member = body['member']
        # Verification of member update
        admin_state = [False, 'False']
        resp, body = self.client.update_member(admin_state[0], member['id'])
        self.assertEqual('200', resp['status'])
        updated_member = body['member']
        self.assertIn(updated_member['admin_state_up'], admin_state)
        # Verification of member delete
        resp, body = self.client.delete_member(member['id'])
        self.assertEqual('204', resp['status'])

    @attr(type='smoke')
    @test.idempotent_id('14442ab9-ca96-47cd-9bf3-1ff7a37a696a')
    def test_show_member(self):
        # Verifies the details of a member
        resp, body = self.client.show_member(self.member['id'])
        self.assertEqual('200', resp['status'])
        member = body['member']
        self.assertEqual(self.member['id'], member['id'])
        self.assertEqual(self.member['admin_state_up'],
                         member['admin_state_up'])

    @attr(type='smoke')
    @test.idempotent_id('10ead679-7c19-45b4-b70e-444b05bdfea4')
    def test_list_health_monitors(self):
        # Verify the health monitor exists in the list of all health monitors
        resp, body = self.client.list_health_monitors()
        self.assertEqual('200', resp['status'])
        health_monitors = body['health_monitors']
        self.assertIn(self.health_monitor['id'],
                      [h['id'] for h in health_monitors])

    @attr(type='smoke')
    @test.idempotent_id('b72dcbf0-bb80-46b9-ade3-4021c8a7f5bf')
    def test_create_update_delete_health_monitor(self):
        # Creates a health_monitor
        resp, body = self.client.create_health_monitor(4, 3, "TCP", 1)
        self.assertEqual('201', resp['status'])
        health_monitor = body['health_monitor']
        # Verification of health_monitor update
        admin_state = [False, 'False']
        resp, body = self.client.update_health_monitor(admin_state[0],
                                                       health_monitor['id'])
        self.assertEqual('200', resp['status'])
        updated_health_monitor = body['health_monitor']
        self.assertIn(updated_health_monitor['admin_state_up'], admin_state)
        # Verification of health_monitor delete
        resp, body = self.client.delete_health_monitor(health_monitor['id'])
        self.assertEqual('204', resp['status'])

    @attr(type='smoke')
    @test.idempotent_id('ddce4d5e-48c1-437e-8414-9e6020cb0864')
    def test_show_health_monitor(self):
        # Verifies the details of a health_monitor
        resp, body = self.client.show_health_monitor(self.health_monitor['id'])
        self.assertEqual('200', resp['status'])
        health_monitor = body['health_monitor']
        self.assertEqual(self.health_monitor['id'], health_monitor['id'])
        self.assertEqual(self.health_monitor['admin_state_up'],
                         health_monitor['admin_state_up'])

    @attr(type='smoke')
    @test.idempotent_id('5ba54a32-58a2-43db-bac0-7ee127fd69ef')
    def test_associate_disassociate_health_monitor_with_pool(self):
        # Verify that a health monitor can be associated with a pool
        resp, body = (self.client.associate_health_monitor_with_pool
                     (self.health_monitor['id'], self.pool['id']))
        self.assertEqual('201', resp['status'])
        # Verify that a health monitor can be disassociated from a pool
        resp, body = (self.client.disassociate_health_monitor_with_pool
                     (self.health_monitor['id'], self.pool['id']))
        self.assertEqual('204', resp['status'])
