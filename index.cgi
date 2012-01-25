#!/usr/bin/python

import os
import EXIF
import cPickle as pickle
import re

try:
	image_data = pickle.load( open( "image_data.p", "rb" ) )

except:
	image_data = {}

class image:
	def __init__(self,path):
		my_data = {}
		self.base_directory = os.path.split(path)[0]
		self.filename = os.path.split(path)[-1]
		self.file_base_name = self.filename.split(".")[0]
		self.fullsize = path
		self.thumb_path = "thumbs/thumb_%s" % (self.filename)
		self.raw_path = "raw/%s.NEF" % (self.file_base_name)
		
		if not image_data.has_key(self.file_base_name):	
			f = open(path,'rb')
			try:
				tags = EXIF.process_file(f)
				f.close()
				datetime = str(tags['EXIF DateTimeDigitized'])
				self.date = datetime.split(" ")[0]
				self.time = datetime.split(" ")[1]
				self.shutterspeed = str(tags['EXIF ExposureTime'])
				apperature_string =  str(tags['EXIF FNumber']).split("/")
				if len(apperature_string) > 1:
					top = int(apperature_string[0])
					bottom = int(apperature_string[1])
					self.fstop = round((float(top)/float(bottom)), 1)
				else:
					self.fstop = apperature_string[0]
			except:
				self.date = "0"
				self.time = "0"
				self.shutterspeed = "0"
				self.fstop = "0"
		else:
			my_data = image_data[self.file_base_name]
			self.date = my_data['date']
			self.time = my_data['time']
			self.shutterspeed = my_data['shutterspeed']
			self.fstop = my_data['fstop']


		if os.path.exists(self.thumb_path):
			self.thumbnail = self.thumb_path
		else:
			self.thumbnail = path

		if os.path.exists(self.raw_path):
			self.raw_path = self.raw_path
		else:
			self.raw_path = ""

		my_data['shutterspeed'] = self.shutterspeed
		my_data['date'] = self.date
		my_data['time'] = self.time
		my_data['fstop'] = self.fstop
		image_data[self.file_base_name] = my_data

	def thumb(self):
		return(self.thumbnail)


images = []
directory_contents = os.listdir(".")

for file in directory_contents:
	if os.path.split(file)[-1].split(".")[-1].lower() in ['jpg','jpeg']:
		my_image = image(file)
		images.append(my_image)

print "content-type:text/html"
print

print "<html>"
print "<h1>You can click any of these images to make them larger.</h1>"
for image in images:
	print "<a href='%s'><img src='%s' width=500></a>" % (image.fullsize,image.thumb())
	print "<br />"
	if image.raw_path != "":
		print "<a href=%s>Download the RAW camera data for this image</a>" % (image.raw_path)
	else:
		print "This image doesn't have a corresponding raw file...yet.  Maybe wait a bit for one? (Stuff is still uploading)"
	print "<br />"
	print "<div style='border: 1px solid #000000'>"
	print "Shutter Speed: %s (seconds)<br />" % (image.shutterspeed)
	print "F-Stop: %s<br />" % (image.fstop)
	print "Date: %s at %s <br />" % (image.date,image.time)
	print "<br />"
	print "</div>"

print "</html>"

pickle.dump( image_data, open( "image_data.p", "wb" ) )
