import cv2 

def rescale_frame(frame, height_scale, width_scale):

    """
    Helper function to resize the video frame
    Scales the height and length of the frame based on the "res" parameter (which is a value from 0-100)
    """
    scaled_dims = (int(frame.shape[0] * height_scale/100), int(frame.shape[1] * width_scale/100) )
    return cv2.resize(frame,scaled_dims,interpolation=cv2.INTER_AREA)

def test_track():
    
    # Load tracking video 
    video   = cv2.VideoCapture("DJI_0003.MP4")

    video.set(3,640)
    video.set(4,480)

    #Initialize KCF tracker 
    tracker = cv2.TrackerKCF_create()

    # Read first frame of the video and select ROI 
    _, frame = video.read()

    # Rescale frame
    frame = rescale_frame(frame,90,30)
    roi = cv2.selectROI(frame,showCrosshair=False)

    # Initialize tracker with ROI bounding box 
    tracker.init(frame,roi)

    while 1:  

        frameExists, frame = video.read()
        # Exit the loop at the end of the video
        if not frameExists: break 

        # Rescale frame
        frame = rescale_frame(frame,90,30)

        # Measure time before tracking calculation
        time_before = cv2.getTickCount()

        # Update the tracker for the current frame 
        trackingValid, roi_updated = tracker.update(frame)

        # If the object was found, draw bounding box - if not, display error msg
        if trackingValid:
            p1 = (int(roi_updated[0]), int(roi_updated[1]))
            p2 = (int(roi_updated[0] + roi_updated[2]), int(roi_updated[1] + roi_updated[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else:
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)


        # Display result
        cv2.imshow("Tracking", frame)

        # break if user presses key
        key = cv2.waitKey(1) & 0xFF
        if key == 27: break

if __name__ == "__main__":
    test_track()