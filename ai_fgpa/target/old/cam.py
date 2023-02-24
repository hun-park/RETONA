import cv2
import pandas as pd

cam = cv2.VideoCapture(0)
ret, frame = cam.read()

print("ret : ", ret)
print("frame : ", frame)