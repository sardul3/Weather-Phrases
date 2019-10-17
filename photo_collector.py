import re
import os
import shutil
import glob
import datetime
from datetime import date
from os import listdir
from PIL import Image

photo_path = "/mnt/idrive/photos/MHK_Camera"
archive_path = photo_path + "/archive"
slideshow = "/var/www/html/slideshow"
os.chdir(photo_path)
#print(os.getcwd())
cur = os.getcwd()

#
mhk_list = os.listdir(photo_path)
mhk_list.sort()
mhk_list.reverse()

today = datetime.date.today()
#print(today)
day = datetime.timedelta(hours = 24)
past_day = today - day
#print(past_day)
print("Today's date: " + str(datetime.datetime.now()))

for filename in mhk_list:
    if '.jpg' in filename:
        path = os.path.join(photo_path, filename)
        #print(path)
        if os.path.isdir(path):
            continue
        else:
            #print(filename)
            if str(today) in filename:
                #print(filename)
                source = "/mnt/idrive/photos/MHK_Camera/" + filename
                dest = "/mnt/idrive/photos/MHK_Camera/archive/" + filename
                shutil.copy(source, dest)
                dest2 = "/var/www/html/slideshow/images/"
                shutil.copy(source, dest2)
            else:
                if str(past_day) in filename:
                    source = "/mnt/idrive/photos/MHK_Camera/" + filename
                    dest = "/mnt/idrive/photos/MHK_Camera/archive/" + filename
                    shutil.copy(source, dest)
                    dest2 = "/var/www/html/slideshow/images/"
                    shutil.copy(source, dest2)
                else:
                    remove = os.path.join(archive_path, filename)
                    continue


a = glob.glob("archive/*.jpg")
a.sort()
b = a.reverse()
#print(a[:48])
for image in a[48:]:
    #print(image)
    old = os.path.join(photo_path, image)
    os.remove(old)


new = glob.glob("archive/*.jpg")
for images in new:
    loc = os.path.join(photo_path, images)
    f = open(loc, "rb")
    byte = f.read()
    f.close()

    matchObj = re.match( b'\xff\xd8.*\xff\xc0...(..)(..).*\xff\xd9', byte, re.MULTILINE|re.DOTALL)
    if matchObj:
#       # http://stackoverflow.com/questions/444591/convert-a-string-of-bytes-into-an-int-python
        #print (int.from_bytes(matchObj.group(1), 'big')) # height
        #print (int.from_bytes(matchObj.group(2), 'big')) # width
        #print("Image not corrupt")
        continue
    else:
        #print("Corrupt file: " + images)
        newimage = images.split('/')[1]
        #print(newimage)
        ci = os.path.join(archive_path, newimage)
        os.remove(ci)
        source = "/mnt/idrive/photos/MHK_Camera/corrupt_image_file.jpg"
        dest = "/mnt/idrive/photos/MHK_Camera/archive/" + newimage
        shutil.copy(source, dest)
        #print(dest)



new_cur = os.chdir(slideshow)
#print(os.getcwd())

c = glob.glob("images/*.jpg")
c.sort()
d = c.reverse()
#print(c[:48])
for pics in c[48:]:
    old_pics = os.path.join(slideshow, pics)
    os.remove(old_pics)


new_glob = glob.glob("images/*.jpg")
for images2 in new_glob:
    loc2 = os.path.join(slideshow, images2)
    f2 = open(loc2, "rb")
    byte2 = f2.read()
    f2.close()

    matchObj2 = re.match( b'\xff\xd8.*\xff\xc0...(..)(..).*\xff\xd9', byte2, re.MULTILINE|re.DOTALL)
    if matchObj2:
        # http://stackoverflow.com/questions/444591/convert-a-string-of-bytes-into-an-int-python
        #print("Image not corrupt")
        continue
    else:
        #print("Corrupt file: " + images2)
        newimage2 = images2.split('/')[1]
        #print(newimage2)
        ci2 = os.path.join(slideshow, images2)
        os.remove(ci2)
        os.chdir(photo_path)
        source = "/mnt/idrive/photos/MHK_Camera/corrupt_image_file.jpg"
        dest = "/var/www/html/slideshow/images/" + newimage2
        shutil.copy(source, dest)
        #print(dest)


print("finished code successfully")
