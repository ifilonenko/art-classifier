import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Environments for the app the run in -
# NOTE! This app only has one environment to run
# in, but one could specify multiple classes
# here to differentiate different environments the
# backend could run in

class Config(object):
  DEBUG = True
  CSRF_ENABLED = True
  CSRF_SESSION_KEY = "secret-1"
  SECRET_KEY = "secret-2"
  THREADS_PER_PAGE = 2
  UPLOAD_FOLDER = '/tmp/'
  ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
  ARTIST_LABELS = 'output_labels_artists_90.txt'
  ARTIST_MODELS = 'output_graph_artists_90.pb'
  STYLES_LABELS = 'output_labels_style.txt'
  STYLES_MODELS = 'output_graph_style.pb'
