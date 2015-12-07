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

from oslo_serialization import jsonutils as json

from tempest.common import service_client


class IdentityClient(service_client.ServiceClient):
    api_version = "v2.0"

    def show_api_description(self):
        """Retrieves info about the v2.0 Identity API"""
        url = ''
        resp, body = self.get(url)
        self.expected_success([200, 203], resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def create_role(self, name):
        """Create a role."""
        post_body = {
            'name': name,
        }
        post_body = json.dumps({'role': post_body})
        resp, body = self.post('OS-KSADM/roles', post_body)
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def show_role(self, role_id):
        """Get a role by its id."""
        resp, body = self.get('OS-KSADM/roles/%s' % role_id)
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def create_tenant(self, name, **kwargs):
        """Create a tenant

        name (required): New tenant name
        description: Description of new tenant (default is none)
        enabled <true|false>: Initial tenant status (default is true)
        """
        post_body = {
            'name': name,
            'description': kwargs.get('description', ''),
            'enabled': kwargs.get('enabled', True),
        }
        post_body = json.dumps({'tenant': post_body})
        resp, body = self.post('tenants', post_body)
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def delete_role(self, role_id):
        """Delete a role."""
        resp, body = self.delete('OS-KSADM/roles/%s' % str(role_id))
        self.expected_success(204, resp.status)
        return resp, body

    def list_user_roles(self, tenant_id, user_id):
        """Returns a list of roles assigned to a user for a tenant."""
        url = '/tenants/%s/users/%s/roles' % (tenant_id, user_id)
        resp, body = self.get(url)
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def assign_user_role(self, tenant_id, user_id, role_id):
        """Add roles to a user on a tenant."""
        resp, body = self.put('/tenants/%s/users/%s/roles/OS-KSADM/%s' %
                              (tenant_id, user_id, role_id), "")
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def delete_user_role(self, tenant_id, user_id, role_id):
        """Removes a role assignment for a user on a tenant."""
        resp, body = self.delete('/tenants/%s/users/%s/roles/OS-KSADM/%s' %
                                 (tenant_id, user_id, role_id))
        self.expected_success(204, resp.status)
        return service_client.ResponseBody(resp, body)

    def delete_tenant(self, tenant_id):
        """Delete a tenant."""
        resp, body = self.delete('tenants/%s' % str(tenant_id))
        self.expected_success(204, resp.status)
        return service_client.ResponseBody(resp, body)

    def show_tenant(self, tenant_id):
        """Get tenant details."""
        resp, body = self.get('tenants/%s' % str(tenant_id))
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def list_roles(self):
        """Returns roles."""
        resp, body = self.get('OS-KSADM/roles')
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def list_tenants(self):
        """Returns tenants."""
        resp, body = self.get('tenants')
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def update_tenant(self, tenant_id, **kwargs):
        """Updates a tenant."""
        body = self.show_tenant(tenant_id)['tenant']
        name = kwargs.get('name', body['name'])
        desc = kwargs.get('description', body['description'])
        en = kwargs.get('enabled', body['enabled'])
        post_body = {
            'id': tenant_id,
            'name': name,
            'description': desc,
            'enabled': en,
        }
        post_body = json.dumps({'tenant': post_body})
        resp, body = self.post('tenants/%s' % tenant_id, post_body)
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def create_user(self, name, password, tenant_id, email, **kwargs):
        """Create a user."""
        post_body = {
            'name': name,
            'password': password,
            'email': email
        }
        if tenant_id is not None:
            post_body['tenantId'] = tenant_id
        if kwargs.get('enabled') is not None:
            post_body['enabled'] = kwargs.get('enabled')
        post_body = json.dumps({'user': post_body})
        resp, body = self.post('users', post_body)
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def update_user(self, user_id, **kwargs):
        """Updates a user."""
        put_body = json.dumps({'user': kwargs})
        resp, body = self.put('users/%s' % user_id, put_body)
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def show_user(self, user_id):
        """GET a user."""
        resp, body = self.get("users/%s" % user_id)
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def delete_user(self, user_id):
        """Delete a user."""
        resp, body = self.delete("users/%s" % user_id)
        self.expected_success(204, resp.status)
        return service_client.ResponseBody(resp, body)

    def list_users(self):
        """Get the list of users."""
        resp, body = self.get("users")
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def enable_disable_user(self, user_id, enabled):
        """Enables or disables a user."""
        put_body = {
            'enabled': enabled
        }
        put_body = json.dumps({'user': put_body})
        resp, body = self.put('users/%s/enabled' % user_id, put_body)
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def show_token(self, token_id):
        """Get token details."""
        resp, body = self.get("tokens/%s" % token_id)
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def delete_token(self, token_id):
        """Delete a token."""
        resp, body = self.delete("tokens/%s" % token_id)
        self.expected_success(204, resp.status)
        return service_client.ResponseBody(resp, body)

    def list_tenant_users(self, tenant_id):
        """List users for a Tenant."""
        resp, body = self.get('/tenants/%s/users' % tenant_id)
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def create_service(self, name, type, **kwargs):
        """Create a service."""
        post_body = {
            'name': name,
            'type': type,
            'description': kwargs.get('description')
        }
        post_body = json.dumps({'OS-KSADM:service': post_body})
        resp, body = self.post('/OS-KSADM/services', post_body)
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def show_service(self, service_id):
        """Get Service."""
        url = '/OS-KSADM/services/%s' % service_id
        resp, body = self.get(url)
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def list_services(self):
        """List Service - Returns Services."""
        resp, body = self.get('/OS-KSADM/services')
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def delete_service(self, service_id):
        """Delete Service."""
        url = '/OS-KSADM/services/%s' % service_id
        resp, body = self.delete(url)
        self.expected_success(204, resp.status)
        return service_client.ResponseBody(resp, body)

    def create_endpoint(self, service_id, region_id, **kwargs):
        """Create an endpoint for service."""
        post_body = {
            'service_id': service_id,
            'region': region_id,
            'publicurl': kwargs.get('publicurl'),
            'adminurl': kwargs.get('adminurl'),
            'internalurl': kwargs.get('internalurl')
        }
        post_body = json.dumps({'endpoint': post_body})
        resp, body = self.post('/endpoints', post_body)
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def list_endpoints(self):
        """List Endpoints - Returns Endpoints."""
        resp, body = self.get('/endpoints')
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def delete_endpoint(self, endpoint_id):
        """Delete an endpoint."""
        url = '/endpoints/%s' % endpoint_id
        resp, body = self.delete(url)
        self.expected_success(204, resp.status)
        return service_client.ResponseBody(resp, body)

    def update_user_password(self, user_id, new_pass):
        """Update User Password."""
        put_body = {
            'password': new_pass,
            'id': user_id
        }
        put_body = json.dumps({'user': put_body})
        resp, body = self.put('users/%s/OS-KSADM/password' % user_id, put_body)
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def update_user_own_password(self, user_id, new_pass, old_pass):
        """User updates own password"""
        patch_body = {
            "password": new_pass,
            "original_password": old_pass
        }
        patch_body = json.dumps({'user': patch_body})
        resp, body = self.patch('OS-KSCRUD/users/%s' % user_id, patch_body)
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def list_extensions(self):
        """List all the extensions."""
        resp, body = self.get('/extensions')
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def create_user_ec2_credentials(self, user_id, **kwargs):
        # TODO(piyush): Current api-site doesn't contain this API description.
        # After fixing the api-site, we need to fix here also for putting the
        # link to api-site.
        post_body = json.dumps(kwargs)
        resp, body = self.post('/users/%s/credentials/OS-EC2' % user_id,
                               post_body)
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def delete_user_ec2_credentials(self, user_id, access):
        resp, body = self.delete('/users/%s/credentials/OS-EC2/%s' %
                                 (user_id, access))
        self.expected_success(204, resp.status)
        return service_client.ResponseBody(resp, body)

    def list_user_ec2_credentials(self, user_id):
        resp, body = self.get('/users/%s/credentials/OS-EC2' % user_id)
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def show_user_ec2_credentials(self, user_id, access):
        resp, body = self.get('/users/%s/credentials/OS-EC2/%s' %
                              (user_id, access))
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)
