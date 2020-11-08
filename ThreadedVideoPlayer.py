#!/usr/bin/env python3
# Author: Julian Gonzalez
import cv2
import os
import time
import threading
import queue
from ThreadedQueue import ThreadedQueue


## Global
videoName = 'clip.mp4'
inputQueue = ThreadedQueue()#queue.Queue()
OutputQueue = ThreadedQueue()#queue.Queue()


## Code snippet from ExtractAndDisplay.py provided by CS4375
def extractFrames(fileName, outputBuffer, maxFramesToLoad=9999):
    # Initialize frame count 
    count = 0

    # open video file
    vidcap = cv2.VideoCapture(fileName)

    # read first image
    success,image = vidcap.read()
    
    print(f'Reading frame {count} {success}')
    while success and count < maxFramesToLoad:
        
        # get a jpg encoded frame
        success, jpgImage = cv2.imencode('.jpg', image)

        # add the frame to the buffer
        outputBuffer.put(image)
       
        success,image = vidcap.read()
        print(f'Reading frame {count} {success}')
        count += 1
        

    print('Frame extraction complete')


## Code snippet from ExtractAndDisplay.py provided by CS4375    
def displayFrames(outputBuffer):
    # initialize frame count
    count = 0

    # go through each frame in the buffer until the buffer is empty
    while outputBuffer is not None:
        
        # get the next frame
        frame = OutputQueue.get()

        print(f'Displaying frame {count}')        

        # display the image in a window called "video" and wait 42ms
        # before displaying the next frame
        cv2.imshow('Video', frame)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        count = count + 1

    print('Finished displaying all frames')
    # cleanup the windows
    cv2.destroyAllWindows()

## Some code snippet from ConvertToGrayScale.py modified into method
def ConvertToGrayScale(inputQueue,OutputQueue,maxFramesToLoad=9999):
    
    # initialize frame count
    count = 0
    
    while inputQueue is not None and count < 72:# can change 72?
        
        print(f'Converting frame {count}')

        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(inputQueue.get(), cv2.COLOR_BGR2GRAY)
        
        count = count + 1
        
        OutputQueue.put(grayscaleFrame)



###Start threads
extractThread = threading.Thread(target = extractFrames, args = (videoName, inputQueue,72))
convertThread = threading.Thread(target = ConvertToGrayScale, args = (inputQueue, OutputQueue,72))
displayThread = threading.Thread(target = displayFrames, args = (OutputQueue,))

extractThread.start()
convertThread.start()
displayThread.start()
