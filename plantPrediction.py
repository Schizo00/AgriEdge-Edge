#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings("ignore", category=ConvergenceWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

import itertools
import numpy as np
import pandas as pd
import os
import subprocess
import json
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from PIL import Image
from sklearn.metrics import classification_report, f1_score , confusion_matrix

import sys
print(sys.executable)

# Tensorflow Libraries
import tensorflow as tf
from tensorflow import keras
from keras.layers import Dense, Dropout , BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers,models,Model
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.keras.callbacks import Callback, EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras import mixed_precision
tf.keras.mixed_precision.set_global_policy('float16')


print(tf.__version__)


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
directory_path = "./test"
images = load_and_preprocess_images(directory_path)


# In[3]:


# Set the global policy to float32
# tf.keras.mixed_precision.set_global_policy('float32')

# Directory where the SavedModel is stored
model_directory = 'my_model_new'  # Replace with the actual directory path

# Load the model from the directory
model = tf.keras.models.load_model(model_directory)
# predictions = model.predict(images)


# In[4]:


predictions = model.predict(images)


# In[5]:


class_labels = predictions.argmax(axis=1)
class_probabilities = predictions.max(axis=1)


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

try:
    completed_process = subprocess.run(["python", script_name], capture_output=True)
    print(completed_process.stdout)    
except subprocess.CalledProcessError as e:
    print('error')


# In[14]:


##plantsPerDisease = {'plantsPerDisease' : [result_df['diseaseName'].value_counts().to_dict()]}
##
##
### In[15]:
##
##
##file_path = 'plantsPerDisease.json'
##
##with open(file_path, 'w') as file:
##    json.dump(plantsPerDisease, file)
##
##
### In[ ]:
##
##
##script_name = "plantSpreadPublisher.py"
##
### Call the second script using subprocess
##try:
##    completed_process = subprocess.run(["python", script_name], capture_output=True)
##    print(completed_process.stdout)    
##except subprocess.CalledProcessError as e:
##    print('error')

