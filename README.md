Get FMW Domain Structure
=========


Role reads domain configuration in order to create in-memory inventory of each host which is part of the domain. So you can apply any subsequent roles against each host within domain. 

Requirements
------------

Tested with weblogic 10.3.6 (FMW 11.1.1.6) 

Role Variables
--------------

    vars:
        NODEMANAGER_DOMAINS: /opt/oracle/admin/nodemanager/common/nodemanager.domains #nodemanager.domains config location
        

Example Playbook
----------------



site.yml:
    
    - hosts: adminserver
      serial: 1 #this one is important to be able to gather info from more than 1 domain at one run
      roles:
        - get-fmw-domain-structure


hosts:
    
    
    [adminserver]
    adminsrv.example.com
    
    [singlehosts]
    
    [weblogic]
    
    [all]
    
    [all:children]
    adminserver
    singlehosts
    weblogic
    
    [all:vars]
    ansible_user=dborysenko
    ansible_become_method=su
    ansible_become_exe=dzdo
    ansible_become_flags="su -"    
     
    
    

License
-------

BSD

Author Information
------------------

Dmytro Borysenko borysenus@gmail.com
