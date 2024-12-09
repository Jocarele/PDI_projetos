## Exemplo: BLOOM 
#-------------------------------------------------------------------------------
# Autor: João Lucas M. Camilo
#        Viviane Ruotolo
# Universidade Tecnológica Federal do Paraná
#============================================

import numpy as np
import cv2
import sys

GREEN_IMAGE = "img/1.bmp"
PUT_IMAGE = "img/Wind Waker GC.bmp"

ANGULO_LIMIAR = 25
LIMIAR_BRANCO = 0.9
LIMIAR_PRETO = 0.1
#TODO A VERDISSE DEPENDE DA LUMINOSIDADE E DA SATURAÇÃO. ACHAR RELAÇÃO
def greeness(img):
        rows,cols,c = np.shape(img)
        img_verde = img.copy()
        #img_verde[:,:,1] = np.where((img[:, :, 0] > (120 - ANGULO_LIMIAR)) & (img[:, :, 0] < (120 + ANGULO_LIMIAR)), img[:, :, 1],0 )
        for row in range(0,rows):
                for col in range (0,cols):
                        img [row,col,2] = 1
        for row in range(0,rows):
                for col in range (0,cols):
                        #TInge de vermelho o que:
                        # Não é verde
                        # O que não é branco e o que não é preto
                        if not((img[row,col,1] > LIMIAR_PRETO and img[row,col,1] < LIMIAR_BRANCO)):
                                img_verde[row,col,0] = 1
                                img_verde[row,col,1] = 0.5
                                img_verde[row,col,2] = 1
                        elif not((img[row,col,0] > (120 - ANGULO_LIMIAR)) and (img[row,col, 0] < (120 + ANGULO_LIMIAR))):
                                img_verde[row,col,0] = 1
                                img_verde[row,col,1] = 0.5
                                img_verde[row,col,2] = 1       
                                
                        
                                

        return img_verde

def substituir(img,img2,img_verde):
        img [:,:,0]= np.where(img_verde[:,:,0]>10,img2[:,:,0],img[:,:,0])
        img [:,:,1]= np.where(img_verde[:,:,0]>10,img2[:,:,1],img[:,:,1])
        img [:,:,2]= np.where(img_verde[:,:,0]>10,img2[:,:,2],img[:,:,2])

def magnitude(img):
    cinza = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    dx = cv2.Sobel(cinza,cv2.CV_32F,1,0)
    dy = cv2.Sobel(cinza,cv2.CV_32F,0,1)
    mag = cv2.magnitude(dx,dy)
    #minimo = np.min(mag)
    #maximo = np.max(mag)
    #print(minimo,maximo)
    mag =cv2.normalize(mag,None,alpha=0,beta=1,norm_type=cv2.NORM_MINMAX)
    return mag

img = cv2.imread(GREEN_IMAGE)
img2 = cv2.imread(PUT_IMAGE)


if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

img = img.astype(np.float32)/255
#TODO: MASCARA PARA DETERMINAR O QUE É NECESSARIO SUBSTITUIR
#ALGORITMO PARA VERIFICAR SE É VERDE UTILIZANDO A MASCARA
# SE VERDE E BORDA, NÃO ULTRAPASSAR A BORDA.
# SE VERDE E NÃO BORDA, É VERDE(IMPROVAVEL QUE TROQUE DE COR DO NADA)
# MESMO ARGUMENTO VALE PARA NÃO VERDES
mag = magnitude(img)
cv2.imshow("-01 - mag",mag)

img2 = img2.astype(np.float32)/255
rows,cols,c = np.shape(img)
img2 = cv2.resize(img2,(cols,rows))
print(np.mean(img), np.median(img))

cv2.imshow("00 - original",img)

img = cv2.cvtColor(img,cv2.COLOR_BGR2HLS)
img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2HLS)

img_verde = greeness(img)
substituir(img,img2,img_verde)
img_verde = cv2.cvtColor(img_verde,cv2.COLOR_HLS2BGR)
img = cv2.cvtColor(img,cv2.COLOR_HLS2BGR)
img2 = cv2.cvtColor(img2,cv2.COLOR_HLS2BGR)
cv2.imshow("01 - verde",img_verde)
cv2.imwrite("01 - verde.png",img_verde*255)


cv2.imshow("02 - sub",img)
cv2.imwrite("02 - sub.png",img*255)




cv2.waitKey()