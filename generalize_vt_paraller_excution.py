import sys
import libvirt
import concurrent.futures
import time
import consolecallback_test as console_vm
import xml_parsing_main as xml
i = 0
start = time.perf_counter()

def vm_creation(i):
    #opening connection from hypervisor 
    try:
        conn = libvirt.open('qemu:///system')
    except libvirt.libvirtError as e:
        print(repr(e),file=sys.stderr)
        exit(1)
    
    #reading xml configuration for domain creation
    try:
        xml.vm_xml_create(i)
        f_xml = open(f'vm_{i}.xml','r')
#    f_xml = open(f'vm_0.xml','r')

    # conn.createXML api will create domain and start the domain if you pass second argument as 2 it will distroy domain automatically.... 
    #VIR_DOMAIN_START_AUTODESTROY flag is set ....
    # search the value for flag in this link https://libvirt.org/html/libvirt-libvirt-domain.html#VIR_DOMAIN_START_AUTODESTROY
        dom = conn.defineXMLFlags(f_xml.read(),0)
        if dom.create() < 0:
            print("Can Not boot guest domain {file=sys.stderr}")
    except Exception:
        print("Can Not boot guest domain {file=sys.stderr}")


    # dom = conn.defineXMLFlags api will only define the domain you have to start domain by calling create function on domain object...
    #dom = conn.defineXMLFlags(f_xml.read(),0)




    print(f"system : {dom.name()}  booted, file=sys.stderr")
    print(f"Sleep for 20 second")
    time.sleep(20)
    console = console_vm.Console('qemu:///system',dom.name())
    console.stdin_watch = libvirt.virEventAddHandle(0, libvirt.VIR_EVENT_HANDLE_READABLE, console_vm.stdin_callback, console)
    while console_vm.check_console(console):
        libvirt.virEventRunDefaultImpl()
    conn.close()

if __name__ == "__main__":

    with concurrent.futures.ProcessPoolExecutor() as executor:
        args = [0,1,2,3,4]
        results = executor.map(vm_creation, args)
    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} second(s)')

#print(f"Sleep for 20 second")
#time.sleep(20)
#console = console_vm.Console('qemu:///system','ubuntu-vm-0')
#console.stdin_watch = libvirt.virEventAddHandle(0, libvirt.VIR_EVENT_HANDLE_READABLE, console_vm.stdin_callback, console)
#while console_vm.check_console(console):
#    libvirt.virEventRunDefaultImpl()
#conn.close()
#exit(0)
