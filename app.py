import os

from flask import Flask, request
from tensorflow import keras
import numpy as np
import cv2
from werkzeug.utils import secure_filename

filepath = 'C:/Users/jaxso/PycharmProjects/flaskProject/images/'

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    # get file input and save it to images directory with randomized name and redirect to /predict/<randomized_name>
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded'
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save('images/' + filename)
        return f"""
        <p>Predicted: {predict(filepath + filename)}</p>
        """
    return f"""
    <h1>Upload a Captcha Image</h1>
    <form method=post enctype=multipart/form-data>
        <input type=file name=file />
        <input type=submit value=Upload />
    </form>
    """


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))

valid_characters = "0123456789abcdefghijklmnopqrstuvwxyz"

model = keras.models.load_model('trained_model')


# Define function to predict captcha
def predict(filepath):
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    if img is not None:
        img = img / 255.0
        img = np.reshape(img, (50, 200, 1))
    else:
        print("Not detected")
    res = np.array(model.predict(img[np.newaxis, :, :, np.newaxis]))
    ans = np.reshape(res, (5, 36))
    l_ind = []
    for a in ans:
        l_ind.append(np.argmax(a))

    capt = ''
    for l in l_ind:
        capt += valid_characters[l]
    return capt
