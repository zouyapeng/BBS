# -*- coding: utf-8 -*-
from datetime import timedelta
import re

from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.template import resolve_variable, VariableDoesNotExist, Context, Node, Variable
from django.utils import dateformat
from django.utils.timezone import now as tznow
from apps.account.models import Favorite, Focus, Thank, AnswerVote, Accuracy, History, Comment
from util import summary
from django.template import RequestContext, loader

try:
    import pytils

    pytils_enabled = True
except ImportError:
    pytils_enabled = False

register = template.Library()


@register.tag
def wenda_time(parser, token):
    try:
        tag, context_time = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('wenda_time requires single argument')
    else:
        return WenDaTimeNode(context_time)


class WenDaTimeNode(template.Node):
    def __init__(self, time):
        self.time = template.Variable(time)

    def render(self, context):
        try:
            context_time = self.time.resolve(context)
        except VariableDoesNotExist:
            context_time = None
        if not context_time:
            return ''
        delta = tznow() - context_time
        today = tznow().replace(hour=0, minute=0, second=0)
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)

        if delta.days == 0:
            if delta.seconds < 60:
                if context['LANGUAGE_CODE'].startswith('ru') and pytils_enabled:
                    msg = '几秒钟前，几秒钟前，秒前'
                    msg = pytils.numeral.choose_plural(delta.seconds, msg)
                else:
                    msg = '秒前'
                return '%d %s' % (delta.seconds, msg)

            elif delta.seconds < 3600:
                minutes = int(delta.seconds / 60)
                if context['LANGUAGE_CODE'].startswith('ru') and pytils_enabled:
                    msg = '分钟前,分钟,分钟前'
                    msg = pytils.numeral.choose_plural(minutes, msg)
                else:
                    msg = '分钟前'
                return '%d %s' % (minutes, msg)
        if today < context_time < tomorrow:
            return '今天, %s' % context_time.strftime('%H:%M')
        elif yesterday < context_time < today:
            return '昨天, %s' % context_time.strftime('%H:%M')
        else:
            return dateformat.format(context_time, 'Y-m-d  H:i')


@register.tag
def favorite(parser, token):
    try:
        tag, obj = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('wenda_time requires single argument')
    else:
        return FavoriteNode(obj)


class FavoriteNode(template.Node):
    def __init__(self, obj):
        self.obj = template.Variable(obj)

    def render(self, context):
        try:
            request = context['request']
            if not request.user.is_authenticated():
                return ''
            obj = self.obj.resolve(context)

            content_type = ContentType.objects.get_for_model(obj)

            resource_url = reverse('api_dispatch_detail',
                                   kwargs={"resource_name": content_type.model, "api_name": content_type.app_label, "pk": obj.id})
            exists = Favorite.objects.filter(object_id=obj.id, content_type=content_type, user=request.user).exists()

            return "<button type=\"button\" data-content_object='{resource_url}'  " \
                   "class='btn btn-link favorite_tag {exists}'><i class='fa fa-star-o'></i> <span>{cancel}收藏</span></button>".format(
                resource_url=resource_url,
                cancel=exists and '取消' or '', exists=exists and "exists" or '')
        except Exception as e:
            print e
        return ''


@register.tag
def focus(parser, token):
    try:
        tag, obj = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('wenda_time requires single argument')
    else:
        return FocusNode(obj)


class FocusNode(template.Node):
    def __init__(self, obj):
        self.obj = template.Variable(obj)

    def render(self, context):
        try:
            request = context['request']
            obj = self.obj.resolve(context)
            content_type = ContentType.objects.get_for_model(obj)
            resource_url = reverse('api_dispatch_detail',
                                   kwargs={"resource_name": content_type.model, "api_name": content_type.app_label,
                                           "pk": obj.id})
            focus = Focus.objects.filter(object_id=obj.id, content_type=content_type)
            kw = {
                "resource_url": resource_url,
                "count": focus.count(),
                "disabled": 'disabled',
                'cancel': '',
                'exists': ''
            }
            if request.user.is_authenticated():
                exists = focus.filter(user=request.user).exists()
                kw.update({
                    "cancel": exists and '取消' or '',
                    "exists": exists and 'exists' or '',
                    'disabled': ''
                })
                if isinstance(obj, request.user.__class__)and obj == request.user:
                    kw['disabled'] = 'disabled'
            return "<button type=\"button\" {disabled} data-content_object='{resource_url}'  " \
                   "class='btn btn-sm btn-success focus_tag {exists}'><span>{cancel}关注</span>  <em>|</em> <b class='count'>{count}</b></button>".format(
                **kw)
        except Exception as e:
            print e
        return ''


