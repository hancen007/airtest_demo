import os
import shutil

class Commonfunction(object):

    def __init__(self):
        pass

    """查找air脚本"""
    def find_all_script(self,path):
        A = []
        files = os.listdir(path)
        for f1 in files:
            tmp_path = os.path.join(path, f1)
            if not os.path.isdir(tmp_path):
                pass
            else:
                if (tmp_path.endswith('.air')):
                    A.append(tmp_path)
                else:
                    self.find_all_script(tmp_path)
        return A



    def get_last_floder(self,path):
        return os.path.basename(path)

    # 返回传来文件上级目录
    def get_parent_path(self,path):
        os.chdir(path + "/" + os.pardir)
        return os.getcwd()

    # 删除文件夹或文件
    def del_folder_or_file(self,path):
        if os.path.isfile(path):
            if os.path.exists(path):
                os.remove(path)
            else:
                print(path + "文件不存在...")
        else:
            if os.path.exists(path):
                shutil.rmtree(path)
            else:
                print(path + "路径不存在...")

    def create_folder(self,path):
        folder = os.path.exists(path)
        if folder:
            self.del_folder_or_file(path)
        os.mkdir(path)