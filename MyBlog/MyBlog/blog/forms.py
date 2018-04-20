from django import forms
#
# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)
from blog.models import technicalArticle, studyNote
from .models import ckeditorBlog,MyPhoto


class ckeditorForm(forms.ModelForm):
    class Meta:
        model = ckeditorBlog
        fields = ('title','content','click_counts','status')

class MyPhotoForm(forms.ModelForm):
    class Meta:
        model = MyPhoto
        fields = ('name','imge','content')

class technicalArticleForm(forms.ModelForm):
    class Meta:
        model = technicalArticle
        fields = ('name','share','content','taggings')

class studyNoteForm(forms.ModelForm):
    class Meta:
        model = studyNote
        fields = ('title','content','click_counts','status')
