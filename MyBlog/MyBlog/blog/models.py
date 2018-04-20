from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.conf import settings
# Create your models here.
from taggit.managers import TaggableManager
from django.contrib.auth.models import User

#个人日记
class ckeditorBlog(models.Model):
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=False)
    STAUTS_CHOICES=(
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=False)
    title = models.CharField(max_length=50, verbose_name="标题")
    content = RichTextUploadingField(blank=True, null=True, verbose_name="内容")
    click_counts = models.IntegerField(default=0)
    status = models.CharField(max_length=10,
                               choices=STAUTS_CHOICES,
                               default='draft')
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    first_image = models.ImageField('first_images/',blank=True,null=True)

    def __str__(self):
        return self.title

#相册
class MyPhoto(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=False)
    name = models.CharField(max_length=50)
    imge = models.ImageField(upload_to='photos/')
    content = models.CharField(max_length=500,blank=True,null=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

#技术文章
class technicalArticle(models.Model):
    user = models.ForeignKey(User,on_delete=False)
    name = models.CharField(max_length=50)
    share = models.TextField()
    content = models.TextField(blank=True,null=True)
    tag = TaggableManager()
    taggings = models.CharField(max_length=20,default='blog')
    click_counts = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

#扩展用户模型
class user_profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=False)
    content = RichTextUploadingField()
    photo = models.ImageField('myPhoto/')
    birth = models.DateField(blank=True,null=True)
    phone = models.CharField(max_length=11)
    qq = models.CharField(max_length=20)
    workstate = models.CharField(max_length=20)
    hobby = models.TextField()

    def __str__(self):
        return self.qq

#学习笔记(该处写的太繁琐！！！)
class studyNote(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )
    user = models.ForeignKey(User,on_delete=False)
    title = models.CharField(max_length=50)
    content = RichTextUploadingField(blank=True, null=True, verbose_name="内容")
    status = models.CharField(max_length=10,
                               choices=STATUS_CHOICES,
                               default='draft')
    tag = TaggableManager()
    click_counts = models.IntegerField(default=0)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    first_image = models.ImageField('first_images/',blank=True,null=True)

    def __str__(self):
        return self.title