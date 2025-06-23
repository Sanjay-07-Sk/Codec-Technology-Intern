from flask import Flask, request, render_template
import os
import numpy as np
from keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from keras.preprocessing.image import load_img, img_to_array

# Setup
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Load model
model = MobileNetV2(weights='imagenet')

# Preprocessing function
def prepare_image(image_path):
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
    return image
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return 'No image part'
        file = request.files['image']
        if file.filename == '':
            return 'No image selected'
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        image = prepare_image(filepath)
        preds = model.predict(image)
        result = decode_predictions(preds, top=1)[0][0]

        label = result[1]  # predicted label
        confidence = round(result[2] * 100, 2)

        return render_template('result.html', label=label, confidence=confidence, image=file.filename)
    
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
