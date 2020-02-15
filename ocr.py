from PIL import Image
import pytesseract
import argparse
import cv2
import os
import pickle


def ocrResult(image):
	fname = image
	image = cv2.imread(fname)
	# gray  = cv2.cvtColor(image,cv2.COLOR_BG2GRAY)
	pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
	text  = pytesseract.image_to_string(Image.open(fname))
	print(text)
	return text