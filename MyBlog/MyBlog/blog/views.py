from django.conf import settings
from django.contrib.admin.templatetags.admin_list import paginator_number
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Max
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet

from blog.forms import MyPhotoForm, technicalArticleForm, studyNoteForm
from blog.models import MyPhoto, technicalArticle, studyNote
from .forms import ckeditorForm
from django.contrib.auth.models import User
from .models import ckeditorBlog
from .models import user_profile
from taggit.models import Tag
import re
# Create your views here.


@login_required
def sucessLogin(request):
    return render(request,'registration/sucessLogin.html',{})

# 添加个人日志
@login_required
def ckeForm(request):
    user1 = get_object_or_404(User,id=request.user.id)
    if request.method == 'POST':
        form = ckeditorForm(request.POST)
        if form.is_valid():
            cke = form.save(commit=False)
            cke.user = user1
            cke.save()
            # 添加first_image
            myblog_image = ckeditorBlog.objects.filter(user_id=1).order_by('-create_time')[0]
            # for studyNote_image in studyNotes:
            if myblog_image.first_image == '':
                myblog_content = myblog_image.content
                power = r'src=.*? '
                # 需要再加一层判断是否有图像，若未匹配到，则默认图像为什么......
                image = re.findall(power, myblog_content)
                if len(image) >= 1:
                    image = image[0][5:-2]
                    if image[0:7] == '/media/':
                        image = image[6:]
                else:
                    image = '/uploads/xucheng.jpg'
                ckeditorBlog.objects.filter(id=myblog_image.id).update(first_image=image)
            return HttpResponseRedirect('/xc_Blog/sucessLogin')
    else:
        form = ckeditorForm()
    return render(request,'registration/cke.html',{'form':form})

# 查看个人日志
@login_required
def showMyBlog(request):
    MyBlog = ckeditorBlog.objects.all()
    object_list = MyBlog.filter(user_id=1).order_by('update_time')
    #分页
    paginator = Paginator(object_list,5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    # page1 = paginator.page(1)
    # print(page1)
    return render(request,'registration/showMyBlog.html',{'posts':posts})

#修改个人日志
@login_required
def update_MyBlog(request,blog_id):
    user1 = get_object_or_404(User,id=request.user.id)
    blog = ckeditorBlog.objects.filter(id=blog_id)
    create_time = ''
    for showBlog in blog:
        create_time = showBlog.create_time
    if request.method == 'POST':
        form = ckeditorForm(request.POST)
        if form.is_valid():
            cke = form.save(commit=False)
            cke.user = user1
            cke.id = blog_id
            cke.create_time = create_time
            cke.save()
            return HttpResponse('sucess')
    else:
        title = ''
        content = ''
        for value in blog:
            title = value.title
            content = value.content
        form = ckeditorForm({'title':title,'content':content})
    return render(request,'registration/cke_update.html',{'form':form,'blog':blog})

#删除日志
def del_Myblog(request,blog_id):
    ckeditorBlog.objects.filter(id=blog_id).delete()
    return HttpResponse('sucess')

#search
def search_blog(request):
    rs = request.GET['q']
    # print(rs)
    form = SearchForm(request.GET)
    res = form.search()
    # res = SearchQuerySet().models(ckeditorBlog).filter(content=rs).load_all()
    # print(res)
    # for i in posts:
    #     print(i)
    # print(posts)
    return render(request, 'search/search.html', {'res':res})
    # else:
    #     form = SearchForm()
    # return render(request,'search/search.html',{'form':form})

#上传照片
@login_required
def addPhotos(request):
    user1 = get_object_or_404(User,id=request.user.id)
    if request.method == 'POST':
        form = MyPhotoForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            rs = form.save(commit=False)
            rs.user=user1
            rs.save()
            return HttpResponse('sucess')
    else:
        form = MyPhotoForm()
    return render(request,'registration/addPhoto.html',{'form':form})

#展示照片
@login_required
def showPhotos(request):
    photos = MyPhoto.objects.filter(user_id=request.user.id)
    paginator = Paginator(photos,8)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,'registration/showphotos.html',{'photos':photos,'posts':posts})

#展示单独的照片
def showSinglePhoto(request,photo_id):
    photos = MyPhoto.objects.filter(id=photo_id)
    myPhotos = MyPhoto.objects.filter(user_id=request.user.id).order_by('create_time')
    counts = 0
    for myPhoto in myPhotos:
        counts += 1
        if myPhoto.id == int(photo_id):
            break
    paginator= Paginator(myPhotos,1)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(counts)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,'registration/showSinglePhoto.html',{'photos':photos,'posts':posts})

