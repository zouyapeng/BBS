from django.db.models import Sum, Count
from django.shortcuts import render

# Create your views here.
from django.views import generic
from apps.question.models import QuestionTag
from apps.tag.models import Tag


class TagListView(generic.ListView):
    model = Tag
    template_name = "tag/tag_list.html"
    ordering = ['-update_date']

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        context['new_tag'] = self.object_list.all().order_by("-created")[0:15]
        from django.db import connection, transaction
        cursor = connection.cursor()
        cursor.execute('SELECT count(tag_id) as c, tag_id, title from ( SELECT question_questiontag.tag_id, tag_tag.title FROM question_questiontag left join tag_tag on tag_tag.id=question_questiontag.tag_id union  all SELECT article_articletag.tag_id, tag_tag.title FROM article_articletag left join tag_tag on tag_tag.id=article_articletag.tag_id) group by tag_id order by c desc limit 0, 20')
        context['popular'] = cursor.fetchall()
        # Tag().question_set
        # Tag().article_set
        return context


class TagDetailView(generic.DetailView):
    model = Tag
    slug_field = 'title'
    slug_url_kwarg = 'title'
    template_name = "tag/tag_detail.html"

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        if self.request.GET.get('tab') == 'question':
            object_list = self.object.question_set.all()
        else:
            object_list = self.object.article_set.all()
        context['object_list'] = object_list
        return context