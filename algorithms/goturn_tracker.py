import cv2 
from cv2_scratch import rescale_frame


if __name__ == "__main__":

    # Load video and create bounding box     
    video = cv2.VideoCapture("DJI_0003.MP4")
    video.set(3,640)
    video.set(4,480)

    _, initframe = video.read()
    initframe = rescale_frame(initframe,90,30) # rescale frame to make it easier to see on the computer screen

    bbox = cv2.selectROI(initframe, showCrosshair=False)

    #Create and initialize GoTURN based tracker using video frame and bbox coords
    tracker_DL = cv2.TrackerGOTURN_create()
    tracker_DL.init(initframe, bbox)

    while True:

        # Read a new frame
        ok, frame = video.read()
        frame = rescale_frame(frame,90,30)


        if not ok: break

        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = tracker_DL.update(frame)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        # Draw bounding box
        if ok:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)

        else :
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            cv2.putText(frame, "GOTURN Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)

        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)

        # Display result
        cv2.imshow("Tracking", frame)

        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