@register.tag
def thank(parser, token):
    try:
        tag, obj = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('wenda_time requires single argument')
    else:
        return ThankNode(obj)


class ThankNode(template.Node):
    def __init__(self, obj):
        self.obj = template.Variable(obj)

    def render(self, context):
        try:
            request = context['request']
            if not request.user.is_authenticated():
                return ''
            obj = self.obj.resolve(context)

            content_type = ContentType.objects.get_for_model(obj)

            resource_url = reverse('api_dispatch_detail',
                                   kwargs={"resource_name": content_type.model,
                                           "api_name": content_type.app_label,
                                           "pk": obj.id})
            exists = Thank.objects.filter(object_id=obj.id, content_type=content_type, user=request.user).exists()
            return "<button type=\"button\" data-content_object='{resource_url}' " \
                   "class='btn btn-link thank_tag {exists}'><i class='fa fa-heart-o'></i> <span>{cancel}感谢</span></button>".format(
                resource_url=resource_url,
                cancel=exists and '取消' or '', exists=exists and "exists" or '')
        except:
            pass
        return ''


@register.tag
def accuracy(parser, token):
    try:
        tag, obj = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('wenda_time requires single argument')
    else:
        return AccuracyNode(obj)


class AccuracyNode(template.Node):
    def __init__(self, obj):
        self.obj = template.Variable(obj)

    def render(self, context):
        try:
            obj = self.obj.resolve(context)

            content_type = ContentType.objects.get_for_model(obj)
            request = context['request']
            if not request.user.is_authenticated():
                return ''
            resource_url = reverse('api_dispatch_detail',
                                   kwargs={"resource_name": content_type.model, "api_name": content_type.app_label,
                                           "pk": obj.id})
            exists = Accuracy.objects.filter(object_id=obj.id, content_type=content_type, user=request.user).exists()
            return "<button type=\"button\" data-content_object='{resource_url}' " \
                   "data-toggle=\"tooltip\" data-container=\"body\" data-placement=\"bottom\" title=\"这是没有价值的答案\" " \
                   "class='btn btn-link accuracy_tag {exists}'><i class='fa fa-user-times'></i> <span>{cancel}不是答案</span></button>".format(
                resource_url=resource_url,
                cancel=exists and '取消' or '', exists=exists and "exists" or '')
        except:
            pass
        return ''


@register.tag
def answer_vote(parser, token):
    try:
        tag, obj = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('wenda_time requires single argument')
    else:
        return AnswerVoteNode(obj)


class AnswerVoteNode(template.Node):
    def __init__(self, obj):
        self.obj = template.Variable(obj)

    def render(self, context):
        try:
            request = context['request']
            obj = self.obj.resolve(context)

            content_type = ContentType.objects.get_for_model(obj)

            resource_url = reverse('api_dispatch_detail',
                                   kwargs={"resource_name": content_type.model, "api_name": content_type.app_label,
                                           "pk": obj.id})
            agree = None
            disabled = 'disabled'
            if request.user.is_authenticated():
                answer_vote = AnswerVote.objects.filter(object_id=obj.id, content_type=content_type, user=request.user)
                if answer_vote.exists():
                    answer_vote = answer_vote[0]
                    agree = answer_vote.agree
                disabled = ''
            avs = AnswerVote.objects.filter(object_id=obj.id, content_type=content_type)
            if content_type.app_label == 'article':
                return "<button type='button' {disabled} data-value='1' data-content_object='{resource_url}'" \
                       "class='btn btn-default {active1} vote_tag'><i class='fa fa-thumbs-up'></i> <span>{active1_count}</span></button>" \
                       "<button {disabled} type='button' data-value='0' data-content_object='{resource_url}' class='btn btn-default {active2} vote_tag'><i class='fa fa-thumbs-down'></i> <span>{active2_count}</span></button>".format(
                    resource_url=resource_url,
                    active1_count=avs.filter(agree=True).count(),
                    active2_count=avs.filter(agree=False).count(),
                    active1=agree == True and 'active' or '',
                    active2=agree == False and 'active' or '',
                    disabled=disabled,
                )
            else:
                return "<button type='button' {disabled} data-toggle='tooltip' data-content_object='{resource_url}' data-container='body' data-value='1' data-placement='bottom' title='这个答案是有用的' " \
                       "class='btn btn-default {active1} vote_tag'><i class='fa fa-thumbs-up'></i> <span>{active1_count}</span></button>" \
                       "<button {disabled} type='button' data-toggle='tooltip' data-content_object='{resource_url}' data-value='0' data-container='body' " \
                       "data-placement='bottom' title='这个答案是没有用的' class='btn btn-default {active2} vote_tag'><i class='fa fa-thumbs-down'></i> <span>{active2_count}</span></button>".format(
                    resource_url=resource_url,
                    active1_count=avs.filter(agree=True).count(),
                    active2_count=avs.filter(agree=False).count(),
                    active1=agree == True and 'active' or '',
                    active2=agree == False and 'active' or '',
                    disabled=disabled,
                )
        except Exception as e:
            print e
        return ''


