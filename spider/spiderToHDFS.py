import pyhdfs

class HDFS:
    def __init__(self, host, user_name):
        self.host = host
        self.user_name = user_name

    def get_conn(self):
        try:
            hdfs = pyhdfs.HdfsClient(hosts=self.host, user_name=self.user_name)
            return hdfs
        except pyhdfs.HdfsException as e:
            print("Error:%s" % e)

    # 返回指定目录下的所有文件
    def listdir(self, hdfs_path):
        try:
            client = self.get_conn()
            dirs = client.listdir(hdfs_path)
            for row in dirs:
                print(row)
        except pyhdfs.HdfsException as e:
            print("Error:%s" % e)

    # 返回用户的根目录
    def get_home_directory(self):
        try:
            client = self.get_conn()
            print(client.get_home_directory())
        except pyhdfs.HdfsException as e:
            print("Error:%s" % e)

    # 创建新目录
    def mkdirs(self, hdfs_path):
        try:
            client = self.get_conn()
            print(client.mkdirs(hdfs_path))
        except pyhdfs.HdfsException as e:
            print("Error:%s" % e)

    # 从集群上copy到本地
    def copy_to_local(self, hdfs_path, local_path):
        try:
            client = self.get_conn()
            client.copy_to_local(hdfs_path, local_path)
        except pyhdfs.HdfsException as e:
            print("Error:%s" % e)

    # 从本地上传文件至集群
    def copy_from_local(self, local_path, hdfs_path):
        try:
            client = self.get_conn()
            client.copy_from_local(local_path, hdfs_path)
        except pyhdfs.HdfsException as e:
            print("Error:%s" % e)

    # 查看文件内容
    def read_files(self, hdfs_path):
        try:
            client = self.get_conn()
            response = client.open(hdfs_path)
            print(response.read())
        except pyhdfs.HdfsException as e:
            print("Error:%s" % e)

    # 向一个已经存在的文件追加内容
    def append_files(self, hdfs_path, content):
        try:
            client = self.get_conn()
            print(client.append(hdfs_path, content))
        except pyhdfs.HdfsException as e:
            print("Error:%s" % e)

    # 查看是否存在文件
    def check_files(self, hdfs_path):
        try:
            client = self.get_conn()
            print(client.exists(hdfs_path))
        except pyhdfs.HdfsException as e:
            print("Error:%s" % e)

    # 删除文件
    def delete_files(self, hdfs_path):
        try:
            client = self.get_conn()
            print(client.delete(hdfs_path))
        except pyhdfs.HdfsException as e:
            print("Error:%s" % e)

if __name__ == '__main__':
    host = 'hadoop102:9870' #端口号
    username = 'akysa'  #用户名

    hdfsObj = HDFS(host, username)

    sight_path = '/travel_db/ods/ods_travel_sight_info/'  #HDFS景点数据文件存储路径
    comment_path = '/travel_db/ods/ods_travel_comment_info/'  #HDFS评论数据文件存储路径
    sight_file = './sight_data.csv'  #本地景点数据文件路径
    comment_file = './comment_data.csv'  #本地评论数据文件路径

    ods_travel_sight_info = 'ods_travel_sight_info.csv' #景点目标文件
    ods_travel_comment_info = 'ods_travel_comment_info.csv' #评论目标文件

    hdfsObj.copy_from_local(sight_file, sight_path + ods_travel_sight_info)
    hdfsObj.copy_from_local(comment_file, comment_path + ods_travel_comment_info)
