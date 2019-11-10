#!/usr/bin/env python3
import torch
import torchvision
import torch.nn.functional as F
import time
import datetime
import numpy as np
import cv2
import torchvision.transforms as transforms
import PIL.Image
import boto3
from jetbot import Camera

model_roadfollow = torchvision.models.resnet18(pretrained=False)
model_roadfollow.fc = torch.nn.Linear(512, 2)
model_roadfollow.load_state_dict(torch.load('best_steering_model_xy.pth'))

model_mascotdet = torchvision.models.resnet18(pretrained=False)
model_mascotdet.fc = torch.nn.Linear(512, 10)
model_mascotdet.load_state_dict(torch.load('best_mascotdet_model_xy.pth'))

device = torch.device('cuda')

model = model_roadfollow.to(device)
model = model_roadfollow.eval().half()

model_mascotdet = model_mascotdet.to(device)
model_mascotdet = model_mascotdet.eval()

camera = Camera.instance(width=224, height=224)

from jetbot import Robot
robot = Robot()
speed_gain_slider = 0.20
steering_gain_slider = 0.15
steering_dgain_slider = 0.00
steering_bias_slider = 0.00
angle = 0.0
angle_last = 0.0
prev_class = -1

mascot_names = [
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9']

mean = 255.0 * np.array([0.485, 0.456, 0.406])
stdev = 255.0 * np.array([0.229, 0.224, 0.225])

mean_roadfollow = torch.Tensor([0.485, 0.456, 0.406]).cuda().half()
std_roadfollow = torch.Tensor([0.229, 0.224, 0.225]).cuda().half()

normalize = torchvision.transforms.Normalize(mean, stdev)


def preprocess(camera_value):
    global device, normalize
    x = camera_value
    x = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)
    x = x.transpose((2, 0, 1))
    x = torch.from_numpy(x).float()
    x = normalize(x)
    x = x.to(device)
    x = x[None, ...]
    return x

def preprocess_roadfollow(image):
    image = PIL.Image.fromarray(image)
    image = transforms.functional.to_tensor(image).to(device).half()
    image.sub_(mean_roadfollow[:, None, None]).div_(std_roadfollow[:, None, None])
    return image[None, ...]

def find_mascot(change):
    x = change['new'] 
    x = preprocess(x)
    y = model_mascotdet(x)
    y_mascot = F.softmax(y, dim=1)
    topk = y_mascot.cpu().topk(1)
    
    return (e.data.numpy().squeeze().tolist() for e in topk)


def move_bot(image, robot_stop):
    global angle, angle_last    
    if robot_stop:
        robot.stop()
        robot.left_motor.value=0
        robot.left_motor.value=0
        time.sleep(2)
        robot_stop = False
    else:
        xy = model_roadfollow(preprocess_roadfollow(image)).detach().float().cpu().numpy().flatten()
        x = xy[0]
        y = (0.5 - xy[1]) / 2.0
        speed_slider = speed_gain_slider
        angle = np.arctan2(x, y)
        pid = angle * steering_gain_slider + (angle - angle_last) * steering_dgain_slider
        angle_last = angle
        steering_slider = pid + steering_bias_slider
        robot.left_motor.value = max(min(speed_slider + steering_slider, 1.0), 0.0)
        robot.right_motor.value = max(min(speed_slider - steering_slider, 1.0), 0.0)
    
while True:
    img = camera.value
    probs, classes = find_mascot({'new': img}) 
    msg = "Start..."
    s3url = ""
    if probs > 0.6 and prev_class != classes:
        prev_class = classes
        msg = '{"mascot":"' + mascot_names[classes] + '"' + ',"confidence":"' + str(probs) +'"}'
        print(msg)
    move_bot(img, robot_stop)