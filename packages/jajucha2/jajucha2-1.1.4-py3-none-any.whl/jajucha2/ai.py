import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image as Img
from torch.utils.data import Dataset
import os
import cv2
import numpy as np
from torchsummary import summary

from IPython.display import display, Image
import ipywidgets as widgets
from IPython.display import clear_output
import mysql.connector
from ultralytics import YOLO
import logging

logging.getLogger("ultralytics").setLevel(logging.CRITICAL)

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="1111",
    database="datasets"
)

transform = transforms.Compose([
    transforms.Resize(224),         
    transforms.CenterCrop((224, 224)), 
    transforms.ToTensor(),
])

cursor = conn.cursor()
home_dir = os.path.expanduser("~")
device = torch.device('cuda')

def get_classes(project):
    query = "select Name from Classes where project= %s;"
    cursor.execute(query, (project,))
    rows = cursor.fetchall()
    return rows

def get_model_dir(name):
    # Use parameterized query to prevent SQL injection
    query = "SELECT model FROM Projects WHERE Name = %s"
    cursor.execute(query, (name,))
    rows = cursor.fetchall()

    # Check if any rows were returned
    if rows:
        return rows[0][0]  # Return the first element of the first row
    else:
        return None  # Return None if no rows were found
    

def show_models():
    query = "SELECT Name,Model FROM UserModels"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

#yolo should be added
def get_model(name):
    query = "SELECT uuid, Model FROM UserModels WHERE Name = %s"
    cursor.execute(query, (name,))
    rows = cursor.fetchone()  # Use fetchone if you're expecting only one result
    uuid, model_name = rows[0], rows[1]

    modeldir = home_dir + "/server/models/usermodels/" + uuid + ".pt"

    loaded_model = None
    if model_name in ['RESNET18', 'RESNET50', 'RESNET101', 'RESNET152']:
        loaded_model = torch.jit.load(modeldir)
        loaded_model.eval()  # Set model to evaluation mode
    elif model_name in ['YOLO8N', 'YOLO9N', 'YOLO10N', 'YOLO11N']:
        loaded_model = YOLO(modeldir)
    return loaded_model

# Cache for model UUIDs, shapes, and loaded models
model_cache = {}

def get_model_output(input, name):
    if name not in model_cache:
        # Fetch metadata from the database if not in cache
        query = "SELECT uuid, Model FROM UserModels WHERE Name = %s"
        cursor.execute(query, (name,))
        rows = cursor.fetchone()  # Use fetchone if you're expecting only one result
        uuid, model_name = rows[0], rows[1]
        
        modeldir = home_dir + "/server/models/usermodels/" + uuid + ".pt"
        
        # Fetch the required output shape
        query = "SELECT shape FROM Models WHERE Name = %s"
        cursor.execute(query, (model_name,))
        shape_row = cursor.fetchone()
        shape = shape_row[0]
        
        # Load the model and cache it
        loaded_model = None
        if model_name in ['RESNET18', 'RESNET50', 'RESNET101', 'RESNET152']:
            loaded_model = torch.jit.load(modeldir)
            loaded_model.eval()  # Set model to evaluation mode
        elif model_name in ['YOLO8N', 'YOLO9N', 'YOLO10N', 'YOLO11N']:
            loaded_model = YOLO(modeldir)
        
        # Cache model data, including the loaded model
        model_cache[name] = {
            'modeldir': modeldir,
            'model_name': model_name,
            'shape': shape,
            'model': loaded_model  # Cache the loaded model
        }
    else:
        # Fetch from cache
        modeldir = model_cache[name]['modeldir']
        model_name = model_cache[name]['model_name']
        shape = model_cache[name]['shape']
        loaded_model = model_cache[name]['model']  # Use cached model

    # Use the cached model to get the output
    if model_name in ['RESNET18', 'RESNET50', 'RESNET101', 'RESNET152']:
        image = Img.fromarray(cv2.cvtColor(input, cv2.COLOR_BGR2RGB))
        image = transform(image)
        image = image.unsqueeze(0).to(device)
        output = loaded_model(image)
        return output
    
    elif model_name in ['YOLO8N', 'YOLO9N', 'YOLO10N']:
        results = loaded_model(input)
        return results
 

def get_model_input(name):
    query = "SELECT Model FROM UserModels WHERE Name = %s"
    cursor.execute(query, (name,))
    rows = cursor.fetchall()
    model = rows[0][0]

    query = "SELECT shape FROM Models WHERE Name = %s"
    cursor.execute(query, (model,))
    rows = cursor.fetchall()
    shape = rows[0][0]
    print(shape)