#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings

from sklearn.exceptions import ConvergenceWarning

warnings.filterwarnings("ignore", category=ConvergenceWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

import numpy as np
import pandas as pd
import subprocess
import pickle
from datetime import datetime
# Tensorflow Libraries
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator


# In[2]:


def load_and_preprocess_images(directory_path, image_size=(224,224), batch_size=32):
    generator = ImageDataGenerator(
        preprocessing_function = tf.keras.applications.efficientnet.preprocess_input,
    )
    
    images = generator.flow_from_directory(
        directory_path,
        target_size=image_size,
        color_mode='rgb',
        class_mode=None,  # use 'None' if you don't have labels
        batch_size=batch_size,
        shuffle=False
    )
    
    return images

# Usage:
today = datetime.today().strftime("%Y%m%d")
directory_path = f"./new_test/{today}/"
images = load_and_preprocess_images(directory_path)


# In[3]:


# Set the global policy to float32
# tf.keras.mixed_precision.set_global_policy('float32')
model_path = 'converted_model.tflite'

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Assuming a single input and single output for simplicity
input_shape = input_details[0]['shape']
output_shape = output_details[0]['shape']

# Prepare your input data (replace 'input_data' with your input data)
predictions = []
probabilities = []
for i in range(len(images[0])):
    input_data = np.reshape(images[0][i], (1, 224, 224, 3))  # Your input data in the appropriate format


    # Set the input tensor to the loaded TFLite model
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Run inference
    interpreter.invoke()

    # Get the output tensor from the TFLite model
    output_data = interpreter.get_tensor(output_details[0]['index'])
    class_probabilities = output_data.max(axis=1)
    
    predicted_label_index = np.argmax(output_data)
    
    predictions.append(predicted_label_index)
    probabilities.append(class_probabilities)


# In[5]:

output_list = list([item.item() for sublist in probabilities for item in sublist])

percentage_list = [round(item * 100, 2) for item in output_list]

    
class_labels = predictions
class_probabilities = percentage_list


# In[6]:


with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)


# In[7]:


decoded_predictions = label_encoder.inverse_transform(class_labels)


# In[8]:


existing_data = {'diseaseName': decoded_predictions,
                 'severity': class_probabilities}

result_df = pd.DataFrame(existing_data)


# In[9]:


result_df.reset_index(drop=False, inplace=True)
result_df.rename(columns={'index': 'id'}, inplace=True)
result_df['id'] += 1


# In[10]:


df_length = len(result_df)

repetitions = (df_length // 4) + 1  

new_feature_pattern = np.repeat(range(repetitions), 4)
result_df['xCoord'] = new_feature_pattern[:df_length]

feature_2_pattern = [x % 4 + 1 for x in range(df_length)]
result_df['yCoord'] = feature_2_pattern


# In[11]:


encode_disease = {
    'Apple___Apple_scab': 'Apple scab',
    'Apple___Black_rot': 'Black rot',
    'Apple___Cedar_apple_rust': 'Cedar apple rust',
    'Apple___healthy': 'Healthy',
    'Blueberry___healthy': 'Healthy',
    'Cherry_(including_sour)___Powdery_mildew': 'Powdery mildew',
    'Cherry_(including_sour)___healthy': 'Healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': 'Cercospora leaf spot Gray leaf spot',
    'Corn_(maize)___Common_rust_': 'Common rust',
    'Corn_(maize)___Northern_Leaf_Blight': 'Northern Leaf Blight',
    'Corn_(maize)___healthy': 'Healthy',
    'Grape___Black_rot': 'Black rot',
    'Grape___Esca_(Black_Measles)': 'Esca (Black Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': 'Leaf blight (Isariopsis Leaf Spot)',
    'Grape___healthy': 'Healthy',
    'Orange___Haunglongbing_(Citrus_greening)': 'Haunglongbing (Citrus greening)',
    'Peach___Bacterial_spot': 'Bacterial spot',
    'Peach___healthy': 'Healthy',
    'Pepper,_bell___Bacterial_spot': 'Bacterial spot',
    'Pepper,_bell___healthy': 'Healthy',
    'Potato___Early_blight': 'Early blight',
    'Potato___Late_blight': 'Late blight',
    'Potato___healthy': 'Healthy',
    'Raspberry___healthy': 'Healthy',
    'Soybean___healthy': 'Healthy',
    'Squash___Powdery_mildew': 'Powdery mildew',
    'Strawberry___Leaf_scorch': 'Leaf scorch',
    'Strawberry___healthy': 'Healthy',
    'Tomato___Bacterial_spot': 'Bacterial spot',
    'Tomato___Early_blight': 'Early blight',
    'Tomato___Late_blight': 'Late blight',
    'Tomato___Leaf_Mold': 'Leaf Mold',
    'Tomato___Septoria_leaf_spot': 'Septoria leaf spot',
    'Tomato___Spider_mites Two-spotted_spider_mite': 'Spider mites Two-spotted spider mite',
    'Tomato___Target_Spot': 'Target Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': 'Tomato Yellow Leaf Curl Virus',
    'Tomato___Tomato_mosaic_virus': 'Tomato mosaic virus',
    'Tomato___healthy': 'Healthy'
}


# In[12]:


result_df['diseaseName'] = result_df['diseaseName'].replace(encode_disease)


# In[13]:


result_df.to_csv('PlantInfo.csv', index = False)


# In[ ]:


script_name = "plantPublisher.py"

with open("plantPublisher.py") as f:
    exec(f.read())

# try:
#     completed_process1 = subprocess.run(["python", "plantPublisher.py"], capture_output=True, shell=True)
#     print(completed_process1.stdout)
# except subprocess.CalledProcessError as e:
#     print('error')


script_name = "weatherPrediction.py"

with open("weatherPrediction.py") as f:
    exec(f.read())

# try:
#     completed_process2 = subprocess.run(["python", "weatherPrediction.py"], capture_output=True, shell=True)
#     print(completed_process2.stdout)
# except subprocess.CalledProcessError as e:
#     print('error')



