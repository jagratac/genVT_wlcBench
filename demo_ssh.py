import paramiko
import yaml
import time
import re
with open('ipaddress.yml',mode='r',encoding='utf-8') as f:
    data = yaml.full_load(f)
    f.close()
#    return data['guest_ip'], data['login'], data['password']
bastion_ip=data['guest_ip']
bastion_pass='wlc123'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
ssh.connect(bastion_ip, username='wlc', password=bastion_pass,allow_agent=False)

chan = ssh.invoke_shell()

# other cloud server 
priv_ip=data['guest_ip']
passw='wlc123'

test_script='/home/wlc/GenVT_Env/synbench/synbench_build.sh'
   
def run_cmd(cmd):
    buff = ''
    while not buff.endswith(':~$ '):
        resp = chan.recv(9999)
        buff += resp.decode()
        print(resp)

    # Ssh and wait for the password prompt.
    chan.send(cmd + '\n')
    buff = ''
    while not buff.endswith(' wlc@wlc-ubuntu:~/GenVT_Env/synbench$'):
        resp = chan.recv(9999)
        buff += resp.decode()
        print(resp)
    
    # Send the password and wait for a prompt.
    time.sleep(3)
    chan.send(passw + '\n')

    buff = ''
    while buff.find(' done.') < 0 :
        resp = chan.recv(9999)
        buff += resp.decode()
        print(resp)
       
    ret=re.search( '(\d) done.', buff).group(1)
    ssh.close()

    print('command was successful:' + str(ret=='0'))

scp_opt=""
#cmd='scp -q ' + scp_opt + ' -o NumberOfPasswordPrompts=1 -o StrictHostKeyChecking=no %s wlc@%s:~/; echo $? done.' % ( test_script, priv_ip )
cmd = 'cd /home/wlc//GenVT_Env/synbench && ./synbench_guest.sh && ./mqtt_build.sh && ./synbench_build.sh'
print('\n test 2\n cmd %s\n' % cmd)
run_cmd(cmd)
