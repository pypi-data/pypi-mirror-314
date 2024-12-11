from django.db import models
from django.core.exceptions import ValidationError

class Fileupload(models.Model):
    keystring = models.CharField(max_length=10, blank=True )
    Name = models.FileField(upload_to='upload/')    

def valid_date(value):
    val=value.split("/")
    if len(val)==3:
        if int(val[0]) in range(1300,1500):
            if int(val[1]) in range(1,7) and int(val[2]) in range(1,32):
                return value
            if int(val[1]) in range(7,13) and int(val[2]) in range(1,31):
                return value
    raise ValidationError("فرمت تاریخ درست نیست!")
'''
class StateType(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class PassType(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name
'''
class User1(models.Model):
	name = models.CharField(max_length=100 ,verbose_name='نام و نام خانوادگی')
	fathername = models.CharField(max_length=30,verbose_name='نام پدر')
	personeli = models.CharField(max_length=20,unique=True,verbose_name='شماره پرسنلی')
	etebar = models.CharField(max_length=10,validators=[valid_date] ,verbose_name='تاريخ اعتبار')
	melli = models.CharField(max_length=10,unique=True,verbose_name='کد ملی')
	pic = models.ImageField(upload_to='images/', blank=True, null=True ,verbose_name='تصویر')
	shenasname = models.CharField(max_length=10,verbose_name='شماره شناسنامه')
	postal = models.CharField(max_length=10,null=True,blank=True,verbose_name='کدپستی')
	position = models.CharField(max_length=30,null=True,blank=True,verbose_name='محل کار')
	gharardad = models.CharField(max_length=20,null=True,blank=True,verbose_name='نوع قرارداد')
	address = models.TextField(null=True,blank=True,verbose_name='آدرس')
	reserv1 = models.CharField(max_length=30,null=True,blank=True,verbose_name='')
	reserv2 = models.CharField(max_length=30,null=True,blank=True,verbose_name='')
	reserv3 = models.CharField(max_length=30,null=True,blank=True,verbose_name='')
	reserv4 = models.TextField(null=True,blank=True,verbose_name='توضیحات')
	
	def __str__(self):
	    return self.name
		
