import paramiko
from scp import SCPClient

def guest_ssh_scp(guest_ip,guest_username,guest_password,cmd):
    
    print(f"guest ip:{guest_ip}")
    print(f"guest username:{guest_username}")
    print(f"guest password:{guest_password}")
    print(f"command:{cmd}")

    ssh = paramiko.SSHClient()
    ssh.load_host_keys('/home/wlc/.ssh/known_hosts')
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(str(guest_ip),username=str(guest_username),password=str(guest_password),allow_agent=False)
    # SCPCLient takes a paramiko transport as an argument
    scp = SCPClient(ssh.get_transport())
#    scp.put('test.txt', 'test3.txt')
#    scp.get('test2.txt')

    # Uploading the 'test' directory with its content in the
    # '/home/user/dump' remote directory
    scp.put('test', recursive=True, remote_path='/home/wlc/Public')

    scp.close()

   # stdin, stdout, stderr = ssh.exec_command(cmd)
   # lines = stdout.readlines()
   # print(lines)
