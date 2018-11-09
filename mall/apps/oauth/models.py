from django.db import models

# Create your models here.
from django.db import models
from utils.models import BaseModel

class OAuthQQUser(BaseModel):
    """
    QQ登录用户数据
    """
    """
    如果我们关联的外键的模型没有在本应用中
    需要使用 '子应用.模型类'
    如果不加子应用,默认会在本子应用中查找
    """
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户')
    openid = models.CharField(max_length=64, verbose_name='openid', db_index=True)

    class Meta:
        db_table = 'tb_oauth_qq'
        verbose_name = 'QQ登录用户数据'
        verbose_name_plural = verbose_name