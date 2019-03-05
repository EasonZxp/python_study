#!/usr/bin/env python
# coding=utf-8

import os,shutil,sys,getopt

ds1 = {"name":"", "dts":"","config":""}
all_dts_files = []

def usage():
    print "="*140
    print "Usage: copy_dts_and_defconfig [--name PROJECT_NAME] [--dts ROOT_DTS] [--config DEF_CONFIG]"
    print "    or copy_dts_and_defconfig [-n PROJECT_NAME] [-d ROOT_DTS] [-c DEF_CONFIG]"
    print "\nExamples:"
    print "   copy_dts_and_defconfig --name cm01 --dts arch/arm/boot/dts/qcom/sdm450-mtp.dts --config arch/arm64/configs/msmcortex_defconfig"
    print "or copy_dts_and_defconfig -n cm01 -d arch/arm/boot/dts/qcom/sdm450-mtp.dts -c arch/arm64/configs/msmcortex_defconfig"
    print "\nMain operation mode:\n"
    print "  -h,  --help        read usage"
    print "  -n,  --name        set project name"
    print "  -d,  --dts         set based root dts file path"
    print "  -c,  --config      set based root def config file path"
    print "\n"
    sys.exit(-1)

def find_all_dts_files(based_dts_name):
    fp = open(based_dts_name)
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
    fp.close()

def make_dir(path):
    is_exists=os.path.exists(path)
    if not is_exists:
        os.mkdir(path)

def copy_file(srcfile, dstfile):
    # print "srcfile:%s dstfile:%s " % (srcfile, dstfile)
    if not os.path.isfile(srcfile):
        print "%s not exist!" % (srcfile)
    else:
        fpath,fname=os.path.split(dstfile)
        shutil.copyfile(srcfile,dstfile)

def parse_options(argv, ds1):
    strings = "hn:d:c:"
    lists = ["help", "name=", "dts=", "config="]

    try:
        opts,args = getopt.getopt(argv, strings, lists)
    except getopt.GetoptError, err:
        usage()
    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-n", "--name"):
            ds1["name"] = a
        elif o in ("-d", "--dts"):
            ds1["dts"] = a
        elif o in ("-c", "--config"):
            ds1["config"] = a
        else:usage()

if __name__ == '__main__':
    parse_options(sys.argv[1:], ds1)

    orig_path = os.getcwd()
    based_dts_path = os.path.dirname(ds1["dts"])
    based_dts_name = os.path.basename(ds1["dts"])
    all_dts_files.append(based_dts_name)
    os.chdir(based_dts_path)
    find_all_dts_files(based_dts_name)

    os.chdir(orig_path)
    pro_dts_path = based_dts_path + "/../" + ds1["name"]
    make_dir(pro_dts_path)

    #print "find %d dts files: %s " % (len(all_dts_files), all_dts_files)
    for file in all_dts_files:
        copy_file(based_dts_path + "/" + file, pro_dts_path + "/" + file)

    based_config_path = os.path.dirname(ds1["config"])
    based_config_name = os.path.basename(ds1["config"])
    project_name = ds1["name"]
    os.chdir(based_config_path)
    eng_config_suffix = "_defconfig"
    user_config_suffix = "-perf_defconfig"
    copy_file(based_config_name, project_name + eng_config_suffix)
    copy_file(based_config_name.split('_')[0] + user_config_suffix, project_name + user_config_suffix)
