# import the necessary packages
from PIL import Image
import os, ntpath
from random import shuffle
import flask
from flask import send_file, request, Response, jsonify
import io
import json
import constants as P

## KERAS
#from keras.models import load_model
#import keras.backend as K

# initialize our Flask application and the Keras model
app = flask.Flask(__name__)


##########################################
##############  KERAS MODEL  #############
import tensorflow as tf
#import tensorflow.compat.v1 as tf
#from tensorflow.compat.v1.keras.models import load_model
#import tensorflow.compat.v1.keras.backend as K


from io import StringIO
import base64, uuid
import numpy as np

#tf.disable_v2_behavior()
    
print("Loading pix2pix model: " + P.BASE_DIR + P.MODEL + "..")
model = tf.keras.models.load_model(P.BASE_DIR + P.MODEL, compile=False)
print("Loading model.. DONE!")

graph = tf.get_default_graph()

@app.route("/magic", methods=["POST"])
def magic():
    image_uuid = uuid.uuid4().hex
    filename_orig = P.BASE_DIR + P.TEMP_DIR + image_uuid + '_orig.png'
    filename_segm = P.BASE_DIR + P.TEMP_DIR + image_uuid + '_segm.png'
    filename_pred = P.BASE_DIR + P.TEMP_DIR + image_uuid + '_pred.png'

    print ('MAGIC BLACKBOARD REQUEST: ' + filename_orig)
    with open(filename_orig,"wb+") as f:
        f.write(base64.b64decode(request.form['original']))
    with open(filename_segm,"wb+") as f:
        f.write(base64.b64decode(request.form['segmentation']))

    # OPEN AND PREPROCESS IMAGES
    img_org = Image.open(filename_orig)
    # WHITE BACKGROUND + PAINT CAUSE IT IS RGBA AND WE NEED ONLY RGB
    paint_sgm = Image.open(filename_segm)
    img_sgm = Image.new("RGB", paint_sgm.size, (255, 255, 255))
    img_sgm.paste(paint_sgm, mask=paint_sgm.split()[3])

    # DELETE TEMP FILE
    if not P.SAVE_DATA:
        os.unlink(filename_orig)
        os.unlink(filename_segm)

    # PREPARE IMAGES FOR MODEL INGESTION
    img_arr_org = np.array(img_org.resize(P.MODEL_SIZE_ORG, Image.BILINEAR))
    img_arr_org = np.asarray(img_arr_org/127.5 - 1)
    img_arr_org = np.expand_dims(img_arr_org, axis=0)

    img_arr_sgm = np.array(img_sgm.resize(P.MODEL_SIZE_SGM, Image.BILINEAR))
    img_arr_sgm = np.asarray(img_arr_sgm/127.5 - 1)
    img_arr_sgm = np.expand_dims(img_arr_sgm, axis=0)
 
    # DO THE MAGIC
    global graph
    with graph.as_default():
        out = model.predict([img_arr_sgm, img_arr_org])
    out_img = Image.fromarray(np.uint8((out[0]+1)*127.5))

    if P.SAVE_DATA:
        out_img.save(filename_pred)

    img_io = io.BytesIO()
    out_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

############# KERA MODEL #################
##########################################

@app.route('/')
def homepage():
    return "NOTHING TO DO HERE"

def start_api():
    app.run(host='0.0.0.0')

