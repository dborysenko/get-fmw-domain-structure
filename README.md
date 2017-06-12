Get FMW Domain Structure
=========

Role reads domain configuration in order to create in memory inventory of each host which is part of the domain. So you can apply any subsequent roles against each host within domain. 

Requirements
------------

There is an assumption that nodemanager's config "nodemanager.domains" is located in /opt/oracle/admin/nodemanager/common/nodemanager.domains If it is not the case in your installation, feel free to edit readDomainConfig.py 

Role Variables
--------------

TODO: redefine nodemanager's config as variable.

Dependencies
------------

No edpendencies.

Example Playbook
----------------

TOD: provide an example of usage

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

BSD

Author Information
------------------

Dmytro Borysenko borysenus@gmail.com
