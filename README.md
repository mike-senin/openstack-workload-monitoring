# Openstack workload monitoring tool
## Description
This solution allows to prepare test workload within environment and monitor instances availability during scheduled operations such as ceph or contrail upgrades.

By default ansible playbook creates one basic monitor VM that has prometheus, alertmanager and alerta as docker compose services at the top of itself. In addition it generates dedicated count of dummy VMs with prometheus exporter that used as monitoring goals to check the instances availability.


## Glossary
"Daemon Set"
TBD

## Architecture overview
![Architecture diagram](docs/architecture_diagram.png?raw=true "Architecture diagram")

TBD

## Installation
### Install pip requirements
```sh
$ git clone https://github.com/msenin94/openstack-workload-monitoring
$ cd openstack-workload-monitoring
$ virtualenv .venv
$ .venv/bin/activate
$ pip install -r requirements.txt

```

### Prepare clouds.yaml
You need to fill up and put `clouds.yaml` file to root project folder. Content example:
```yaml
clouds:
  devstack:
    auth:
      auth_url: http://192.168.122.10:35357/
      project_name: demo
      username: demo
      password: 0penstack
    region_name: RegionOne
  ds-admin:
    auth:
      auth_url: http://192.168.122.10:35357/
      project_name: admin
      username: admin
      password: 0penstack
    region_name: RegionOne
  infra:
    cloud: rackspace
    auth:
      project_id: 275610
      username: openstack
      password: xyzpdq!lazydog
    region_name: DFW,ORD,IAD
    interface: internal
```
More information about `clouds.yaml` you may find in the [official documentation]( https://docs.openstack.org/python-openstackclient/pike/configuration/index.html).

### Set up variables for roles

#### project vars:
#### put info how to configure

#### role: create_instances
#### put info how to configure

### Requirements
TBD, count all openstack resources needed for playbook start

## Usage
From root project folder execute:
```sh
$ ansible-playbook -i hosts --private-key=<path-to-mon.pem> main.yaml
```

## Potential problems

1. Squid proxy cache is incorrect
Ways to fix: 

a. restart squid

b. remove cache from cache folders, recreate them and restart service

2. External proxy is unavailable or slow
The most obvious behaviour when you see timeouts errors during pip, apt commands execution or docker image pull. In this case restart manifests.
   

## Todos
- Add openstack resources creation - project, private key, security group, network, etc.
- Migrate cloud init logic to ansible role
- Create and attach volumes for each service for datastore as it should be split from system volume
- Make tasks async
- Optimise roles
- Extend documentation
- Add new alert rule - ping / curl destination from external network and fire alert once external network is unavailable
- Add dockerfile
- Make proxy peaces optional 
- Add kitchen: ansible-playbook --syntax-check