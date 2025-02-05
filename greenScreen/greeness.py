## Exemplo: BLOOM 
#-------------------------------------------------------------------------------
# Autor: João Lucas M. Camilo
#        Viviane Ruotolo
# Universidade Tecnológica Federal do Paraná
#============================================

import numpy as np
import cv2


GREEN_IMAGE = "img/3.bmp"
PUT_IMAGE = "img/Wind Waker GC.bmp"

img = cv2.imread (GREEN_IMAGE)
img2 = cv2.imread (PUT_IMAGE)


rows,cols,c = np.shape(img)
img2 = cv2.resize(img2,(cols,rows))

img2 = img2.astype(np.float32)/255.0


img = img.astype(np.float32)/255.0

greeness = (img[:, :, 1] - np.maximum(img[:, :, 0], img[:, :, 2]))

greeness = np.clip(greeness,0,1)
greeness =cv2.normalize(greeness,None,alpha=0,beta=1,norm_type=cv2.NORM_MINMAX)
greeness_inv = (1-greeness)- img[:,:,1]
greeness_inv = np.repeat(greeness_inv[:, :, np.newaxis], 3, axis=-1)  # Expande para (992, 1908, 3)


greeness_inv = np.clip(greeness_inv,0,1)
greeness_inv =cv2.normalize(greeness_inv,None,alpha=0,beta=1,norm_type=cv2.NORM_MINMAX)
greeness_inv = cv2.GaussianBlur(greeness_inv, (0,0), 3)


cv2.imshow("G-RB",greeness)
cv2.imwrite("G-RB.png",greeness*255)
cv2.imshow("G-RB_inv",greeness_inv)
cv2.imwrite("G-RB_inv.png",greeness_inv*255)






#img_parcial = np.where(greeness_inv >0.7,img, 0)
img_parcial = greeness_inv * img



img_final =img_parcial +img2*(1-greeness_inv)
print(1-greeness_inv[480,748,1])
cv2.imshow("IMG", 1-greeness_inv)
cv2.imwrite("IMG.png", greeness*255)
cv2.imshow("IMG_parcial", img_parcial)
cv2.imwrite("IMG_parcial.png", img_parcial*255)

cv2.imshow("IMG_final", img_final)
cv2.imwrite("IMG_final.png", img_final*255)

cv2.waitKey()
cv2.destroyAllWindows()