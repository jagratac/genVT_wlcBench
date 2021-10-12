#!/bin/bash
if [ -z $1 ];then
    echo "syntex:./init.sh wl_name"
    echo $1
    exit
fi
python3 genvt_scp.py $1
