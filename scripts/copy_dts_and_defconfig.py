
## Run the script like this:
#
# python copy_dts_and_defconfig.py cm01 arch/arm/boot/dts/qcom/sdm450-mtp.dts arch/arm64/configs/msmcortex_defconfig

import os,shutil
from sys import argv

project_name = argv[1]
root_dts = argv[2]
root_def_config = argv[3]
root_dts_path = os.path.dirname(os.path.abspath(root_dts))
root_def_config_path = os.path.dirname(os.path.abspath(root_def_config))
pro_dts_path = root_dts_path + "/../" + project_name
#print "current path : %s" % os.getcwd()
#print "root dts path: %s" % root_dts_path
#print "root def config path: %s" % root_def_config_path

all_dts_files = []
all_dts_files.append(os.path.basename(root_dts))

def find_all_dts_files(file_name):
    # print "open: %s " % file_name
    os.chdir(root_dts_path)
    # print "Now current path : %s" % os.getcwd()
    file_name = os.path.basename(file_name)
    fp = open(file_name)
    while True:
        line = fp.readline()
        if line:
            if(line.find("#include \"") >= 0):
                dts_file = line.split("\"")[1]
                # print dts_file
                if (dts_file not in all_dts_files)  == True:
                    all_dts_files.append(dts_file)
                    # print "Add dts file: %s" % dts_file
                find_all_dts_files(line.split("\"")[1])
        else:
            break
    # print "close: %s " % file_name
    fp.close()

def make_dir(path):
    is_exists=os.path.exists(path)
    if not is_exists:
        os.mkdir(path)

def copy_file(srcfile, dstfile):
    #print "srcfile:%s dstfile:%s " % (srcfile, dstfile)
    if not os.path.isfile(srcfile):
        print "%s not exist!" % (srcfile)
    else:
        fpath,fname=os.path.split(dstfile)
        shutil.copyfile(srcfile,dstfile)

#1. copy dts files
find_all_dts_files(root_dts)
#print "current path : %s" % os.getcwd()
make_dir(pro_dts_path)
print "find %d dts files: %s " % (len(all_dts_files), all_dts_files)
for file in all_dts_files:
    copy_file(file, pro_dts_path+"/"+file)

#2. copy def config file
os.chdir(root_def_config_path)
copy_file(os.path.basename(root_def_config), root_def_config_path+"/"+project_name+"_defconfig")
copy_file(os.path.basename(root_def_config).split('_')[0] + "-perf_defconfig", root_def_config_path+"/"+project_name+"-perf_defconfig")
#print os.path.basename(root_def_config).split('_')[0] + "-perf_defconfig"

