import cv2 as cv

img = cv.imread('diff-colors-img.png', 1)
img2 = cv.cvtColor(img, cv.COLOR_BGR2RGB)
img3 = cv.cvtColor(img2, cv.COLOR_RGB2HSV)

umbralBajo=(0, 80, 80  )
umbralAlto=(10, 255, 255)
umbralBajoB=(170, 80,80)
umbralAltoB=(180, 255, 255)

umbralBajoC=(90, 80,80)
umbralAltoC=(130, 255, 255)


mascara1 = cv.inRange(img3, umbralBajo, umbralAlto)
mascara2 = cv.inRange(img3, umbralBajoB, umbralAltoB)

mascara3 = cv.inRange(img3, umbralBajoC, umbralAltoC)


mascara = mascara1 + mascara2 + mascara3

resultado = cv.bitwise_and(img, img, mask=mascara)

cv.imshow('mascara', mascara)
cv.imshow('img',img)

cv.waitKey(0)
cv.destroyAllWindows()