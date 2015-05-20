# -*- coding: utf-8 -*-
import os
import re
import uuid
from django.utils.html import strip_tags
from HTMLParser import HTMLParser


def get_file_path(instance, filename, to):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(to, filename)


def summary(text, length):
    text = u''.join(strip_tags(text).split())

    if len(text) > length:
        text = '%s...' % text[0: length]
    return text


def get_html_tag(html):
    tags = []

    class MyHTMLParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            tags.append(tag)

    p = MyHTMLParser()
    p.feed(html)
    return set(tags)


def remove_html_tag(html, tags):
    for tag in tags:
        re_data = re.compile('</?\s*?%s\s*?.*?/?>' % tag, re.I)
        html = re_data.sub('', html)
    return html
