# Twitter Live Feed
This is a simple example of how we can use websockets to show real time twitter
feed on a webpage. This repo also serves as an example for using Tornado with
Django.

The frontend is written in Angular but the backend can work with any frontend
framework.

## Dependencies
- Python 3
- RabbitMQ
- Node.js
- Modern browser which supports WebSockets

## How to run services
Before running the servies create a link from `/opt/twitter-livefeed` to the
repository folder, this way the following commands can be run as it is.

### Collector service
1. `cd /opt/twitter-livefeed/collector`
2. `DJANGO_SETTINGS_MODULE=livefeed.settings PYTHONPATH=/opt/twitter-livefeed python collect.py`

### Tornado service
1. `cd /opt/twitter-livefeed/tornado_app`
2. `DJANGO_SETTINGS_MODULE=livefeed.settings PYTHONPATH=/opt/twitter-livefeed python app.py`

### Websever
1. `cd /opt/twitter-livefeed/frontend`
2. `npm install` (should be done only the first time)
3. `npm start`

## Gotchas
- If you are not getting the real time updates then before trying anything else
  try refreshing the web page, it's possible that the socket connection to
  server is not open, refreshing the page will reconnect the socket.
- If you get InsecurePlatformWarning due to SSL when you run `collector` service
  try `pip install --upgrade ndg-httpsclient`.
