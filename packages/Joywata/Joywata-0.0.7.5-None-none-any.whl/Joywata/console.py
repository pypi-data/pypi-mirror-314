import os
from tabulate import tabulate
import sys
from pathlib import Path
import os
from Joywata.images_filtering import manual_image_filtering_interface


def wata_list(argv):
    assert argv.__len__() == 2, 'error command'
    table_list = [
        ['终端命令', '功能'],
        ['wata', 'Hello JOYWATA !'],
        ['wata list', '列出wata终端命令'],
        ['wata install', '用清华源安装包'],
        ['wata uninstall', '卸载python包'],
        ['wata unzip', 'ubuntu解压文件'],
        ['wata show_size', 'ubuntu查看子目录的大小'],
        ['wata conda rm <env>', '删除conda中的env环境'],
        ['wata cuda list', '列出ubuntu系统中已安装的cuda版本'],
        ['wata tmux', '刷新tmux窗口'],
        ['wata show_img1', '弹出界面，展示和播放图片，可以进行人工筛选'],
    ]
    print(tabulate(table_list, headers='firstrow', tablefmt='grid'))


def pip_install_by_tsinghua(argv):
    assert argv.__len__() > 2

    package = ''
    len_pack = argv.__len__()
    for i in range(2, len_pack):
        package = package + argv[i] + ' '
    if argv[1] =="install":
        print("pip install "+ package + "-i https://pypi.tuna.tsinghua.edu.cn/simple/")
        os.system("pip install " + package + "-i https://pypi.tuna.tsinghua.edu.cn/simple/")
    elif argv[1] == "uninstall":
        print("pip uninstall " + package)
        os.system("pip uninstall " + package)


def conda_cmd(argv):
    
    assert argv.__len__() > 3
    if argv[2] == "rm":
        print("conda rm " + argv[-1] + " --all")
        os.system("conda remove -n " + argv[-1] + " --all")

def docker_cmd(argv):
    len_pack = argv.__len__()
    assert len_pack >= 3
    cmd =""
    
    if argv[2] == "rmc":
        for i in range(3, len_pack):
            cmd = cmd + argv[i] + ' '
        print("docker rm -f " + cmd)
        os.system("docker rm -f " + cmd)

    elif argv[2] == "attach":
        assert len_pack == 4
        print("docker start " + argv[3] + " && docker attach " + argv[3])
        os.system("docker start " + argv[-1] + " && docker attach " + argv[-1])

    elif argv[2] == "rungpu":
        os.system("bash " + os.path.dirname(os.path.abspath(__file__)) + "/dockercmd/docker_run_gpu.sh "+argv[3] +" "+argv[4])
    elif argv[2] == "runcpu":
        os.system("bash " + os.path.dirname(os.path.abspath(__file__)) + "/dockercmd/docker_run_cpu.sh "+argv[3] +" "+argv[4])

    elif argv[2] == "list":
        print("==>docker 镜像如下:")
        os.system("docker images")
        print("-------------------------------------------------------------------------")
        print("==>所有的docker容器如下:")
        os.system("docker ps -a")
        print("-------------------------------------------------------------------------")
        print("==>其中正在运行的docker容器如下:")
        os.system("docker ps")
        


def unzip(argv):
    user = '' if argv[1] == 'unzip' else 'sudo '
    assert argv.__len__() > 2
    zip_file = argv[2]
    zip_ext = Path(zip_file).suffix[1:]
    print(zip_ext)
    if zip_ext == "zip":
        print(user + "unzip " + zip_file)
        os.system(user + "unzip " + zip_file)
    elif zip_ext == "tar":
        print(user + "tar -xvf " + zip_file)
        os.system(user + "tar -xvf " + zip_file)
    elif zip_ext == "tgz":
        print(user + "tar -xzvf " + zip_file)
        os.system(user + "tar -xzvf " + zip_file)
    elif zip_file.split(".")[-1] == "gz" and zip_file.split(".")[-2] == "tar":
        print(user + "tar -zxvf " + zip_file)
        os.system(user + "tar -zxvf " + zip_file)
    elif zip_file.split(".")[-1] == "xz" and zip_file.split(".")[-2] == "tar":
        print(user + "tar -xvf " + zip_file)
        os.system(user + "tar -xvf " + zip_file)
    else:
        print('Unable to decompress the file type temporarily')

def wata_console():
    if sys.argv.__len__() == 1:
        print("Hello JOYWATA !")
        print('Enter "wata list" to view the function')
        return None

    cmd = sys.argv[1]
    if cmd == 'install' or cmd == 'uninstall':
        pip_install_by_tsinghua(sys.argv)
        return None

    if cmd == 'install' or cmd == 'uninstall':
        pip_install_by_tsinghua(sys.argv)
        return None

    elif cmd == 'unzip' or (cmd == 'sudo' and sys.argv[2] == 'unzip'):
        unzip(sys.argv)
        return None

    elif cmd == 'list':
        wata_list(sys.argv)
        return None

    elif cmd == 'show_size':
        os.system("sudo du -sh *")
        return None

    elif cmd == 'cuda':
        os.system("ls /usr/local/ | grep ^cuda-")
        return None

    elif cmd == 'conda':
        conda_cmd(sys.argv)
        return None

    elif cmd == 'tmux':
        os.system("tmux detach -a")
        return None

    elif cmd == 'docker':
        docker_cmd(sys.argv)
        return None
    
    elif cmd == 'show_img1':
        manual_image_filtering_interface()
        return None

    else:
        print("error command")


# def manual_image_filtering_interface():
#     manual_image_filtering_interface()


