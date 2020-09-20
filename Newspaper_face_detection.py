import zipfile
from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np

face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
images = {}
name_list = []

def unzip_images(zip_name):
    # extracting zipfile
    zip_file = zipfile.ZipFile(zip_name)
    for things in zip_file.infolist():
        images[things.filename] = [Image.open(zip_file.open(things.filename))]
        name_list.append(things.filename)

if __name__ == '__main__':
    unzip_images('small_img.zip')
    for name in name_list:
        img = images[name][0]
        
        # deleting line seperators
        images[name].append(pytesseract.image_to_string(img).replace('-\n',''))
        
        # modifying global data structure to append text on images 
        if 'Mark' in images[name][1]: 
            print('Results found in file',name)
            try:
                # storing the detected faces on images that has been marked with boxes
                faces = (face_cascade.detectMultiScale(np.array(img),1.35,4)).tolist()
                
                # appending detected faces to global data structure
                images[name].append(faces)
                faces_in_files = []
                for x,y,w,h in images[name][2]:
                    # appending to local data structure to store PIL image of detected faces
                    faces_in_files.append(img.crop((x,y,x+w,y+h)))
                    # creating a contact sheet to display detected faces
                    contact_sheet = Image.new(img.mode, (550,110*int(np.ceil(len(faces_in_files)/5))))
                    x = 0
                    y = 0
                    for face in faces_in_files:
                        # resizing images using PIL.Image.thumbnail function
                        face.thumbnail((110,110))
                        contact_sheet.paste(face, (x, y))
                        if x+110 == contact_sheet.width:   
                            x=0
                            y+=110
                        else :
                            x+=110
                    contact_sheet.show()
            except:
                    print('But there were no faces in that file!')



                











