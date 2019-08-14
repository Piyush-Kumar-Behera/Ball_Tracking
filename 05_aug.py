# Import openCV library and imutils library
import cv2
import imutils

def search_ball():
    pass

# Need to be modified according to pi cam
cam = cv2.VideoCapture(0)

# Assuming ball radius to be 6...To be modified
ball_radius_in_cm = 6
app_radius_in_pix = 150
distance_in_cm = 15

focal_len = (app_radius_in_pix * distance_in_cm) / ball_radius_in_cm

# The lower and upper hsv limits for the masking
greenLower = (50, 60, 20)
greenUpper = (75, 255, 255)

x1 = -1
y1 = -1
radius1 = -1

x2 = 0
y2 = 0
radius2 = 1

# This while loop is the starter of the code and runs immediately as pi is switched on.
# The while loop is getting all the contours captured in the pi cam and then selects the contour having maximum area
# So it is necessary that the ball is kept close to the pi cam,and possess the maximum area

while x1 == -1:
    abc, frame = cam.read()
    areacont = [0] * 200
    dist = [100000] * 200

    frame = imutils.resize(frame, width=600)
    blurr = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurr, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=1)
    mask1 = mask

    contour = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = imutils.grab_contours(contour)
    radius = 0

    lent = len(contour)
    if lent > 0:
        for i in range(lent):
            cont_ind = contour[i]
            areacont[i] = cv2.contourArea(cont_ind)
        cont1_pos = areacont.index(max(areacont))
        cont_final = contour[cont1_pos]

        ((x1, y1), radius1) = cv2.minEnclosingCircle(cont_final)
        # print((x1,y1))
    elif lent is 0:
        search_ball()
    if radius1 > 10:
        cv2.circle(frame, (int(x1), int(y1)), int(radius1), (0, 255, 255), 2)

print(str(x1) + " " + str(y1))

# After the ball is tracked once, this while loop tracks the ball as the contour
# that is nearest to the contour in the previous frame,
# if the ball looses the track of ball that is has no contour on scree it calls search ball function to execute
while True:
    dist = [100000] * 200
    abc, frame = cam.read()
    frame = imutils.resize(frame, width=600)
    blurr = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurr, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=1)
    mask1 = mask

    contour = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = imutils.grab_contours(contour)
    radius = 0

    lent = len(contour)
    if lent > 0:
        for i in range(lent):
            cont_ind = contour[i]
            ((x2, y2), radius2) = cv2.minEnclosingCircle(cont_ind)
            dist[i] = abs(x2 - x1)

        cont2_pos = dist.index(min(dist))
        # print(lent,"  ",cont2_pos)
        cont2 = contour[cont2_pos]
        ((x2, y2), radius2) = cv2.minEnclosingCircle(cont2)

    elif lent is 0:
        search_ball()

    if radius2 > 10:
        cv2.circle(frame, (int(x2), int(y2)), int(radius2), (0, 255, 255), 2)


    distance = (focal_len * ball_radius_in_cm) / (2 * radius1)


    #print(distance)

    x1 = x2
    y1 = y2
    radius1 = radius2

    cv2.imshow("Image1", mask)
    cv2.imshow("Image", frame)

    h = cv2.waitKey(10)
    if not h == -1:
        break;

cam.release()
cv2.destroyAllWindows()
