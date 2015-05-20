# # -*- coding: utf-8 -*-
from datetime import datetime
import os
import uuid
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _


class AttachmentManager(models.Manager):
    def attachments_for_object(self, obj):
        object_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__pk=object_type.id,
                           object_id=obj.id)


def attachment_upload(instance, filename):
        file_name = str(uuid.uuid4()) + os.path.splitext(filename)[1]
        instance.target_filename = file_name
        return 'attachments/%s/%s' % (
            '%s_%s' % (instance._meta.app_label,
                       instance._meta.object_name.lower()),
            file_name)


class Attachment(models.Model):
    objects = AttachmentManager()

    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    source_filename = models.CharField('Source Filename', max_length=255, null=True, blank=True, editable=False)
    target_filename = models.CharField('Target Filename', max_length=255, null=True, blank=True, editable=False)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="created_attachments", verbose_name="文件上传者")
    attachment_file = models.FileField(_('attachment'), upload_to=attachment_upload)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)


    class Meta:
        ordering = ['-created']
        permissions = (
            ('delete_foreign_attachments', 'Can delete foreign attachments'),
        )

    def __unicode__(self):
        return '%s attached %s' % (self.creator.username, self.attachment_file.name)


