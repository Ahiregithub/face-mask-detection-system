import cv2

video=cv2.VideoCapture(0)
facedetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:

ret, frame=video.read()
faces=facedetect.detectMultiScale(frame,1.3, 5)
for x,y,w,h in faces:
cv2.rectangle(frame, (x,y), (xw, y=h), (0,255,0),3)
cv2.imshow("WindowFrame", frame)
k=cv2.waitkey(1)
if k==ord('q'):
break
video.release()
cv2.destroyAllWindows ()
