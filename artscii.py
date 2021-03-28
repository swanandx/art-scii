#!/usr/bin/env python3

import cv2
from PIL import Image
import time
import argparse
import requests


class Ascii_art:
	def __init__(self, width=70):
		self.width = width
		self.height = 0
		self.ASCII_CHARS_11 = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
		self.ASCII_CHARS_70 = ["$" , "@" , "B" , "%" , "8" , "&" , "W" , "M" , "#" , "*" , "o" , "a" , "h" , "k" , "b" , "d" , "p" , "q" , "w" , "m" , "Z" , "O" , "0" , "Q" , "L" , "C" , "J" , "U" , "Y" , "X" , "z" , "c" , "v" , "u" , "n" , "x" , "r" , "j" , "f" , "t" , "/" , "\\" , "|" , "(" , ")" , "1" , "{" , "}" , "[" , "]" , "?" , "-" , "_" , "+" , "~" , "<" , ">" , "i" , "!" , "l" , "I" , ";" , ":" , "," , "\"" , "^" , "`" , "'" , "." , " "]
		self.max = False


	def resize_image(self, image):
	    width, height = image.size
	    ratio = height/width
	    new_width = self.width
	    if self.height == 0:
	    	new_height = int(new_width * ratio)
	    else:
	    	new_height = self.height
	    resized_image = image.resize((new_width, new_height))
	    return(resized_image)


	def pixels_to_ascii(self, image):
		pixels = image.getdata()
		if self.max == True:
			characters = "".join([self.ASCII_CHARS_70[pixel//4] for pixel in pixels])
		else:
			characters = "".join([self.ASCII_CHARS_11[pixel//25] for pixel in pixels])
		return(characters)


	def from_video(self,video=None):
		if video:
			try:
				vid = cv2.VideoCapture(video)
			except Exception:
				print("An error occured.\n Please check if specified file is valid.")

		else:
			vid = cv2.VideoCapture(0)
			if self.height != 0:
				vid.set(3, self.width)
				vid.set(4, self.height)
		fps = int(vid.get(cv2.CAP_PROP_FPS))
		while True:
			try:
				ret,frame = vid.read()

				if ret:
					time.sleep(1/fps)
					frm = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
					self.img_to_art(Image.fromarray(frm))
					print('\033c',end='')
				else:
					break
			except KeyboardInterrupt:
				break
		vid.release()
		cv2.destroyAllWindows()


	def from_image(self, path):
		try:
			img = Image.open(path)
			img = img.convert('L')
			self.img_to_art(img)
		except Exception as e:
			print("Please check if supplied file is a image.\n An Error occured.")


	def img_to_art(self,img):
	    new_width = self.width    
	    new_image_data = self.pixels_to_ascii(self.resize_image(img)) 
	    pixel_count = len(new_image_data)  
	    ascii_image = "\n".join([new_image_data[index:(index+new_width)] for index in range(0, pixel_count, new_width)])
	    print(ascii_image)


	def from_url(self,url):
		try:
			im = Image.open(requests.get(url, stream=True).raw)
			im = im.convert('L')
			self.img_to_art(im)
		except Exception:
			print("An error occured.")

	def main(self):
		parser = argparse.ArgumentParser()
		parser.add_argument("--image", "-i", help="ASCII from image")
		parser.add_argument("--url", "-u", help="Get image from url")
		parser.add_argument("--video", "-v", help="ASCII from Video")
		parser.add_argument("--webcam", "-w", help="ASCII from webcam [For better view, specify height and width]",action="store_true")
		parser.add_argument("--max", "-m", help="Use 70 shades",action="store_true")
		parser.add_argument("--width", "-W", type=int, help="Specify width for output")
		parser.add_argument("--height", "-H", type=int, help="Specify height for output")

		args = parser.parse_args()
		
		if args.max:
			self.max = True
		if args.width:
			self.width=args.width
		if args.height:
			self.height=args.height

		if args.image:
			self.from_image(args.image)
		elif args.video:
			self.from_video(args.video)
		elif args.webcam:
			self.from_video()
		elif args.url:
			self.from_url(args.url)
		else:
			print("Please specify some arguments. Use -h / --help for help")


if __name__ == '__main__':
	Ascii_art().main()
