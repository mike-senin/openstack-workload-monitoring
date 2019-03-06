#!/usr/bin/python

# Copyright (c) 2019 Mikhail Senin
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': ''}


DOCUMENTATION = '''
module: os_hypervisor_facts
short_description: Retrieve facts about an hypervisor within OpenStack.
version_added: "1.0"
author: "Mikhail Senin (@msenin94)"
description:
    - Retrieve facts about a hypervisor from OpenStack.
notes:
    - Facts are placed in the C(openstack_hypervisor) variable.
requirements:
    - "python >= 2.7"
    - "openstacksdk"
options:
   hypervisor_id:
     description:
        - ID of the hypervisor, integer
     required: false
extends_documentation_fragment: openstack
'''

EXAMPLES = '''
- name: Gather facts about a previously hypervisor with id 1
  os_hypervisor_facts:
    auth:
      auth_url: https://identity.example.com
      username: user
      password: password
      project_name: someproject
    hypervisor: 1
- name: Show openstack facts
  debug:
    var: openstack_image
# Show all available Openstack hypervisors
- name: Retrieve all available Openstack hypervisors
  os_hypervisor_facts:
- name: Show hypervisors
  debug:
    var: openstack_hypervisor
'''

# TODO (msenin):
RETURN = '''
openstack_hypervisor:
    description: has all the openstack facts about the hypervisor
    returned: always, but can be null
    type: complex
    contains:
        id:
            description: Unique UUID.
            returned: success
            type: str
        name:
            description: Name given to the image.
            returned: success
            type: str
        status:
            description: Image status.
            returned: success
            type: str
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.openstack import openstack_full_argument_spec, openstack_module_kwargs, openstack_cloud_from_module


def main():

    argument_spec = openstack_full_argument_spec(
        hypervisor_id=dict(required=False, type='int'),
        enabled=dict(required=False, type='bool'),
        active=dict(reqired=False, type='bool')
    )
    module_kwargs = openstack_module_kwargs(
        mutually_exclusive=[
            ['hypervisor_id', 'enabled'],
            ['hypervisor_id', 'active'],
        ],
    )
    module = AnsibleModule(argument_spec, **module_kwargs)

    sdk, cloud = openstack_cloud_from_module(module)
    try:
        if module.params['hypervisor_id']:
            hypervisor = cloud.compute.get_hypervisor(module.params['hypervisor_id'])
            module.exit_json(changed=False, ansible_facts=dict(
                openstack_hypervisor=hypervisor))
        else:
            hypervisors = list(cloud.compute.hypervisors())
            if module.params['enabled']:
                hypervisors = filter(lambda x: x['status'] == 'enabled', hypervisors)

            if module.params['active']:
                hypervisors = filter(lambda x: x['state'] == 'up', hypervisors)

            module.exit_json(changed=False, ansible_facts=dict(
                openstack_hypervisor=hypervisors))

    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
