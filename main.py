import cv2
#importing winsound to make a noise when bulgulary movement is detected
import winsound
#reading camera(webcam of laptop) and capturing video info in variable cam
cam = cv2.VideoCapture(0)
#turning on camera and using while loop

while cam.isOpened():
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()
        #we capture 2 respective instances of the webcam and find the diff b/w them , if diff=!0 then the object infromt of the cam has moved and motion is detected
    diff = cv2.absdiff(frame1, frame2)
    #converting diff color to grey color
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    #getting rid of the noise by setting the threshhold
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY )
    #using some dilation after getting rid of the noise to amplify the focus objects
    #passing thresh as paramter to be dilated and passing kernels= none and dilating 3 times
    dilated = cv2.dilate(thresh, None, iterations=3)
    #setting contours boxes around objects that are moving to detect them
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #drawing contours around frame1 , press -1 to draw everything, with rgb value green and thickness =2
    # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
    for c in contours:
        #setting condition to detect only big moving objects and neglecting minor details
        #if area < 5000 ignore that movement
        if cv2.contourArea(c) < 5000:
            continue
        #drawing contour box with parameter x,y,w,h
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x,y), (x+w, y+h), (0,255,0), 2)
        #calling winsound to make a beep noise with freq 500 and duration 200 msec
        winsound.Beep(500, 200)



    #waiting 10 secs to know whether user presses a key(q) on computer , if yes then destroy the window
    if cv2.waitKey(10) == ord('q'):
        break
    #activating webcam and displaying video
    cv2.imshow("security cam 1, press q to exit", frame1)

