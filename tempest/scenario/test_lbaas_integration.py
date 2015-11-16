# Copyright 2013 OpenStack Foundation
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
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

import time

from tempest.api.network import base
from tempest.common.utils import data_utils
from tempest import config
from tempest import test

CONF = config.cfg.CONF


class LbaasHttpsTestJSON(base.BaseNetworkTest):
    _interface = 'json'

    """
    Tests the SSL termination for OpenContrail neutron-lbaas plugin.
    Scenario:
    1. Create network
    2. Create security group allowing TCP traffic
    3. Create VM with HTTP service enabled.
    4. Create LB pool.
    5. Add VM as a member to this pool.
    6. Create LB VIP in a public network, serving on port 443.
    7. Create a TCP health monitor.
    8. Connect to a LB VIP by SSH.
    """

    test_data = {}

    @classmethod
    def setUpClass(cls):
        super(LbaasHttpsTestJSON, cls).setUpClass()
        if not test.is_extension_enabled('lbaas', 'network'):
            msg = "lbaas extension not enabled."
            raise cls.skipException(msg)
        _, cls.vip_net = cls.client.show_network(CONF.network.public_network_id)
        cls.vip_subnet = cls.vip_net['network']['subnets'][0]
        cls.network = cls.create_network()
        cls.test_data['net_name'] = cls.network['name']
        cls.test_data['net_id'] = cls.network['id']
        cls.subnet = cls.create_subnet(cls.network, None, None, None)

        cls.os = cls.get_client_manager()
        cls.compute = cls.os.servers_client

        cls.secgroups = cls.os.security_groups_client
        resp, secgroup = cls.secgroups.create_security_group(data_utils.rand_name('lbaas-sg'))
        cls.test_data['secgroup_id'] = secgroup['id']
        cls.test_data['secgroup_name'] = secgroup['name']
        cls.secgroups.create_security_group_rule(cls.test_data['secgroup_id'],
                                                 'icmp', -1, -1)
        cls.secgroups.create_security_group_rule(cls.test_data['secgroup_id'],
                                                 'tcp', 22, 444)


    def setup_lb_infra(self, proto, n_servers, n_vips, n_pools=1, port=22, **params):
        self.__class__.test_data['servers'] = []
        self.__class__.test_data['members'] = []
        self.__class__.test_data['vips'] = []
        self.__class__.test_data['pools'] = []
        self.ips = []
        for i in range(n_pools):
            print 'Creating pool %s'%i
            for j in range(n_servers):
                _, server = self.compute.create_server(data_utils.rand_name('lbaas-server'),
                                                       CONF.network.image_with_httpd,
                                                       CONF.compute.flavor_ref,
                                                       networks=[{"uuid": self.network['id']}],
                                                       security_groups=[{'name': self.test_data['secgroup_name']}])
                self.compute.wait_for_server_status(server['id'], 'ACTIVE', 300)
                _, server = self.compute.get_server(server['id'])
                self.server = server
                ipaddr = server['addresses'].values()[0][0]['addr']
                self.__class__.test_data['servers'].append(self.server['id'])
                self.ips.append(ipaddr)


            pool_name = data_utils.rand_name('test-pool-')
            self.__class__.pool = self.create_pool(pool_name, "ROUND_ROBIN", proto, self.subnet)
            self.__class__.test_data['pools'].append(self.__class__.pool['id'])

            for vip in range(n_vips):
                vip_name = data_utils.rand_name('vip-')
                self.__class__.test_data['vip_name'] = vip_name
                try:
                    self.__class__.vip = self.__class__.create_vip(name=vip_name, protocol=proto, protocol_port=port,
                                         subnet={"id": self.__class__.vip_subnet}, pool=self.__class__.pool)
                except Exception, e:
                    print 'Cant create VIP.'
                    raise RuntimeError(i)
                self.__class__.test_data['vips'].append(self.__class__.vip['id'])

            for ip in self.ips:
                self.__class__.member = self.__class__.create_member(80, self.__class__.pool, ip)
                self.__class__.test_data['members'].append(self.__class__.member['id'])

    def tearDown(self):
        for server in self.__class__.test_data['servers']:
            try:
                self.compute.delete_server(server)
            except:
                print 'Cant delete server %s'%server
        self.__class__.test_data['servers'] = []

        for vip in self.__class__.vips:
            try:
                self.client.delete_vip(vip['id'])
            except:
                print 'Cant delete VIP %s'%vip['id']

        for member in self.__class__.members:
            try:
                self.client.delete_member(member['id'])
            except:
                print 'Cant delete member %s'%member['id']

        for healthmon in self.__class__.health_monitors:
            try:
                self.client.delete_health_monitor(healthmon[id])
            except:
                print 'Cant delete health monitor %s'%healthmon['id']

        for pool in self.__class__.pools:
            try:
                self.client.delete_pool(pool['id'])
            except:
                print 'Cant delete pool %s'%pool['id']

        self.__class__vips = []
        self.__class__.members = []
        self.__class__.health_monitors = []
        self.__class__.pools = []
        super(LbaasHttpsTestJSON, self).tearDown()


    @classmethod
    def tearDownClass(cls):
        if 'servers' in cls.test_data:
            for server in cls.test_data['servers']:
                try:
                    cls.compute.delete_server(server)
                    cls.compute.wait_for_server_termination(server)
                except:
                    print 'Cant delete server %s.'%server
        import time
        time.sleep(10)
        try:
            if cls.test_data.has_key('fip_id'):
                cls.os.floating_ips_client.delete_floating_ip(cls.test_data['fip_id'])

            if cls.test_data.has_key('secgroup_id'):
                cls.secgroups.delete_security_group(cls.test_data['secgroup_id'])

        finally:
            super(LbaasHttpsTestJSON, cls).tearDownClass()


    def test_lbaas_by_vip_ip(self):
        self.setup_lb_infra('TCP', 3, 1, 1, 22)
        vip_addr = self.test_data['vips'][0]['address']

        import socket
        s = socket.socket()

        try:
            for i in range(15):
                result = s.connect_ex((vip_addr, 22))
                s.close()
                time.sleep(10)
                if not result:
                    break
        except:
            print 'Socket error.'
            self.assertTrue(False)
        finally:
            s.close()
            time.sleep(10)
        self.assertEqual(0, result, 'Check if VIP is reachable.')