#上传技术文档链接
def uploadTechnicalArticle(request):
    user = get_object_or_404(User,id=request.user.id)
    if request.method == 'POST':
        form = technicalArticleForm(request.POST)
        tags = request.POST['taggings']
        if form.is_valid():
            technicalArticle = form.save(commit=False)
            technicalArticle.user = user
            technicalArticle.save()
            technicalArticle.tag.add(tags)
            return HttpResponse('sucess')
    else:
        form = technicalArticleForm()
    return render(request,'registration/TechnicalArticle.html',{'form':form})

#展示技术文章
def showTechnicalArticle(request,tag_sulg):

    technicalArticles = technicalArticle.objects.filter(user_id=request.user.id)
    # for article in technicalArticles1:
    #     a = article.tag.all()
    #     for b in a:
    #         print(b)
        # if tag_sulg in article.taggings:
        #     print('sucess')
    if tag_sulg != 'None':
        # t = get_object_or_404(Tag,slug=tag_sulg)
        technicalArticles = technicalArticle.objects.filter(taggings__contains=tag_sulg)
    return render(request,'registration/showTechnicalArticle.html',{'technicalArticles':technicalArticles})

#上传个人笔记
def addStudyNotes(request):
    user = get_object_or_404(User,id=request.user.id)
    if request.method == 'POST':
        form = studyNoteForm(data=request.POST)
        if form.is_valid():
            noteForm = form.save(commit=False)
            noteForm.user = user
            noteForm.save()
            # 添加first_image
            studyNote_image = studyNote.objects.filter(user_id=1).order_by('-create_time')[0]
            # for studyNote_image in studyNotes:
            if studyNote_image.first_image == '':
                studyNote_content = studyNote_image.content
                power = r'src=.*? '
                #需要再加一层判断是否有图像，若未匹配到，则默认图像为什么......
                image = re.findall(power,studyNote_content)
                if len(image)>=1:
                    image = image[0][5:-2]
                    if image[0:7] == '/media/':
                        image = image[6:]
                else:
                    image = '/uploads/xucheng.jpg'
                studyNote.objects.filter(id=studyNote_image.id).update(first_image=image)
            return HttpResponseRedirect('/xc_Blog/sucessLogin')
    else:
        form = studyNoteForm()
    return render(request,'registration/addStudyNotes.html',{'form':form})

#查看个人笔记
def showStudyNotes(request):
    user = get_object_or_404(User,id=request.user.id)
    studyNotes = studyNote.objects.all()
    paginator = Paginator(studyNotes,5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,'registration/showStudyNotes.html',{'studyNotes':studyNotes,
                                                              'posts':posts})

#修改个人笔记

#删除个人笔记



#测试
def test(request):
    return render(request,'web/index.html',{})

#网站首页
def index_studyNote(request):
    user = get_object_or_404(User,id=1)
    user_profiles = user_profile.objects.filter(user_id=1)
    studyNotes = studyNote.objects.filter(user_id=1).order_by('-create_time')
    studyNotePublished = studyNote.objects.filter(user_id=1,status='published')
    #展示图片,这段加入提交中，此处设置会造成初始访问报错
    for studyNote_image in studyNotes:
        if studyNote_image.first_image == '':
            studyNote_content = studyNote_image.content
            power = r'src=.*? '
            #需要再加一层判断是否有图像，若未匹配到，则默认图像为什么......
            image = re.findall(power,studyNote_content)
            if len(image)>=1:
                image = image[0][5:-2]
                if image[0:7] == '/media/':
                    image = image[6:]
            else:
                image = '/uploads/xucheng.jpg'
            studyNotes.filter(id=studyNote_image.id).update(first_image=image)
    #点击排行
    studyNote_clickCounts = studyNote.objects.order_by('-click_counts','-create_time')[0:12]
    myBlog_clickCounts = ckeditorBlog.objects.order_by('-click_counts','-create_time')[0:12]
    click_rank = []
    for i in studyNote_clickCounts:
        click_rank.append(i)
    for i in myBlog_clickCounts:
        click_rank.append(i)
    for i in range(len(click_rank)-1):
        for j in range(len(click_rank)-1-i):
            if click_rank[j].click_counts < click_rank[j+1].click_counts:
                click_rank[j],click_rank[j+1] = click_rank[j+1],click_rank[j]
    # count = 0
    # rs = []
    # for studyNote_clickCount in studyNote_clickCounts:
    #     for myBlog_clickCount in myBlog_clickCounts:
    #         if studyNote_clickCount.click_counts >= myBlog_clickCount.click_counts:
    #             rs.append(studyNote_clickCount.click_counts)
    #             count += 1
    #             if count>=12 :
    #                 break
    #         else:
    #             rs.append(myBlog_clickCount.click_counts)
    #             count += 1



    # c = max(studyNote_clickCount.click_counts,myBlog_clickCount.click_counts)
    # print(c)
    #得到2个对象所有的内容
    myBlog = ckeditorBlog.objects.filter(user_id=1).order_by('-create_time')
    # for i in click_rank:
    #     if i in myBlog:
    #         print('sucess')
    context = {'studyNotes':studyNotes,'user':user,
               'user_profiles':user_profiles,'studyNotePublished':studyNotePublished,'click_rank':click_rank,'myBlog':myBlog}
    return render(request,'web/index.html',context)

