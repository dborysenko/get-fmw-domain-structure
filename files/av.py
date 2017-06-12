#!/usr/bin/env python
import os
import ConfigParser
import StringIO
import json
try:
    import xml.etree.ElementTree as ET
except ImportError:
    import cElementTree as ET


NODEMANAGER_DOMAINS = "/opt/oracle/admin/nodemanager/common/nodemanager.domains"

if not hasattr(os, 'SEEK_SET'):
    os.SEEK_SET = 0


def get_domains():
    init_config = NODEMANAGER_DOMAINS
    cp = ConfigParser.ConfigParser()
    config = StringIO.StringIO()
    try:
        # Fake leading section
        config.write('[fakesection]\n')
        config.write(open(init_config).read())
        config.seek(0, os.SEEK_SET)
        #
        cp.readfp(config)
        result = cp.items('fakesection')
        config.close()
        return result
    except IOError, e:
        print "ERROR.\nCannot open file: %(filename)s.\nError: %(error)s" % {
            'filename': init_config,
            'error': e.strerror,
        }
        config.close()
        exit(1)

domains = get_domains()
# domains = [['Testdomain', '/Users/dborysenko/Downloads', ], ]
result = {}
dom = {}
clusters = {}
res = []
resd = {}
for domain in domains:
    domain_config = os.path.join(domain[1], "config", "config.xml")
    try:
        tree = ET.parse(domain_config)
    except IOError, e:
        print "Can't open file %(filename)s\tError: %(error)s" % {
            'filename': domain_config,
            'error': e.strerror,
        }
        continue
    root = tree.getroot()
    nms = {}
    servers = {}
    dom[domain[0]] = {'children': [], 'vars': {}}
    for cluster in root.findall("{http://xmlns.oracle.com/weblogic/domain}cluster"):
        # clusters.append(cluster.find("{http://xmlns.oracle.com/weblogic/domain}name").text)
        clusters[cluster.find("{http://xmlns.oracle.com/weblogic/domain}name").text] = {'hosts': []}

    for machine in root.findall("{http://xmlns.oracle.com/weblogic/domain}machine"):
        nodemanager = machine.find("{http://xmlns.oracle.com/weblogic/domain}node-manager")
        name = machine.find("{http://xmlns.oracle.com/weblogic/domain}name").text
        nms.update({name:
                    nodemanager.find("{http://xmlns.oracle.com/weblogic/domain}listen-address").text})

    for server in root.findall("{http://xmlns.oracle.com/weblogic/domain}server"):
        machine = server.find("{http://xmlns.oracle.com/weblogic/domain}machine").text
        name = server.find("{http://xmlns.oracle.com/weblogic/domain}name").text
        port = server.find("{http://xmlns.oracle.com/weblogic/domain}listen-port")
        cluster = server.find("{http://xmlns.oracle.com/weblogic/domain}cluster")
        if cluster is not None:
            cluster = cluster.text
        if name == "AdminServer":
            cluster = "AdminServer"
            # continue
        managed_addr = server.find("{http://xmlns.oracle.com/weblogic/domain}listen-address").text
        if machine:
            servers.update({name: {'nm_addr': nms[machine], 'managed_addr': managed_addr, 'port': port}})
        else:
            servers.update({name: {'nm_addr': "None", 'managed_addr': managed_addr, 'port': port}})
        res.append(nms[machine])
        resd[nms[machine]] = dict(cluster=cluster)
        # clusters[cluster]['hosts'].append(nms[machine])
    # dom[domain[0]]['children'] = clusters.keys()
    # dom[domain[0]]['vars'] = {'ansible_user': 'oracle', 'ansible_ssh_private_key_file': 'ansible_ssh_private_key_file=/Users/dborysenko/.ssh/id_rsa'}
print json.dumps(resd)
# for i in set(res):
#     print i

# print clusters
# print dom
# res = json.dumps(dict(clusters.items() + dom.items()))
# print json.dumps(dict(clusters['web_cluster_1'].items() + {'vars': {'ansible_user': 'oracle'}}.items()))
