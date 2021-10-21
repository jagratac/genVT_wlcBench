import sys
import yaml
import paramiko


def get_VM_info():
    
    with open('ipaddress.yml',mode='r',encoding='utf-8') as f:
        data = yaml.full_load(f)
    f.close()
    return data['guest_ip'], data['login'], data['password']

def Create_SSH(guest_ip,vm_password,login):
    
    if None in [guest_ip,login,vm_password]:
        print('Missing one of the required credentails')
        return None

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Addedd to Keys if missing
    ssh.load_system_host_keys()
    
    try:
        ssh.connect(guest_ip, username=login, password=vm_password,allow_agent=False)
        print(f'Connected to {guest_ip} as {login}')
    except Exception as e:
        print(f"Error: {e} while connecting to {guest_ip} as {login}")
    
    return ssh


def ssh_guest(cmd):
    # Check arguments
#    if len(sys.argv) != 2:
#        sys.exit("Usage:  python3 genvt_ssh.py <cmd>")

    guest_ip ,login, vm_password= get_VM_info()
    ssh = Create_SSH(guest_ip,vm_password,login)

    if ssh is None:
        print('Error in creating connection')
        sys.exit()

    print(f"\r\nExecuting the WL by the command :{cmd}")
    #channel = ssh.invoke_shell()
    #while not channel.send_ready(): 
    #    time.sleep(1)
    #    channel.send(f"{sys.argv[1]}\n")
    stdin, stdout, stderr = ssh.exec_command(cmd)
#    lines = stdout.readlines()
    error = stderr.readlines()
#    print(lines)
    for data in error:
        print(f"\n\r{data}")
