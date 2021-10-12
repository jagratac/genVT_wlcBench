
'''def get_yml_values(mode, parsed_file, parser):
        """
         Extract all values from parsed YML object
         :param mode: WLC mode, ex: breakpoint_serial
         :param parsed_file: parsed object from parse() API
         :param parser: YML parser object handle
         :return: tuple of values
        """
        mode = parser.get(mode, parsed_file)

        # get os image name
        os_image = parser.get("os_image", mode) 

        # get no. of vm_instance 
        vm_name = parser.get("vm_name", mode)

        return os_image,vm_name
'''
'''
#checking state for VM
state, reason = dom.state()

if state == libvirt.VIR_DOMAIN_NOSTATE:
    print('The state is VIR_DOMAIN_NOSTATE')
elif state == libvirt.VIR_DOMAIN_RUNNING:
    print('The state is VIR_DOMAIN_RUNNING')
elif state == libvirt.VIR_DOMAIN_BLOCKED:
    print('The state is VIR_DOMAIN_BLOCKED')
elif state == libvirt.VIR_DOMAIN_PAUSED:
    print('The state is VIR_DOMAIN_PAUSED')
elif state == libvirt.VIR_DOMAIN_SHUTDOWN:
    print('The state is VIR_DOMAIN_SHUTDOWN')
elif state == libvirt.VIR_DOMAIN_SHUTOFF:
    print('The state is VIR_DOMAIN_SHUTOFF')
elif state == libvirt.VIR_DOMAIN_CRASHED:
    print('The state is VIR_DOMAIN_CRASHED')
elif state == libvirt.VIR_DOMAIN_PMSUSPENDED:
    print('The state is VIR_DOMAIN_PMSUSPENDED')
else:
    print(' The state is unknown.')
print('The reason code is ' + str(reason))
'''
'''
        conn = None
    try:
        conn = libvirt.open("qemu:///system")
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
        exit(1)
    temp = []
    dom = conn.lookupByName(vm_name)
    if dom == None:
        print('Failed to get the domain object', file=sys.stderr)
        '''
