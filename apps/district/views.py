from django.views import generic
from apps.district.models import District
from apps.forum.models import Forum
from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.account.models import User
from apps.article.models import Article

def HomeView(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        users = User.objects.all()
        districts = District.objects.all()
        forums = Forum.objects.all()
        return render_to_response("district/home.html", locals(), context_instance=RequestContext(request))