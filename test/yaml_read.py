import sys
import yaml


msgbus = sys.argv[1]
dest_file = sys.argv[2]
sos_params = sys.argv[3]

with open(sos_params) as f:
    data = yaml.full_load(f)

with open(msgbus) as f:
    cpp_data = f.readlines()

with open(dest_file,'w') as f:
    for line in cpp_data:
        if 'tcp://' in line:
            line = line.split(':')
            line[1] = '://'+data['ip']+':'
            line = ''.join(line)
        f.write(line)

print(f"IP of MQTT to publish has been changed to {data['ip']}")
