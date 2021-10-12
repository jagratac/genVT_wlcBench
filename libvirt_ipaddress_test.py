import sys
import libvirt
import paramiko
from scp import SCPClient
from yml_parser import YAMLParser

#def Guest_IPAddress(vm_name):
conn = None
try:
    conn = libvirt.open("qemu:///system")
except libvirt.libvirtError as e:
    print(repr(e), file=sys.stderr)
    exit(1)
# Check arguments
if len(sys.argv) != 2:
    sys.exit("Usage: ./wlc_bench.py <config.yaml>")
# no longer need to specify breakpoint_serial, only takes 1 arg - yml file
yml_file = sys.argv[1]

# default mode, none other currently defined
wlc_bench_mode = "breakpoint_serial"

# parse YML file
parser = YAMLParser(yml_file)
parsed_file = parser.parse()

#picking values from YAML
mode = parser.get(wlc_bench_mode, parsed_file)
vm = parser.get("vm_0", mode)
os_image = parser.get("os_image",vm)
vm_name = parser.get("vm_name",vm)
try:
    dom = conn.lookupByName(vm_name)
    if dom == None:
        print('Failed to get the domain object', file=sys.stderr)
    
    ifaces = dom.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
#    print("The interface IP addresses:")
    for (name, val) in ifaces.items():
        if val['addrs']:
            for ipaddr in val['addrs']:
                if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
#               print(ipaddr['addr'] + " VIR_IP_ADDR_TYPE_IPV4")
                    temp = ipaddr['addr'].split('.')
                    ipaddress = [ipaddr['addr'] for i in temp if (i == '192')]
#                print(ipaddress)
    conn.close()

except Exception:
    print("Attribut error")

try:
    ssh = paramiko.SSHClient()
    ssh.load_host_keys('/home/wlc/.ssh/known_hosts')
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(str(ipaddress[0]),username="wlc",password="wlc123",allow_agent=False)
    print(str(ipaddress[0]))
# SCPCLient takes a paramiko transport as an argument
    scp = SCPClient(ssh.get_transport())
#scp.put('test.txt', 'test3.txt')
#scp.get('test2.txt')

# Uploading the 'test' directory with its content in the
# '/home/user/dump' remote directory
    scp.put('synbench', recursive=True, remote_path='/home/wlc/Public')
    scp.close()
except Exception:
    print("Attribute Error")


