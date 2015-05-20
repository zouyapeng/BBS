# --*-- encoding: utf-8 --*--
import json
from random import random
import uuid
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models.loading import get_model
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views import generic
from apps.account.models import AnswerVote, Thank, Focus, Favorite, Invite, History
from apps.article.models import Article
from apps.question.models import Question
from apps.tag.models import Tag
from apps.account.client import Client
from apps.account.models import User

client = Client(settings.CAS_SETTINGS["client_id"],
                    settings.CAS_SETTINGS["client_secret"],
                    settings.SIGNIN_BACK,
                    settings.CAS_SETTINGS["authorization_uri"],
                    settings.CAS_SETTINGS["token_uri"],
                    settings.CAS_SETTINGS["openid_uri"],
                    settings.CAS_SETTINGS["user_api_uri"])

class HomeView(generic.ListView):
    model = User
    template_name = "account/list.html"

def caslogin(request):
    uri = client.get_authorization_code_uri(scope="get_user_info get_user_group")
    return HttpResponseRedirect(uri)

def cas_get(request):
    code = request.GET.get('code')
    if code:
        openid = None
        try:
            token = client.get_token(code=code)
            error = token.get('error')
            if error:
                token = None
            else:
                openid = client.get_openid(token['access_token'])['openid']
                cas_user = client.get_user_info(token['access_token'],openid)
        except Exception as e:
            print e
            return HttpResponseRedirect(reverse("home"))
        if openid:
            try:
                user = User.objects.get(username=cas_user["username"])
                print user
            except ObjectDoesNotExist:
                user = User.objects.create_user(str(random()))
                user.username = cas_user["username"]
            user.openid = openid
            user.save()
        user = authenticate(openid = openid)
        # print openid,user
        if user:
            login(request,user)
            url = settings.HOME_PAGE
            return HttpResponseRedirect(url)

        return HttpResponseRedirect("account:login")

def Logout(request):
    if request.user.is_authenticated():
        try:
           logout_on_server(request)
        except Exception as e:
            pass
    return HttpResponseRedirect("/")


def logout_on_server(request):
    user = getattr(request, 'user', None)

    from django.contrib.auth.signals import user_logged_out

    if hasattr(user, 'is_authenticated') and not user.is_authenticated():
        user = None
    user_logged_out.send(sender=user.__class__, request=request, user=user)

    request.session.flush()
    if hasattr(request, 'user'):
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()

class RegisterView(generic.TemplateView):
    template_name = "account/register.html"

class LoginView(generic.TemplateView):
    template_name = "account/login.html"


class InviteView(generic.ListView):
    model = Invite
    template_name = "account/invite.html"
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(InviteView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        object_list = super(InviteView, self).get_queryset().filter(recipient=self.request.user)
        return object_list


class FavoriteView(generic.ListView):
    model = Favorite
    template_name = "account/favorite.html"
    content_types = []
    c_content_type = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(FavoriteView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.content_types = ContentType.objects.get_for_models(Question, Article).values()
        self.c_content_type = ContentType.objects.get_for_id(
            self.request.GET.get("content_type")) if self.request.GET.get("content_type") else self.content_types[0]
        object_list = super(FavoriteView, self).get_queryset().filter(content_type=self.c_content_type,
                                                                      user=self.request.user)

        return object_list

    def get_context_data(self, **kwargs):
        context = super(FavoriteView, self).get_context_data(**kwargs)
        context['content_types'] = self.content_types
        context['c_content_type'] = self.c_content_type
        return context


class SettingView(generic.TemplateView):
    template_name = "account/setting.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SettingView, self).dispatch(request, *args, **kwargs)

    def get_template_names(self):
        return "account/setting_%s.html" % self.kwargs.get("tag")

    def get_context_data(self, **kwargs):
        context = super(SettingView, self).get_context_data(**kwargs)
        context.update(self.kwargs)
        context['user'] = self.request.user
        return context


class UserDetailView(generic.DeleteView):
    model = get_model(settings.AUTH_USER_MODEL)
    slug_field = 'username'
    slug_url_kwarg = 'name'
    template_name = "account/detail.html"

    def get(self, request, *args, **kwargs):
        response = super(UserDetailView, self).get(request, *args, **kwargs)
        if self.object != request.user:
            History.generate_history(self.object, request)
        return response

    def get_template_names(self):
        if self.kwargs.get("tag"):
            return "account/detail_%s.html" % self.kwargs.get("tag")
        return self.template_name

    def get_context_data(self, **kwargs):

        context = super(UserDetailView, self).get_context_data(**kwargs)
        context.update(self.kwargs)
        context['vote_count'] = AnswerVote.objects.filter(user=self.object, agree=True).count()
        context['thank_count'] = Thank.objects.filter(user=self.object).count()
        # context['question_count'] = self.object.question_set.count()
        context['article_count'] = self.object.article_set.count()

        context['focus_users'] = Focus.objects.filter(
            content_type=ContentType.objects.get_for_model(get_model(settings.AUTH_USER_MODEL)), user=self.object)[:10]
        context['focus_user_count'] = Focus.objects.filter(
            content_type=ContentType.objects.get_for_model(get_model(settings.AUTH_USER_MODEL)), user=self.object).count()

        # context['focus_tags'] = Focus.objects.filter(content_type=ContentType.objects.get_for_model(Tag),
        #                                            user=self.object)[:10]
        # context['focus_tag_count'] = Focus.objects.filter(content_type=ContentType.objects.get_for_model(Tag),
        #                                            user=self.object).count()


        context['focus_users1'] = Focus.objects.filter(content_type=ContentType.objects.get_for_model(User),
                                                       object_id=self.object.id)

        if self.kwargs.get('tag') == 'question':
            context['questions'] = self.object.question_set.all().order_by('-last_answer_date').select_related("user")
        if self.kwargs.get('tag') == 'article':
            context['articles'] = self.object.article_set.all().order_by('-update_date').select_related("user")
        if self.kwargs.get('tag') == 'answer':
            if self.request.GET.get('tab') == 'answer':
                context['objects'] = self.object.answer_set.all().order_by('-created').select_related("question")
            else:
                context['objects'] = self.object.reply_set.all().order_by('-created').select_related("article")
        if self.kwargs.get('tag') == 'attention':
            tab = self.request.GET.get("tab", 'questions')
            if tab in ['questions', 'tags', 'articles', 'users']:
                objects = []
                # if tab == 'questions':
                #     objects = Focus.objects.filter(content_type=ContentType.objects.get_for_model(Question),
                #                                    user=self.object)
                # elif tab == 'tags':
                #     objects = Focus.objects.filter(content_type=ContentType.objects.get_for_model(Tag),
                #                                    user=self.object)
                if tab == 'articles':
                    objects = Focus.objects.filter(content_type=ContentType.objects.get_for_model(Article),
                                                   user=self.object)
                elif tab == 'users':
                    objects =  Focus.objects.filter(
            content_type=ContentType.objects.get_for_model(get_model(settings.AUTH_USER_MODEL)), user=self.object)
                    print objects
                context['objects'] = objects
                context['tab'] = tab
        return context