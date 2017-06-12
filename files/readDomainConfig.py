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
        clusters[cluster.find("{http://xmlns.oracle.com/weblogic/domain}name").text] = {'hosts': []}
    for server in root.findall("{http://xmlns.oracle.com/weblogic/domain}server"):
        machine = server.find("{http://xmlns.oracle.com/weblogic/domain}machine").text
        name = server.find("{http://xmlns.oracle.com/weblogic/domain}name").text
        port = server.find("{http://xmlns.oracle.com/weblogic/domain}listen-port")
        cluster = server.find("{http://xmlns.oracle.com/weblogic/domain}cluster")
        if cluster is not None:
            cluster = cluster.text
        if name == "AdminServer":
            cluster = "AdminServer"
        managed_addr = server.find("{http://xmlns.oracle.com/weblogic/domain}listen-address").text
        resd[managed_addr] = dict(cluster=cluster)
print json.dumps(resd)
