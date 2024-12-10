'''
ftplib: https://docs.python.org/3.10/library/ftplib.html
'''
import os
from ftplib import FTP
from pathlib import Path


class XFTP:

    def __init__(self, host='127.0.0.1', port=21, username='anonymous', password='', encoding='UTF-8', debuglevel=0):
        ''' Initiation '''
        self.ftp = FTP()
        self.ftp.set_debuglevel(debuglevel)
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.encoding = encoding
        self.retry = 1

    def connect(self):
        ''' FTP connect '''
        try:
            self.ftp.connect(host=self.host, port=self.port, timeout=10)
            self.ftp.encoding = self.encoding
            self.ftp.login(user=self.username, passwd=self.password)
            print('FTP connect success')
            print('-' * 80)
            return True
        except Exception as e:
            print(f'FTP connect error: {e}, retry...')
            if self.retry >= 3:
                print('FTP connect faild')
                return False
            self.retry += 1
            self.connect()

    def close(self, info=None):
        ''' FTP close '''
        print(info) if info else None
        try:
            self.ftp.quit()
        except:
            self.ftp.close()
        print('-' * 80)
        print('FTP connect closed')

    def get_file_list(self, dir='/'):
        ''' Get file list '''
        self.chdir_to_remote(dir)
        return self.ftp.nlst()

    def get_file_size(self, dir='/', file=None):
        ''' Get file size '''
        self.chdir_to_remote(dir)
        return self.ftp.size(file)

    def mkdir(self, dir_string='/'):
        ''' 创建目录 (从 / 目录依次递增创建子目录. 如果目录存在, 创建目录时会报错, 所以这里忽略所有错误.) '''
        try:
            dir_list = dir_string.split("/")
            for i, _ in enumerate(dir_list):
                dir = '/'.join(dir_list[:i + 1])
                try:
                    self.ftp.mkd(dir)
                except:
                    pass
            return True
        except:
            return False

    def chdir_to_remote(self, dir='/'):
        ''' change to remote directory'''
        try:
            self.ftp.cwd(dir)
        except:
            self.close(f'Remote directory error: {dir}')

    def x_exit(self, info=None):
        ''' Exit '''
        print(info) if info else None
        # 注意: exit() 并不会退出脚本, 配合 try 使用
        exit()

    def x_exec(self, local_dir='.', local_file='', remote_dir='/', remote_file='', upload=False):
        ''' Download or Upload '''

        bufsize = 1024
        local_path = local_dir + '/' + local_file
        remote_path = remote_dir + '/' + remote_file
        info = 'Upload' if upload else 'Download'

        # 检查参数
        if upload:
            if local_file == '':
                self.close('Argument Miss: local file')
            # 如果没有设置 远程文件 名称, 则使用 本地文件 名称
            if remote_file == '':
                remote_file = local_file
                remote_path = remote_dir + '/' + remote_file
        else:
            if remote_file == '':
                self.close('Argument Miss: remote file')
            # 如果没有设置 本地文件 名称, 则使用 远程文件 名称
            if local_file == '':
                local_file = remote_file
                local_path = local_dir + '/' + local_file

        # 进入本地目录
        try:
            if upload:
                # 检查本地目录
                stat = Path(local_dir)
                self.close(f'Local directory error: {local_dir}') if stat.exists() == False else None
            else:
                # 创建本地目录
                Path(local_dir).mkdir(parents=True, exist_ok=True)
            # 进入本地目录
            os.chdir(local_dir)
        except:
            # 第一层 try 使用 self.x_exit() 无效, 直接使用 self.close()
            self.close(f'Local directory error: {local_dir}')

        # 上传或下载
        try:

            if upload:

                ''' 上传 '''

                # 创建远程目录
                if remote_dir != '/':
                    self.mkdir(remote_dir)

                # 进入远程目录
                self.chdir_to_remote(remote_dir)

                # 上传文件
                stat = Path(local_file)
                if stat.exists() and stat.is_file():
                    with open(local_file, 'rb') as fid:
                        self.ftp.storbinary(f'STOR {remote_file}', fid, bufsize)
                    print('{} success: {} -> {}'.format(info, local_path.replace('//', '/'), remote_path.replace('//', '/')))
                    return True
                else:
                    self.x_exit('{} error: {} is not exist'.format(info, local_path.replace('//', '/')))

            else:

                ''' 下载 '''

                # 进入远程目录
                self.chdir_to_remote(remote_dir)

                # 下载文件
                if remote_file in self.ftp.nlst():
                    with open(local_file, 'wb') as fid:
                        self.ftp.retrbinary(f'RETR {remote_file}', fid.write, bufsize)
                    print('{} success: {} -> {}'.format(info, remote_path.replace('//', '/'), local_path.replace('//', '/')))
                    return True
                else:
                    self.x_exit('{} error: {} is not exist'.format(info, remote_path.replace('//', '/')))

        except Exception as e:
            # 第一层 try 使用 self.x_exit() 无效, 直接使用 self.close()
            # self.close('{} faild! Please check {} or {}'.format(info, local_path, remote_path))
            self.close(f'{info} error: {e}')
            return False

    def handle_all(self, local_dir='.', remote_dir='/', upload=False):
        ''' Handle All '''
        if upload:
            # 检查本地目录
            stat = Path(local_dir)
            self.close(f'Local directory error: {local_dir}') if stat.exists() == False else None
            # 获取文件列表
            local_files = [f for f in os.listdir(local_dir) if os.path.isfile(os.path.join(local_dir, f))]
            for i in local_files:
                self.x_exec(local_dir=local_dir, remote_dir=remote_dir, local_file=i, upload=True)
        else:
            remote_files = self.get_file_list(remote_dir)
            for i in remote_files:
                self.x_exec(local_dir=local_dir, remote_dir=remote_dir, remote_file=i)

    def retrlines(self, remote_dir='/', cmd='LIST'):
        ''' Retrlines '''
        try:
            self.chdir_to_remote(remote_dir)
            print(self.ftp.retrlines(cmd))
            self.close()
        except Exception as e:
            # 第一层 try 使用 self.x_exit() 无效, 直接使用 self.close()
            self.close(e)
