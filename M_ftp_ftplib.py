#!/usr/bin/python3
# -*- coding: UTF-8 -*-

## propuse : upload or download files use M_ftplib, a modified python internal ftplib module to suit EPSV mode
## created : Shichao Xie 2021.9.6
## ref     : ftplib.py from Python, script by Ouyang Peng from CSDN:http://blog.csdn.net/ouyang_peng/article/details/79271113

#from ftplib import FTP
from M_ftplib import FTP
import os,re
import sys
import time
import socket

class MyFTP:
    """
        ftp自动下载、自动上传脚本，可以递归目录操作
        作者：欧阳鹏
        博客地址：http://blog.csdn.net/ouyang_peng/article/details/79271113
    """

    def __init__(self, host, log, port=21):
        """ 初始化 FTP 客户端
        参数:
                host:ip地址

                port:端口号
        """
        # print("__init__()---> host = %s ,port = %s" % (host, port))

        self.host = host
        self.port = port
        self.ftp = FTP()
        self.log = log
        # 重新设置下编码方式
        #self.ftp.encoding = 'gbk'
        self.log_file = open(self.log, "a")
        self.file_list = []

    def login(self, username, password):
        """ 初始化 FTP 客户端
            参数:
                username: 用户名

                password: 密码
        """
        try:
            timeout = 30.0
            socket.setdefaulttimeout(timeout)
            ## 0主动模式 1 #被动模式
            self.ftp.set_pasv(False)
            #EPSV mode
            self.ftp.set_epsv(True)
            # 打开调试级别2，显示详细信息
            #self.ftp.set_debuglevel(2)

            self.debug_print('connecting to %s ...' % self.host)
            self.ftp.connect(self.host, self.port)
            self.debug_print('Succesfully connected to  %s' % self.host)

            self.debug_print('Logging to %s ...' % self.host)
            self.ftp.login(username, password)
            #self.ftp.sendcmd("EPSV")
            self.debug_print('Succesfully Logged to %s' % self.host)

            self.debug_print(self.ftp.welcome)
        except Exception as err:
            self.deal_error("FTP connection or log in failed, Error: %s" % err)
            pass

    def is_same_size(self, local_file, remote_file):
        """判断远程文件和本地文件大小是否一致

            参数:
                local_file: 本地文件

                remote_file: 远程文件
        """
        try:
            remote_file_size = self.ftp.size(remote_file)
        except Exception as err:
            # self.debug_print("is_same_size() 错误描述为：%s" % err)
            remote_file_size = -1

        try:
            local_file_size = os.path.getsize(local_file)
        except Exception as err:
            # self.debug_print("is_same_size() 错误描述为：%s" % err)
            local_file_size = -1
        local_file_size = -1  if local_file_size == None else local_file_size
        remote_file_size = -1 if remote_file_size == None else remote_file_size
        self.debug_print('local_file_size:%d  , remote_file_size:%d' % (local_file_size, remote_file_size))
        if remote_file_size == local_file_size or remote_file_size == -1:
            return 1
        else:
            return 0

    def download_file(self, local_file, remote_file):
        """从ftp下载文件
            参数:
                local_file: 本地文件

                remote_file: 远程文件
        """
        self.debug_print("download_file()---> local_path = %s ,remote_path = %s" % (local_file, remote_file))

        if self.is_same_size(local_file, remote_file):
            self.debug_print('%s file size is same, no need to download' % local_file)
            return
        else:
            try:
                downloading = ''.join([local_file,"_downloading"])
                if os.path.exists(downloading):
                    self.debug_print('%s file is downloading by another ftp thread, no need to download' % local_file)
                    return
                else :
                    os.mknod(downloading)
                    self.debug_print('>>>>>>>>>>>>Downloading file %s ...' % local_file)
                    buf_size = 1024
                    file_handler = open(local_file, 'wb')
                    self.ftp.retrbinary('RETR %s' % remote_file, file_handler.write, buf_size)
                    file_handler.close()
                    os.remove(downloading)
            except Exception as err:
                self.debug_print('Download failed, Error: %s ' % err)
                return

    def download_file_tree(self, local_path, remote_path):
        """从远程目录下载多个文件到本地目录
                        参数:
                            local_path: 本地路径

                            remote_path: 远程路径
                """
        print("download_file_tree()--->  local_path = %s ,remote_path = %s" % (local_path, remote_path))
        try:
            self.ftp.cwd(remote_path)
        except Exception as err:
            self.debug_print('Remote path %s does not exist, continue...' % remote_path + ", Error: %s" % err)
            return

        if not os.path.isdir(local_path):
            self.debug_print('Local path %s does not exist, mkdir first' % local_path)
            os.makedirs(local_path)

        self.debug_print('Change directory to %s' % self.ftp.pwd())

        self.file_list = []
        # 方法回调
        self.ftp.dir(self.get_file_list)

        remote_names = self.file_list
        self.debug_print('Remote path List: %s' % remote_names)
        for item in remote_names:
            file_type = item[0]
            file_name = item[1]
            local = os.path.join(local_path, file_name)
            if file_type == 'd':
                print("download_file_tree()---> Download directory: %s" % file_name)
                self.download_file_tree(local, file_name)
                self.ftp.cwd("..")
                self.debug_print('back to father directory %s' % self.ftp.pwd())
            elif file_type == '-':
                print("download_file()---> Download file: %s" % file_name)
                self.download_file(local, file_name)
        return True

    def download_files_glob(self, local_path, remote_path,sfiles,sites):
        """从远程目录通过通配符下载多个文件到本地目录
                        参数:
                            local_path: 本地路径

                            remote_path: 远程路径
                """
        #remote_path = re.sub(remote_files.split("/")[-1],'',remote_files)
        print("download_file_tree()--->  local_path = %s ,remote_path = %s" % (local_path, remote_path))
        try:
            self.ftp.cwd(remote_path)
        except Exception as err:
            self.debug_print('Remote path %s does not exist, continue...' % remote_path + ", Error: %s" % err)
            return

        if not os.path.isdir(local_path):
            self.debug_print('Local path %s does not exist, mkdir first' % local_path)
            os.makedirs(local_path)

        self.debug_print('Change directory to %s' % self.ftp.pwd())

        self.file_list = []
        # 方法回调
        self.ftp.dir(self.get_file_list)

        remote_names = self.file_list
        #self.debug_print('Remote path List: %s' % remote_names)
        for item in remote_names:
            file_type = item[0]
            file_name = item[1]
            if len(sites) == 0:
                globb = re.sub("\?",r"\\S",sfiles)
                if re.match(globb,file_name):
                    local = os.path.join(local_path, file_name)
                    if file_type == 'd':
                        print("download_file_tree()---> Download directory: %s" % file_name)
                        self.download_file_tree(local, file_name)
                        self.ftp.cwd("..")
                        self.debug_print('back to father directory %s' % self.ftp.pwd())
                    elif file_type == '-':
                        print("download_file()---> Download file: %s" % file_name)
                        self.download_file(local, file_name)
            else :
                for site in sites :
                    if sfiles[0:9] == "?????????":
                        sfile_1 = re.sub(r"^\?{9}",str(site).upper()+"?????",sfiles,count=0,flags=0)
                    else :
                        sfile_1 = re.sub(r"^\?{4}",str(site).lower(),sfiles,count=0,flags=0)
                    globb = re.sub("\?",r"\\S",sfile_1)
                    if re.match(globb,file_name):
                        local = os.path.join(local_path, file_name)
                        if file_type == 'd':
                            print("download_file_tree()---> Download directory: %s" % file_name)
                            self.download_file_tree(local, file_name)
                            self.ftp.cwd("..")
                            self.debug_print('back to father directory %s' % self.ftp.pwd())
                        elif file_type == '-':
                            print("download_file()---> Download file: %s" % file_name)
                            self.download_file(local, file_name)
        return True

    def upload_file(self, local_file, remote_file):
        """从本地上传文件到ftp

            参数:
                local_path: 本地文件

                remote_path: 远程文件
        """
        if not os.path.isfile(local_file):
            self.debug_print('%s does not exist' % local_file)
            return

        if self.is_same_size(local_file, remote_file):
            self.debug_print('skip file already exist: %s' % local_file)
            return

        buf_size = 1024
        file_handler = open(local_file, 'rb')
        #self.ftp.sendcmd("EPSV")
        self.ftp.storbinary('STOR %s' % remote_file, file_handler, buf_size)
        file_handler.close()
        self.debug_print('Upload: %s' % local_file + "Succeed!")

    def upload_file_tree(self, local_path, remote_path):
        """从本地上传目录下多个文件到ftp
            参数:

                local_path: 本地路径

                remote_path: 远程路径
        """
        if not os.path.isdir(local_path):
            self.debug_print('Local path %s does not exits' % local_path)
            return
        """
        创建服务器目录
        """
        try:
            self.ftp.cwd(remote_path)  # 切换工作路径
        except Exception as e:
            base_dir, part_path = self.ftp.pwd(), remote_path.split('/')
            for p in part_path[1:-1]:
                base_dir = base_dir + p + '/'  # 拼接子目录
                try:
                    self.ftp.cwd(base_dir)  # 切换到子目录, 不存在则异常
                except Exception as e:
                    print('INFO:', e)
                    self.ftp.mkd(base_dir)  # 不存在创建当前子目录
        #self.ftp.cwd(remote_path)
        self.debug_print('Change to remote directory: %s' % self.ftp.pwd())

        local_name_list = os.listdir(local_path)
        self.debug_print('Local Directory list: %s' % local_name_list)
        #self.debug_print('判断是否有服务器目录: %s' % os.path.isdir())

        for local_name in local_name_list:
            src = os.path.join(local_path, local_name)
            print("src Path=========="+src)
            if os.path.isdir(src):
                try:
                    self.ftp.mkd(local_name)
                except Exception as err:
                    self.debug_print("Path already exist  %s , Error: %s" % (local_name, err))
                self.debug_print("upload_file_tree()---> Upload dir: %s" % local_name)
                self.debug_print("upload_file_tree()---> Upload src dir: %s" % src)
                self.upload_file_tree(src, local_name)
            else:
                self.debug_print("upload_file_tree()---> Upload file: %s" % local_name)
                self.upload_file(src, local_name)
        self.ftp.cwd("..")

    def close(self):
        """ 退出ftp
        """
        self.debug_print("close()---> FTP Exit")
        self.ftp.quit()
        self.log_file.close()

    def debug_print(self, s):
        """ 打印日志
        """
        self.write_log(s)

    def deal_error(self, e):
        """ 处理错误异常
            参数：
                e：异常
        """
        log_str = 'Error: %s' % e
        self.write_log(log_str)
        sys.exit()

    def write_log(self, log_str):
        """ 记录日志
            参数：
                log_str：日志
        """
        time_now = time.localtime()
        date_now = time.strftime('%Y-%m-%d', time_now)
        format_log_str = "%s ---> %s \n " % (date_now, log_str)
        print(format_log_str)
        self.log_file.write(format_log_str)

    def get_file_list(self, line):
        """ 获取文件列表
            参数：
                line：
        """
        file_arr = self.get_file_name(line)
        # 去除  . 和  ..
        if file_arr[1] not in ['.', '..']:
            self.file_list.append(file_arr)

    def get_file_name(self, line):
        """ 获取文件名
            参数：
                line：
        """
        pos = line.rfind(':')
        while (line[pos] != ' '):
            pos += 1
        while (line[pos] == ' '):
            pos += 1
        file_arr = [line[0], line[pos:]]
        return file_arr

def upload_for_chd_ac(host,username,password,log_file,local_dir,remote_dir):
    my_ftp = MyFTP(host,log_file)
    my_ftp.login(username,password)
    my_ftp.upload_file_tree(local_dir, remote_dir)
    my_ftp.close()

def ftp_down(host,username,password,log_file,local_dir,remote_dir,sites,sfile):
    os.chdir(local_dir)
    my_ftp = MyFTP(host,log_file)
    my_ftp.login(username,password)
    my_ftp.download_files_glob(local_dir, remote_dir,sfile,sites)
    my_ftp.close()
    return 0
