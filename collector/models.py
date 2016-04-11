from __future__ import unicode_literals

import json
import time
from urllib.parse import urlparse, urlunparse

from django.db import models
from django.conf import settings


class Tweet(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    @property
    def important_words(self):
        return self.text

    def to_json(self):
        fields = ['text']
        data = {k: getattr(self, k) for k in fields}
        data['created_at'] = time.mktime(self.created_at.timetuple())
        return json.dumps(data)