@register.filter
def focus_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    focus = Focus.objects.filter(object_id=obj.id, content_type=content_type)
    return focus.count()

@register.filter
def comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(object_id=obj.id, content_type=content_type)
    return comments.count()

@register.filter
def focus_user(obj):
    content_type = ContentType.objects.get_for_model(obj)
    focus = Focus.objects.filter(object_id=obj.id, content_type=content_type)
    return focus


@register.filter('summary')
def summary_text(text, l):
    return summary(text, l)

@register.filter('content_type')
def content_type(obj):
    return ContentType.objects.get_for_model(obj).id



@register.filter
def history(obj):
    return History.objects.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id,
        ).count()


class Authenticated(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        request = resolve_variable('request', context)
        user = request.user
        if not user.is_authenticated():
            content = loader.render_to_string('include/login_register.html', {'next': request.path})
            return content
        output = self.nodelist.render(context)
        return output

@register.tag
def is_authenticated(parser, token):
    args = token.split_contents()

    nodelist = parser.parse(('endis_authenticated',))
    parser.delete_first_token()

    return Authenticated(nodelist)

def get_pattern(query):
    items = []
    for pstr in re.split('\s+', query):
        sub_pstr = re.sub('^[\*\?\+]', '', pstr)
        if sub_pstr: items.append(sub_pstr)

    return '(?i)%s' % '|'.join(items)


def get_summary_text(query, searchable_text, _len=50):
    if query and searchable_text:
        m = re.search(get_pattern(query), searchable_text)
        if m is None:
            return 0, 0
        len_text = len(searchable_text)
        if len_text <= _len * 2:
            return 0, len_text

        start, end = m.span()
        if start - _len > 0:
            start -= _len
        else:
            start = 0
        end_text = searchable_text[end:]
        if len(end_text) < _len:
            end += len(end_text)
        else:
            end += _len
        return start, end
    return 0, 0


class SummaryHighlightNode(Node):
    def __init__(self, content, wd):
        self.wd = wd
        self.content = content

    def render(self, context):
        text = Variable(self.content).resolve(context)
        text = re.sub(r'<.*?>', u'', text).replace('&quot;', '').replace('&nbsp;', '     ')
        if not self.wd:
            text = text[0:200]
            return u'{0}{1}{2}'.format(text, '', len(text) > 200 and '...' or '')
        try:
            wd = Variable(self.wd).resolve(context)
            _list = []
            wd = filter(lambda w: w in text, wd)
            if not wd:
                raise Exception
            for se in sorted(map(lambda k: get_summary_text(unicode(k), text, 200 / len(wd)), wd),
                             key=lambda student: student[0]):
                start, end = se
                if start != end:
                    if _list:
                        if start - _list[-1][1] <= 0:
                            start, _end = _list.pop()
                    _list.append((start, end))
            _str = ''
            for index, (s, e) in enumerate(_list[0:6]):
                if s != 0 and _str == '':
                    _str += '...'
                if index != 0:
                    _str += '......'
                _str += text[s: e]

                if index + 1 == len(_list) and len(text) > e:
                    _str += '...'

            pattern = re.compile(ur'(%s)' % '|'.join(wd))
            _str = pattern.sub(r'<span class="color-red">\1</span>', _str)
        except Exception as e:
            print e
            text = text[0:200]
            _str = u'{0}{1}{2}'.format(text, '', len(text) > 200 and '...' or '')
        return _str


@register.tag
def summary_highlight(parser, token):
    bits = token.contents.split()
    wd = None
    if len(bits) == 3:
        wd = bits[2]
    return SummaryHighlightNode(bits[1], wd)