import paramiko
import sys
import yaml
from scp import SCPClient
f =open("ipaddress.yml",mode='r',encoding = 'utf-8') 
read_data = yaml.full_load(f)
f.close()
ssh = paramiko.SSHClient()
ssh.load_host_keys('/home/wlc/.ssh/known_hosts')
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(read_data['guest_ip'],username = read_data['login'], password = read_data['password'],allow_agent=False)
guest_ip = read_data['guest_ip']
login = read_data['login']
host_password = read_data['password']
stdin, stdout, stderr = ssh.exec_command(sys.argv[1])
lines = stdout.readlines()
print(lines)

# SCPCLient takes a paramiko transport as an argument
#scp = SCPClient(ssh.get_transport())

#scp.put('test.txt', 'test2.txt')
#scp.get('test2.txt')

# Uploading the 'test' directory with its content in the
# '/home/user/dump' remote directory
#scp.put(sys.argv[1], recursive=True, remote_path='/home/wlc/GenVT_Env')

#scp.close()
