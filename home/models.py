from django.db import models

# Create your models here.

class Zhanhui(models.Model):
    name = models.CharField(verbose_name='公司名称',max_length=100,null=True,blank=True)
    phone = models.CharField(verbose_name='电话',null=True,blank=True,max_length=11)
    contact_name = models.CharField(verbose_name='联系人',max_length=100,null=True,blank=True)
    contact_phone = models.CharField(verbose_name='联系人电话',null=True,blank=True,max_length=11)
    city = models.CharField(verbose_name='城市',max_length=255, null=True, blank=True)
    address = models.CharField(verbose_name='地址',max_length=255,null=True,blank=True)
    we_chat = models.CharField(verbose_name='微信',max_length=50,null=True,blank=True)
    qq = models.CharField(verbose_name='qq',max_length=50,null=True,blank=True)
    email = models.EmailField(verbose_name='邮箱',null=False,blank=False)
    pay_way = models.CharField(max_length=30,verbose_name='支付方式',null=True,blank=True)
    pay_account = models.CharField(verbose_name='支付金额',null=True,blank=True,max_length=255)
    note = models.CharField(max_length=255,verbose_name="备注",null=True,blank=True)
    time = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    zhifubao = models.CharField(verbose_name='支付宝账号',max_length=50,blank=True,null=True)
    bank = models.CharField(verbose_name="开户银行",max_length=50,blank=True,null=True)
    kahao = models.IntegerField(verbose_name='卡号后五位',null=True,blank=True)
    status = models.IntegerField(verbose_name="收款状态",default=0)

    def __str__(self):
        return self.email
    class Meta:
        verbose_name = verbose_name_plural = '展会表'

