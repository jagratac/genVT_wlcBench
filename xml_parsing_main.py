import xml.etree.ElementTree as ET

def vm_xml_create(num,vm_name,os_image):

    mytree= ET.parse('vm_standered.xml')
    myroot = mytree.getroot()

    for name in myroot.iter('name'):
        a = str(vm_name)
        name.text = str(a)
    for device_element in myroot.findall('devices'):
        for disk_element in device_element.findall('disk'):
            file_dict = disk_element.find('source').attrib
            file_dict['file'] = str(os_image)
#            print(file_dict['file'])
            target_dict = disk_element.find('target').attrib
            target_dict['dev'] = str(f'vd{chr(vm_xml_create.lc_ch)}')
            vm_xml_create.lc_ch += 1
#            print(target_dict['dev'])
        for serial_element in device_element.findall('serial'):
            target_serial_dict = serial_element.find('target').attrib
            target_serial_dict['port'] = chr((num%10)+48)
#            print(target_serial_dict['port'])
        for console_element in device_element.findall('console'):
            target_console_dict = console_element.find('target').attrib
            target_console_dict['port'] = chr((num%10)+48)
            if num > 9:
                target_console_dict['type'] = 'virtio'
            else:
                target_console_dict['type'] = 'serial'

#            print(target_console_dict['port'])
#            print(target_console_dict['type'])
                
    mytree.write(f'vm_{num}.xml')	
# ascii value for 'a'
vm_xml_create.lc_ch = 97
