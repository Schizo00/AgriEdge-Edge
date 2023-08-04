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
from PIL import Image
from datetime import datetime
import sys
# Tensorflow Libraries
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator

from google.cloud import pubsub_v1
import avro.schema as schema
from google.api_core.exceptions import NotFound
from google.pubsub_v1.types import Encoding
from avro.io import BinaryEncoder, DatumWriter
import io

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.popup import Popup


class AgriEdge(App):
    def __init__(self, **kwargs):
        super(AgriEdge, self).__init__(**kwargs)
        self.progress_value = 0
        self.process = None


    def start_process(self, *args):
        # Replace "your_script.py" with the name of the script you want to run
        with open("plantPrediction.py", "r") as f:
            script_contents = exec(f.read())

        completion_popup = Popup(title='Process Completed', content=Label(text='The process has finished.'),
                                 size_hint=(None, None), size=(400, 200))
        completion_popup.open()
        
        print("Done")

    def build(self):
        # Main layout
        layout = FloatLayout()

        # Set white background for the entire application
        with layout.canvas.before:
            Color(241, 239, 239)  # White color with full opacity
            self.rect = Rectangle(size=layout.size, pos=layout.pos)

        layout.bind(size=self._update_rect, pos=self._update_rect)

        # Logo image (centered)
        logo = Image(source='Logo.png',
                     pos_hint={'center_x': 0.5, 'center_y': 0.6})
        layout.add_widget(logo)

        # Manual button (centered)
        button = Button(text='Manual', font_size=24,size_hint=(None, None), size=(300, 75),
                        pos_hint={'center_x': 0.5, 'center_y': 0.3},
                        background_normal='Button1.png',
                        background_down='Button2.png',
                        color=(0, 0, 0, 1))  # Set transparent background color
        button.bind(on_press=self.start_process)
        
        layout.add_widget(button)


        return layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

if __name__ == '__main__':
    AgriEdge().run()
