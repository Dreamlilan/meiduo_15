# 1.您的自定义存储系统必须是以下子类 django.core.files.storage.Storage：
from django.core.files.storage import Storage
from mall import settings


class MyStorage(Storage):
    # 2.Django必须能够在没有任何参数的情况下实例化您的存储系统
    # 这意味着任何设置都应该来自django.conf.settings
    def __init__(self,conf_path=None,ip=None):
        if not conf_path:
            conf_path = settings.FDFS_CLIENT_CONF
        self.conf_path = conf_path

        if not ip:
            ip = settings.FDFS_URL
        self.ip = ip

    # 3.您的存储类必须实现_open()和_save() 方法以及适用于您的存储类的任何其他方法
    def _open(self,name,mode='rb'):
        pass

    def _save(self,name,content,max_length=None):

        # 1.创建客户端的实例对象
        from fdfs_client.client import Fdfs_client
        client = Fdfs_client(self.conf_path)
        # 2.上传图片, read的读取的资源是二进制
        data = content.read()
        # upload_by_buffer 上传二进制
        # upload_by_buffer 会返回上传结果
        result = client.upload_appender_by_buffer(data)
        """
        {'Status': 'Upload successed.',
        'Uploaded size': '333.00KB',
        'Local file name': '/home/python/Pictures/snow.jpg',
        'Storage IP': '192.168.144.132',
        'Status': 'Upload successed.',
        'Group name': 'group1',
        'Remote file_id': 'group1/M00/00/00/wKiQglvrjeeAY2LvAAU3v5e9Wi8265.jpg'}
        """
        # 3.判断上传结果，获取file_id
        if result.get('Status') == 'Upload successed.':
            file_id = result.get('Remote file_id')
            return file_id
        else:
            raise Exception('上传失败')

    def exists(self, name):
        return False

    def url(self,name):

        # 默认这个 url 是返回name的值
        # name的值其实就是 file_id 的值

        # 我们访问图片的时候 真实的路径是 http://ip:port/ + file_id
        # 所以我们返回url的时候 就直接 把拼接好的url返回
        # return 'http://192.168.144.132:8888/' + name
        # return settings.FDFS_URL + name
        return self.ip + name




























