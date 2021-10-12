for ((i=0;i<=20;i++)); 
do 
   # your-unix-command-here
    virsh destroy ubuntu-vm-$i
    virsh undefine ubuntu-vm-$i
    rm vm_$i.xml
    echo $i
done

