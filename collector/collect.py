import logging

import pika
import django
from django.conf import settings

django.setup()

from collector import models
from livefeed.utils import twitter


logger = logging.getLogger(__name__)


class TweetPublisher():
    connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'))

    @classmethod
    def publish(cls, tweet):
        if hasattr(cls, 'channel') and cls.channel.is_open:
            channel = cls.channel
        else:
            channel = cls.channel = cls.connection.channel()

        return cls.channel.basic_publish(exchange='',
                                         routing_key='tweets',
                                         body=tweet.to_json())


def get_keywords():
    return settings.KEYWORDS


def extract_tweet_info(tweet):
    info = {
        'text': tweet.get('text', ''),
    }

    return info


def get_valid_tweets():
    for data in twitter.api.track(get_keywords()):
        tweet = extract_tweet_info(data)
        if tweet['text']:
            yield tweet


def collect():
    for tweet in get_valid_tweets():
        try:
            tweet = models.Tweet.objects.create(**tweet)
        except Exception:
            logger.exception(u"indexing of tweet failed: %s", tweet.text)
        else:
            logger.info(u"indexing: %s", tweet.text)
            TweetPublisher.publish(tweet)


if __name__ == "__main__":
    logger = logging.getLogger('collector.collect')
    logger.info("starting collector")
    collect()
