


src=$1
#dest=$2
params_file=$2
synbench_dir=$3

python3 yaml_read.py $src $src $params_file
cd $3
make

export DESTDIR=$PWD
./synbench params/intel_indu_hmi_high_profile.txt 
