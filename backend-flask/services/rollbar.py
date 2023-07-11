import rollbar
import rollbar.contrib.flask
from flask import Flask
from flask import got_request_exception
import os

## XXX hack to make request data work with pyrollbar <= 0.16.3
def _get_flask_request():
  print("Getting flask request")
  from flask import request
  print("request:", request)
  return request
rollbar._get_flask_request = _get_flask_request

def _build_request_data(request):
  return rollbar._build_werkzeug_request_data(request)
rollbar._build_request_data = _build_request_data
## XXX end hack

def init_rollbar(app: Flask):
  rollbar.init(
  access_token=os.getenv("ROLLBAR_ACCESS_TOKEN"),
  flask_env = os.getenv('FLASK_ENV'),
  environment='cruddur flask',
  root=os.path.dirname(os.path.realpath(__file__)),
  code_version='1.0',
  allow_logging_basic_config=False
  )
  # send exceptions from `app` to rollbar, using flask's signal system.
  got_request_exception.connect(rollbar.contrib.flask.report_exception, app)
  return rollbar
