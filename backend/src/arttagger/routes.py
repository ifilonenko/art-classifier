from flask import jsonify, request
from werkzeug.utils import secure_filename
from arttagger import app
from arttagger.predicter import Predicter
import os

@app.route('/artist', methods=['POST'])
def artists():
  image = request.files['image']
  filename = secure_filename(image.filename)
  file_location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
  image.save(file_location)
  predicter = Predicter(file_location)
  predicter.resize(file_location)
  predicter.predict_artists()
  return jsonify({'result': predicter.result, 'total': predicter.total, 'top': predicter.top})

@app.route('/style', methods=['POST'])
def styles():
  image = request.files['image']
  filename = secure_filename(image.filename)
  file_location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
  image.save(file_location)
  predicter = Predicter(file_location)
  predicter.resize(file_location)
  predicter.predict_styles()
  return jsonify({'result': predicter.result, 'total': predicter.total, 'top': predicter.top})
