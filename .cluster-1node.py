
from socket import gethostname
import os

defaults = {
    'netmask': '255.255.255.0',
    'public_key': '~/.ssh/id_rsa.pub',
    'private_key': '~/.ssh/id_rsa',
    'domain_name': 'local',
    'extra_disks': {},

    'openstack': {
        'flavor': 'm1.large',
        'image': 'Ubuntu-14.04-64',
        'key_name': gethostname(),
        'network': '{}-net'.format(os.getenv('OS_PROJECT_NAME')),
        'create_floating_ip': False, 
        'floating_ip_pool': 'ext-net',
        'security_groups': ['default'],
    },

    'vagrant': {
        'provider': 'libvirt',
        'box': 'ubuntu/14.04'
    },

    'provider': 'openstack',
}


hadoop = lambda i: {
    'hadoop%d' % i: {}
}



machines = [hadoop(0)]
hostnames = map(lambda n: n.keys()[0], machines)

namenodes = {'namenodes': hostnames}
backup_namenodes = {'backup_namenodes': []}
journalnodes = {'journalnodes': hostnames}
historyservers = {'historyservernodes': hostnames}
resourcemanagers = {'resourcemanagernodes': hostnames}
datanodes = {'datanodes': hostnames}
frontends = {'frontendnodes': hostnames}
hadoopnodes = combine('hadoopnodes', namenodes, datanodes,
                      journalnodes, historyservers)
monitornodes = {'monitornodes': hostnames}

inventory = [
    namenodes,
    backup_namenodes,
    journalnodes,
    historyservers,
    resourcemanagers,
    datanodes,
    frontends,
    hadoopnodes,
    monitornodes,
]


spec = {
    'defaults': defaults,
    'machines': machines,
    'inventory': inventory,
}


