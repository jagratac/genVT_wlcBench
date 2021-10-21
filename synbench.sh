#!/bin/bash
#if [ -z $@ ];then
#    echo "syntex:./synbench.sh cmd"
#    echo $1
#    exit
#fi
python3 genvt_ssh_2.py 'cd ${HOME}/GenVT_Env/synbench/ && ./synbench_guest.sh'
#sleep 5
python3 genvt_ssh_2.py 'cd ${HOME}/GenVT_Env/synbench/ && ./mqtt_build.sh'
#sleep 5
python3 genvt_ssh_2.py 'cd ${HOME}/GenVT_Env/synbench/ && ./synbench_build.sh'
#python3 demo_ssh.py
