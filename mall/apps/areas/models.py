from django.db import models


# 暂时理解为 省
class Area(models.Model):
    """
    行政区划
    """
    name = models.CharField(max_length=20, verbose_name='名称')
    # related_name='' 可以修改关联模型属性的默认名字,默认名字是 '关联模型类名小写_set'
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True,
                               verbose_name='上级行政区划')

    # 市的信息
    # area_set = [Area,Area]
    class Meta:
        db_table = 'tb_areas'
        verbose_name = '行政区划'
        verbose_name_plural = '行政区划'

    def __str__(self):
        return self.name
