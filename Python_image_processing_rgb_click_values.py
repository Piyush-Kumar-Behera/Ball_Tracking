import cv2

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(img1[y][x])

cam = cv2.VideoCapture(0)

#img = cv2.imread('C:/Users/piyus/Desktop/Red-green-blue_flag.jpeg')
#cv2.namedWindow("Videofeed",cv2.WINDOW_NORMAL)
#cv2.resizeWindow("Videofeed",1200,800)

abc,frame = cam.read()
cv2.imshow("VideoFeed",frame)
#cv2.imshow("Image",img)
img1=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

cv2.setMouseCallback("VideoFeed",click_event)

