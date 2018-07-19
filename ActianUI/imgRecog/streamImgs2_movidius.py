#!/usr/bin/env python3
from time import sleep
from picamera import PiCamera
import os
import sys
import shutil
import v1_image_classifier as classifier
#sys.path.insert(0, '/usr/local/psql/FlightData_db')
#import b2_images as btrieve2
#print(os.getcwd())
#btrieve2.selectImages()
camera = PiCamera()
camera.resolution = (1024, 768)


device = classifier.open_ncs_device()
graph = classifier.load_graph( device )
def infer(imgLocation):
    img_draw = classifier.skimage.io.imread(imgLocation)
    img = classifier.pre_process_image( img_draw )
    inferanceOutput = classifier.infer_image( graph, img )
    return(inferanceOutput)
	

def stream2_movidius():
    for i in range(10):
        print('------------------------------')
        print('brace for image capture')
        sleep(1)
        print('3')
        sleep(1)
        print('2')
        sleep(1)
        print('1')
        #os.remove('/tmp/imagenet/foo.jpg')
        os.rename('/home/pi/Desktop/foo.jpg', '/home/pi/Desktop/oldImages/foo.jpg')
        imgloc = '/home/pi/Desktop/foo.jpg'
        camera.capture(imgloc)
        #comment this out until you test how the api responds to image feed
        guesses = infer(imgloc)
        for i in range(len(guesses[0])):
            if ( ('mouse' in guesses[0][i]) or ('computer' in guesses[0][i]) or \
                 ('keyboard' in guesses[0][i]) or ('mechanical' in guesses[0][i])):
                match = guesses[0][i]
                print(match)
                #btrieve2.insertImage('/tmp/imagenet/foo.jpg : ' + match)
                #btrieve2.selectImages()
        i = i + 1

if __name__ == "__main__":
    #img = '/home/pi/Desktop/foo2.jpg'
    #infer(img)
    stream2_movidius()
    classifier.close_ncs_device( device, graph )

