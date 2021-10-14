import sys
import yaml
import paramiko




def get_VM_info():
    
    with open(sys.argv[1]) as f:
        data = yaml.full_load(f)
    return data['ip'], data['un'], data['pwd'], data['cmd']

def Create_SSH():
    
    if None in [host,un,pwd]:
        print('Missing one of the required credentails')
        return None

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Addedd to Keys if missing
    ssh.load_system_host_keys()
    
    try:
        ssh.connect(host, username=un, password=pwd)
        print(f'Connected to {host} as {un}')
    except Exception as e:
        print(f"Error: {e} while connecting to {host} as {un}")
    
    return ssh



host, un, pwd, cmd = get_VM_info()
ssh = Create_SSH()


if ssh is None:
    print('Error in creating connection')
    sys.exit()

print(f"Executing the WL by the command {cmd}")
ssh.exec_command(cmd)
