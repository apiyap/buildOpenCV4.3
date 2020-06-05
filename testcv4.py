import numpy as np
import cv2

#gst-launch-1.0 nvarguscamerasrc sensor_id=0 ! \
#   'video/x-raw(memory:NVMM),width=3280, height=2464, framerate=21/1, format=NV12' ! \
#   nvvidconv flip-method=0 ! 'video/x-raw,width=960, height=720' ! \
#   nvvidconv ! nvegltransform ! nveglglessink -e

def gstreamer_pipeline(
    camera_index=0,
    capture_width=1920,
    capture_height=1080,
    framerate=21,
    flip_method=0,
    display_width=960,
    display_height=720,
):
    return (
        "nvarguscamerasrc sensor_id=%d ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            camera_index,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

print(gstreamer_pipeline(camera_index=1,flip_method=0))
cam0 = cv2.VideoCapture(gstreamer_pipeline(camera_index=0,flip_method=0),cv2.CAP_GSTREAMER)
cam1 = cv2.VideoCapture(gstreamer_pipeline(camera_index=1,flip_method=0),cv2.CAP_GSTREAMER)

while(cam0.isOpened() and cam1.isOpened()):
    ret0, frame0 = cam0.read()
    ret1, frame1 = cam1.read()
    if ret0 and ret1:
#        frame = cv2.flip(frame,0)
        frame_stack = np.hstack((frame0,frame1))
        cv2.imshow('frame',frame_stack)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
# Release everything if job is finished
cam0.release()
cam1.release()
cv2.destroyAllWindows()
