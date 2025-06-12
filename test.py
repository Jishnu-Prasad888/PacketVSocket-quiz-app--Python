import cv2

cam = cv2.VideoCapture(0)
ret, frame = cam.read()
if ret:
    cv2.imshow("Test", frame)
    cv2.waitKey(0)
else:
    print("Cannot access webcam")
cam.release()
cv2.destroyAllWindows()
