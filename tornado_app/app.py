import django
import logging
import tornado.web
import tornado.ioloop
import tornado.websocket
from django.template.loader import render_to_string

django.setup()

from collector import models
from tornado_app import queue_client


logger = logging.getLogger("tornado_app.app")


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        context = {
            "tweets": models.Tweet.objects.order_by('-created_at')[:10],
        }
        self.write(render_to_string("tornado_app/index.html", context))


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    _clients = {}
    _client_count = 0

    @classmethod
    def broadcast_tweet(cls, tweet):
        for client in cls._clients.values():
            client.write_message(tweet)

    def add_client(self):
        WebSocketHandler._client_count += 1
        self.client_id = WebSocketHandler._client_count
        WebSocketHandler._clients[self.client_id] = self

    def delete_client(self):
        del self._clients[self.client_id]

    def open(self):
        self.add_client()
        logger.debug("Opening client: %d", self.client_id)

    def on_close(self):
        self.delete_client()
        logger.debug("closing client: %d", self.client_id)

    def check_origin(self, origin):
        logger.debug("Got socket request from %s", origin)
        return True


def make_app():
    return tornado.web.Application([
        (r"/", IndexHandler),
        (r"/websocket", WebSocketHandler),
    ], debug=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)

    tweet_consumer = queue_client.QueueClient(
        'tweets', WebSocketHandler.broadcast_tweet)
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        tweet_consumer.stop()
