import paramiko
import sys
from scp import SCPClient
f = open("ipaddress.txt",mode='r',encoding = 'utf-8')
read_data = f.read()
ipaddress = read_data.split(':=')
print(ipaddress[1])
ssh = paramiko.SSHClient()
ssh.load_host_keys('/home/wlc/.ssh/known_hosts')
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ipaddress[1],username='wlc',password='wlc123',allow_agent=False)

# SCPCLient takes a paramiko transport as an argument
scp = SCPClient(ssh.get_transport())

#scp.put('test.txt', 'test2.txt')
#scp.get('test2.txt')

# Uploading the 'test' directory with its content in the
# '/home/user/dump' remote directory
scp.put(sys.argv[1], recursive=True, remote_path='/home/wlc')

scp.close()
