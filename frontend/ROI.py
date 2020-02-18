import cv2 as cv

VIDEO_NAME = '12.11.wmv'

def main():
    video = cv.VideoCapture(VIDEO_NAME)             # Open video and store in 'video'
    if video.isOpened() == False:
        print('Error opening video')
        quit()
        
    status, frame = video.read()                    # Read first frame
    
    if status == False:                             # Quit program if error
        print('Capture Error')
        quit()
    ROI = cv.selectROI('Select ROI', frame, False)  # Select ROI

    if ROI == (0, 0, 0, 0):                         # Quit program if cancelled
        print('No ROI Selected')
        quit()
    x, y, w, h = ROI                                # Store ROI location and size

if __name__ == '__main__':
    main()                               