import sys
import libvirt
import xml_parsing_main as xml
import time
import os
import getpass
import libvirt_console as console_vm
from yml_parser import YAMLParser
import netifaces as ni

#opening connection from hypervisor 
try:
    conn = libvirt.open('qemu:///system')
    os.system("clear")
except libvirt.libvirtError as e:
    print(repr(e),file=sys.stderr)
    exit(1)

#geting user name of host machine
username = getpass.getuser()
print("Username of Host machine:{}".format(username))

#geting ip address of host machine
ni.ifaddresses('virbr0')
ip = ni.ifaddresses('virbr0')[ni.AF_INET][0]['addr']
print("IP Address of Host machine:{}".format(ip))

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
os_name = parser.get("os_name",vm)
wl_info = parser.get("proxy_wl",vm)
workload_name = wl_info[0]['wl']
init_cmd = wl_info[0]['init_cmd']
print(workload_name)
print(os_name)
print(init_cmd)



#reading xml configuration for domain creation
try:
    for vm_count in range(0,1):
        xml.vm_xml_create(vm_count,vm_name,os_image)
        f_xml = open(f'vm_{vm_count}.xml','r')
        dom = conn.createXML(f_xml.read(),2)
#        dom = conn.defineXMLFlags(f_xml.read(),0)
#        if dom.create() < 0:
#            print("Can Not boot guest domain {file=sys.stderr}")
except Exception:
    print("Can Not boot guest domain {file=sys.stderr}")
    

print(f"system : {dom.name()}  booted, file=sys.stderr")

print(f"Sleep for 20 second")
time.sleep(20)

#console call for created VM
console = console_vm.Console('qemu:///system',dom.name(),wl_info)
console.stdin_watch = libvirt.virEventAddHandle(0, libvirt.VIR_EVENT_HANDLE_READABLE, console_vm.stdin_callback, console)

while console_vm.check_console(console):
    libvirt.virEventRunDefaultImpl()
#dom.destroy()
conn.close()
exit(0)
