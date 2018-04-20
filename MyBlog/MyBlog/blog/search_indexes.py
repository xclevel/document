from haystack import indexes
from .models import ckeditorBlog,studyNote
import datetime

class ckeditorBlogIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True)
    # author = indexes.CharField(model_attr='user')
    # title = indexes.CharField(model_attr='title')
    def get_model(self):  # 重载get_model方法，必须要有！
        return ckeditorBlog

    '''一个常见的主题是允许管理员用户添加未来的内容，
    但不会在该网站上显示，直到达到未来的日期。
    我们指定一个自定义 index_queryset方法来防止将来的项目被索引'''
    # 重载index_..函数
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class studyNoteIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True)
    # author = indexes.CharField(model_attr='user')
    # title = indexes.CharField(model_attr='title')
    def get_model(self):  # 重载get_model方法，必须要有！
        return studyNote

    '''一个常见的主题是允许管理员用户添加未来的内容，
    但不会在该网站上显示，直到达到未来的日期。
    我们指定一个自定义 index_queryset方法来防止将来的项目被索引'''
    # 重载index_..函数
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()