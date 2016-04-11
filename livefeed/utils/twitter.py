import json
import time
import logging

import TwitterAPI
from django.conf import settings


logger = logging.getLogger(__name__)


class Twitter(object):
    def __init__(self):
        self.api = TwitterAPI.TwitterAPI(settings.CONSUMER_KEY,
                                         settings.CONSUMER_SECRET,
                                         settings.ACCESS_TOKEN,
                                         settings.ACCESS_SECRET)

    def make_request(self, endpoint, data):
        rsp = self.api.request(endpoint, data)
        time_to_sleep = 5
        while rsp.status_code != 200:
            logger.error('api error, endpoint: %s, data: %s, '
                         'rsp: %s, status_code: %d',
                         endpoint, json.dumps(data), rsp.text,
                         rsp.status_code)
            time.sleep(time_to_sleep)
            time_to_sleep *= 2
            rsp = self.api.request(endpoint, data)

        return rsp

    def track(self, keywords):
        return self.make_request('statuses/filter',
                                 {'track': keywords}).get_iterator()


api = Twitter()
