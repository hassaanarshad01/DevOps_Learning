#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from models import ModelPackage
import os
from io import BytesIO

app = Flask(__name__)
CORS(app) 

models = ModelPackage()
print('models made')

@app.route('/')
def home():
    return jsonify({"status": "Flask API is up and running!"}), 200

@app.route('/classify', methods=['POST'])
def classify():
    print('reached classify')
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        image_path = os.path.join("temp", file.filename)
        print('path joined with: ', file.filename)
        
        print(f"Saving file to: {image_path}")
        file.save(image_path)
        
        classification_result = models.classify(image_path)
        return jsonify({"classification": classification_result})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        

    

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files or 'model_name' not in request.form:
        return jsonify({"error": "File or model name missing"}), 400

    file = request.files['file']
    model_name = request.form['model_name']
    image_path = os.path.join("temp/predicts", "input.jpg")
    file.save(image_path)

    result = models.predict(image_path, model_name)

    output_path = os.path.join("temp/predicts", "output.jpg")
    models.save_image(result, output_path)

    return send_file(output_path, mimetype='image/jpeg')



@app.route('/inpaint', methods=['POST'])
def inpaint():
    """try:
        print("Received inpaint request")

        if 'file' not in request.files or 'prompt' not in request.form:
            print("File or prompt missing")
            return jsonify({"error": "File or prompt missing"}), 400

        file = request.files['file']
        prompt = request.form['prompt']
        print(f"File received: {file.filename}")
        print(f"Prompt: {prompt}")

        image_path = os.path.join("temp/inpainting", "1 - inpaint_input.jpg")
        file.save(image_path)

        inpainted_image, eroded_mask, clear_mask = models.inpaint_image(image_path, prompt)

        output_path_clear_mask = os.path.join("temp/inpainting", "2 - clear_mask.jpg")
        clear_mask.save(output_path_clear_mask)
        
        output_path_eroded_mask = os.path.join("temp/inpainting", "3 - eroded_mask.jpg")
        eroded_mask.save(output_path_eroded_mask)
        
        output_path = os.path.join("temp/inpainting", "4 - inpaint_output.jpg")
        inpainted_image.save(output_path)
        
        img_io = BytesIO()
        inpainted_image.save(img_io, 'JPEG')
        img_io.seek(0)

        print("Sending inpainted image response")
        return send_file(img_io, mimetype='image/jpeg')
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
        """
    return

if __name__ == '__main__':
    print('main working')
    os.makedirs("temp", exist_ok=True) 
    app.run(host='0.0.0.0', port=5000)


# In[ ]:




