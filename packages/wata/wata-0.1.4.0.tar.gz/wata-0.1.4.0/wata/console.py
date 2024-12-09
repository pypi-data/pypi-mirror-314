# from wata.pointcloud.pcd import PointCloudProcess
#
# import os
# from tabulate import tabulate
# from wata import obtain_wata_path
# import sys
# from pathlib import Path


# def wata_list(argv):
#     assert argv.__len__() == 2, 'error command'
#     table_list = [
#         ['终端命令', '功能'],
#         ['wata', 'Hello WATA !'],
#         ['wata show_kitti', '展示kitti数据集第一帧'],
#         ['wata list', '列出wata终端命令'],
#         ['wata install', '用清华源安装包'],
#         ['wata unzip', 'ubuntu解压文件'],
#         ['wata show_size', 'ubuntu查看子目录的大小'],
#         ['wata.lxq.yanhua', '打开烟花'],
#     ]
#     print(tabulate(table_list, headers='firstrow', tablefmt='grid'))


# def show_kitti(argv):
#     assert argv.__len__() == 2, 'error command'
#     cur_path = obtain_wata_path()
#     PointCloudProcess.show_pcd(os.path.join(cur_path, "resources/pcd/000000.bin"))
#
#
# def fireworks():
#     try:
#         from wata.lxq.fireworks_explosion import open_app as open_fireworks
#         cur_path = obtain_wata_path()
#         open_fireworks(ui=os.path.join(cur_path, "resources/fireworks/main.ui"),
#                        icon=os.path.join(cur_path, "resources/fireworks/icon.png"),
#                        snow=os.path.join(cur_path, "resources/fireworks/snow.gif"),
#                        emoji=os.path.join(cur_path, "resources/fireworks/paitou.gif"),
#                        fireworks=os.path.join(cur_path, "resources/fireworks/fireworks"))
#     except:
#         print("package err")


# def pip_install(argv):
#     assert argv.__len__() > 2
#     package = ''
#     len_pack = argv.__len__()
#     for i in range(2, len_pack):
#         package = package + argv[i] + ' '
#     print("pip install " + package + "-i https://pypi.tuna.tsinghua.edu.cn/simple/")
#     os.system("pip install " + package + "-i https://pypi.tuna.tsinghua.edu.cn/simple/")


# def unzip(argv):
#     user = '' if argv[1] == 'unzip' else 'sudo '
#     assert argv.__len__() > 2
#     zip_file = argv[2]
#     zip_ext = Path(zip_file).suffix[1:]
#     print(zip_ext)
#     if zip_ext == "zip":
#         print(user + "unzip " + zip_file)
#         os.system(user + "unzip " + zip_file)
#     elif zip_ext == "tar":
#         print(user + "tar -xvf " + zip_file)
#         os.system(user + "tar -xvf " + zip_file)
#     elif zip_ext == "tgz":
#         print(user + "tar -xzvf " + zip_file)
#         os.system(user + "tar -xzvf " + zip_file)
#     elif zip_file.split(".")[-1] == "gz" and zip_file.split(".")[-2] == "tar":
#         print(user + "tar -zxvf " + zip_file)
#         os.system(user + "tar -zxvf " + zip_file)
#     else:
#         print('Unable to decompress the file type temporarily')


# def wata_console():
#     if sys.argv.__len__() == 1:
#         print("Hello WATA !")
#         print('Enter "wata list" to view the function')
#         return None
#
#     cmd = sys.argv[1]
#     if cmd == 'install':
#         pip_install(sys.argv)
#         return None
#
#     elif cmd == 'unzip' or (cmd == 'sudo' and sys.argv[2] == 'unzip'):
#         unzip(sys.argv)
#         return None
#
#     elif cmd == 'list':
#         wata_list(sys.argv)
#         return None
#
#     elif cmd == 'show_kitti':
#         show_kitti(sys.argv)
#         return None
#
#     elif cmd == 'show_size':
#         os.system("sudo du -h --max-depth=1")
#         return None
#     else:
#         print("error command")
