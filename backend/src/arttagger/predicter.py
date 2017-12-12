import os, sys
import tensorflow as tf
from arttagger import app
from PIL import Image

class Predicter(object):
  image = None
  def __init__(self, image):
    self.image = image
    self.resized_image = ""
    self.result = []
    self.total = 0
    self.top = ""

  def resize(self, infile):
    size = (299, 299)
    outfile_name = os.path.splitext(infile)[0] + '_resized.jpg'
    outfile = os.path.join(app.config['UPLOAD_FOLDER'], outfile_name)
    try:
        im = Image.open(infile)
        im.thumbnail(size, Image.ANTIALIAS)
        old_im_size = im.size

        ## By default, black colour would be used as the background for padding!
        new_im = Image.new("RGB", size)

        new_im.paste(im, (int((size[0]-old_im_size[0])/2),
                          int((size[1]-old_im_size[1])/2)))
        new_im.save(outfile, "JPEG")
        self.resized_image = outfile
    except IOError as e:
        print "Cannot resize '%s' because of '%s" % (infile, e)

  def predict_artists(self):
    labels_artist_file = "%s/%s" % (app.root_path,app.config['ARTIST_LABELS'])
    model_artist_file = "%s/%s" % (app.root_path,app.config['ARTIST_MODELS'])
    # Read in the image_data
    image_data = tf.gfile.FastGFile(self.resized_image, 'rb').read()
    # Loads label file, strips off carriage return
    l_lines = [line.rstrip() for line
               in tf.gfile.GFile(labels_artist_file)]
    # Unpersists graph from file
    with tf.gfile.FastGFile(model_artist_file, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    init_ops = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init_ops)
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1][:5]
        self.result = \
          [{'identifier': l_lines[node_id], 'score':str(predictions[0][node_id])} for node_id in top_k]
        self.total = sum([ float(k["score"]) for k in self.result])
        self.top = self.result[0]["identifier"]
    os.remove(self.resized_image)
    os.remove(self.image)

  def predict_styles(self):
      labels_styles_file = "%s/%s" % (app.root_path,app.config['STYLES_LABELS'])
      model_styles_file = "%s/%s" % (app.root_path,app.config['STYLES_MODELS'])
      # Read in the image_data
      image_data = tf.gfile.FastGFile(self.resized_image, 'rb').read()
      # Loads label file, strips off carriage return
      l_lines = [line.rstrip() for line
                 in tf.gfile.GFile(labels_styles_file)]
      # Unpersists graph from file
      with tf.gfile.FastGFile(model_styles_file, 'rb') as f:
          graph_def = tf.GraphDef()
          graph_def.ParseFromString(f.read())
          _ = tf.import_graph_def(graph_def, name='')

      init_ops = tf.global_variables_initializer()
      with tf.Session() as sess:
          sess.run(init_ops)
          # Feed the image_data as input to the graph and get first prediction
          softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

          predictions = sess.run(softmax_tensor, \
                   {'DecodeJpeg/contents:0': image_data})

          # Sort to show labels of first prediction in order of confidence
          top_k = predictions[0].argsort()[-len(predictions[0]):][::-1][:5]
          for node_id in top_k:
            human_string = l_lines[node_id]
            score = predictions[0][node_id]
            print('%s (score = %.5f)' % (human_string, score))
          self.result = \
            [{'identifier': l_lines[node_id], 'score':str(predictions[0][node_id])} for node_id in top_k]
          self.total = sum([ float(k["score"]) for k in self.result])
          self.top = self.result[0]["identifier"]
      os.remove(self.resized_image)
      os.remove(self.image)
