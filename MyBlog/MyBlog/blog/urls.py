from django.conf.urls import url
from django.contrib.auth.views import login, logout

from blog.views import addStudyNotes,showStudyNotes
from .views import ckeForm,showMyBlog,update_MyBlog,del_Myblog,search_blog
from .views import addPhotos,showPhotos,showSinglePhoto
from .views import uploadTechnicalArticle,showTechnicalArticle
from .views import sucessLogin
from .views import index_studyNote,introductionMe,showMyPhoto,showDiary,showTechnicalArticles,showSingleArticle,search_all
from .views import test



urlpatterns = [
    url(r'^login/$',login,name='login'),
    url(r'^sucessLogin/',sucessLogin,name='sucessLogin'),
    url(r'^logout/',logout,name='logout'),
    url(r'^ckeditorForm/',ckeForm,name='ckeditorForm'),
    url(r'^showMyBlog/',showMyBlog,name='showMyBlog'),
    url(r'^update_MyBlog/(?P<blog_id>\d+)/$',update_MyBlog,name='update_MyBlog'),
    url(r'^del_Myblog/(?P<blog_id>\d+)/',del_Myblog,name='del_Myblog'),
    url(r'^search_blog/',search_blog,name='search_blog'),
    url(r'^addPhoto',addPhotos,name='addPhotos'),
    url(r'^showPhotos/',showPhotos,name='showPhotos'),
    url(r'^showSinglePhoto/(?P<photo_id>\d+)/',showSinglePhoto,name='showSinglePhoto'),
    url(r'^uploadTechnicalArticle/',uploadTechnicalArticle,name='uploadTechnicalArticle'),
    url(r'^showTechnicalArticle/(?P<tag_sulg>\w+)/$',showTechnicalArticle,name='showTechnicalArticle'),
    url(r'^addStudyNotes/',addStudyNotes,name='addStudyNotes'),
    url(r'^showStudyNotes/',showStudyNotes,name='showStudyNotes'),
    url(r'^index/', index_studyNote, name='index_studyNote'),
    url(r'^about/',introductionMe,name='introduction'),
    url(r'^showMyPhoto/',showMyPhoto,name='showMyPhoto'),
    url(r'^showDiary',showDiary,name='showDiary'),
    url(r'^technical.html',showTechnicalArticles,name='showTechnicalArticles'),
    url(r'^showArticle/(?P<article_id>\d+)/(?P<obj>\w+)',showSingleArticle,name='showSingleArticle'),
    url(r'searchResult/',search_all,name='search_all'),
]
# (?P<user_id>\d+)/

