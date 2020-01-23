import cv2
from PIL import Image
import os
import shutil
import sys

#Default frame interval for Mister M.
frameinterval = 192
#Default black borders position for Mister M.
borderposition = (159, 0, 1121, 720)

cap = cv2.VideoCapture(sys.argv[1])
#Creates temp folder to store images inside
os.mkdir('temp')
print('Stealing slides, please wait...')
pageslist = []
currframe = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    if (currframe != 0) & (currframe%frameinterval == 0):
        #Saves image to temp folder
        cv2.imwrite('temp/' + str(len(pageslist)) + '.jpg',frame)
        #Reads image from temp folder (yes, it's inevitable)
        slide = Image.open(r'temp/' + str(len(pageslist)) + '.jpg')
        #Crops image based on input values
        croppedslide = slide.crop(borderposition)
        rgbslide = croppedslide.convert('RGB')
        #First image must be kept separate from the others
        if currframe == frameinterval:
            firstscreen = rgbslide
        #All the other images must be put in a list
        else:
            pageslist.append(rgbslide)
    currframe+=1

#Classic buffer emptying
cap.release()
cv2.destroyAllWindows()

#Gives a new cool name (or rather, just changes extention)
newname = sys.argv[1].replace('.mp4', '.pdf')
firstscreen.save(r'' + newname, save_all=True, append_images=pageslist)
#Deletes temp folder
shutil.rmtree('temp')
print('DONE! Enjoy your free, brand new slides')