#about_introduction
def introductionMe(request):
    user = user_profile.objects.filter(user_id=1)
    return render(request,'web/about.html',{'user':user})

#about_MyPhoto
def showMyPhoto(request):
    myphotos = MyPhoto.objects.filter(user_id=1)
    paginator = Paginator(myphotos,8)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,'web/listpic.html',{'posts':posts,'myphotos':myphotos})

#展示单独的照片
def showSinglePhoto_index(request,photo_id):
    photos = MyPhoto.objects.filter(id=photo_id)
    myPhotos = MyPhoto.objects.filter(user_id=request.user.id).order_by('create_time')
    counts = 0
    for myPhoto in myPhotos:
        counts += 1
        if myPhoto.id == int(photo_id):
            break
    paginator= Paginator(myPhotos,1)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(counts)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,'web/showSinglePhoto.html',{'photos':photos,'posts':posts})

#展示个人日志
def showDiary(request):
    diarys = ckeditorBlog.objects.filter(user_id=1).order_by('-create_time')
    paginator = Paginator(diarys,6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'diarys':diarys,'posts':posts}
    return render(request,'web/diary.html',context)

#展示技术文章
def showTechnicalArticles(request):
    studyNotes = studyNote.objects.filter(user_id=1).order_by('-create_time')
    paginator = Paginator(studyNotes,6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'posts':posts}
    return render(request,'web/technicalAtricle.html',context)

#展示博客文章内容
def showSingleArticle(request,article_id,obj):
    # post = studyNote.objects.filter(user_id=1,id=article_id)
    # post = get_object_or_404(studyNote,id=article_id)
    studyNotes_list,after_posts,before_posts = None,None,None
    count,click_counts = 0,0
    if obj == 'studyNote':
        studyNotes_list = studyNote.objects.filter(user_id=1).order_by('-create_time')
    if obj == 'ckeditorBlog':
        studyNotes_list = ckeditorBlog.objects.filter(user_id=1).order_by('-create_time')
    for note in studyNotes_list:
        count += 1
        if note.id == int(article_id):
            break
    paginator = Paginator(studyNotes_list,1)
    page = request.GET.get('page')
    if page is not None:
        page = int(page)
    try:
        if page == 1:
            posts = paginator.page(1)
            before_posts = None
            after_posts = paginator.page(page+1)
        elif page == paginator.num_pages:
            posts = paginator.page(paginator.num_pages)
            before_posts = paginator.page(page-1)
            after_posts = None
        else:
            posts = paginator.page(page)
            before_posts = paginator.page(page-1)
            after_posts = paginator.page(page+1)
    except PageNotAnInteger:
        posts = paginator.page(count)
        if count == 1:
            before_posts = None
            after_posts = paginator.page(count+1)
        elif count == paginator.num_pages:
            before_posts = paginator.page(count-1)
            after_posts = None
        else:
            before_posts = paginator.page(count-1)
            after_posts = paginator.page(count + 1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        before_posts = paginator.page(paginator.num_pages-1)
        after_posts = None
    for i in posts:
        click_counts = studyNotes_list.get(id=i.id).click_counts
        studyNotes_list.filter(id=i.id).update(click_counts=click_counts+1)
    context = {'posts':posts,'before_posts':before_posts,'after_posts':after_posts}
    return render(request,'web/showSingleBlog.html',context)

#展示日志

#全文搜索@search
def search_all(request):
    rs = request.GET.get('q',False)
    form = SearchForm(request.GET)
    searchResult = form.search()
    # print(searchResult.query)
    # for i in posts:
    #     print(i.object.title)
    paginator = Paginator(searchResult,6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    studyNotes = studyNote.objects.all()
    ckeditorBlogs = ckeditorBlog.objects.all()
    return render(request, 'search/search_result.html', {'posts':posts,'rs':rs,
                                                         'studyNotes':studyNotes,'ckeditorBlogs':ckeditorBlogs})

#全文搜索结果展示
def show_searchResult(reuqest,obj):
    pass
































