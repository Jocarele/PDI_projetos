## Exemplo: BLOOM 
#-------------------------------------------------------------------------------
# Autor: João Lucas M. Camilo
#        Viviane Ruotolo
# Universidade Tecnológica Federal do Paraná
#============================================

import numpy as np
import cv2
import sys

GREEN_IMAGE = "img/4.bmp"
PUT_IMAGE = "img/Wind Waker GC.bmp"

ANGULO_LIMIAR = 60
LIMIAR_BRANCO = 0.80196
LIMIAR_PRETO = 0.298039


#TODO A VERDISSE DEPENDE DA LUMINOSIDADE E DA SATURAÇÃO. ACHAR RELAÇÃO
def greeness(img):
	rows,cols,c = np.shape(img)
	img_verde = img.copy()
	#img_verde[:,:,1] = np.where((img[:, :, 0] > (120 - ANGULO_LIMIAR)) & (img[:, :, 0] < (120 + ANGULO_LIMIAR)), img[:, :, 1],0 )

	for row in range(0,rows):
		for col in range (0,cols):
			#TInge de vermelho o que:
			# Não é verde
			# O que é branco e o que é preto
						
			if not((img[row,col,1] > LIMIAR_PRETO and img[row,col,1] < LIMIAR_BRANCO)):
				img_verde[row,col,0] = 1
				img_verde[row,col,1] = 0.5
				img_verde[row,col,2] = 1
				
			if not((img[row,col,0] > (120 - ANGULO_LIMIAR)) and (img[row,col, 0] < (120 + ANGULO_LIMIAR))):
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
	cinza = cv2.normalize(cinza,None,alpha=0,beta=1,norm_type=cv2.NORM_MINMAX)


	cv2.imshow("01 - mag.png",cinza)
	cinza = (cinza * 255).astype(np.uint8)


	#dx = cv2.Sobel(cinza,cv2.CV_32F,1,0)
	#dy = cv2.Sobel(cinza,cv2.CV_32F,0,1)
   # mag = cv2.magnitude(dx,dy)
	#minimo = np.min(mag)
	#maximo = np.max(mag)
	#print(minimo,maximo)
	#mag =cv2.normalize(mag,None,alpha=0,beta=1,norm_type=cv2.NORM_MINMAX)
	cinza = cv2.GaussianBlur(cinza, (0,0), 3)

	mag = cv2.Canny(cinza, 20, 100)
	cv2.imwrite("01 - mag.png",mag)

	return mag

def catch_borda(copia,img,img2,mag): 
	rows,cols,c = np.shape(img)
	img_verde = img.copy()        
	for row in range(0,rows):
		for col in range (0,cols):
			if(mag[row,col] > 100):
				img[row,col] = img2[row,col]
	return img

def greenessRGB(img):
	rows,cols,c = np.shape(img)
	img_verde = img.copy()
	#img_verde[:,:,1] = np.where((img[:, :, 0] > (120 - ANGULO_LIMIAR)) & (img[:, :, 0] < (120 + ANGULO_LIMIAR)), img[:, :, 1],0 )
	limiar_baixo = 128
	limiar_alto = 200
	img_blur = cv2.blur(img, ksize=(81,81))
	for row in range(0,rows):
		for col in range (0,cols):
			#B G R
			#TODO: ESTATISTICA VERIFICAR LIMIAR VERDE, AZUL E VERMELHO
			vermelho = abs(-float(img[row,col,2]) + float(img_blur[row,col,2]))
			azul = abs(-float(img[row,col,0]) + float(img_blur[row,col,0]))
			if(img[row,col,0]<limiar_baixo and img[row,col,1]<limiar_baixo and img[row,col,2]<limiar_baixo):
				img_verde[row,col,0] = 0
				img_verde[row,col,1] = 0
				img_verde[row,col,2] = 255
			elif(img[row,col,0]>limiar_alto and img[row,col,1]>limiar_alto and img[row,col,2]>limiar_alto):
				img_verde[row,col,0] = 0
				img_verde[row,col,1] = 0
				img_verde[row,col,2] = 255
			elif(img[row,col,0]< float(img[row,col,1])-azul and img[row,col,1]>limiar_baixo and 
																	img[row,col,2]< float(img[row,col,1])-vermelho):
				img_verde[row,col,0] = 0
				img_verde[row,col,1] = 255
				img_verde[row,col,2] = 0
			else:
				img_verde[row,col,0] = 0
				img_verde[row,col,1] = 0
				img_verde[row,col,2] = 255
		
	cv2.imshow("RGB2",img)
	cv2.imwrite("RGB.png",img_verde)
		
	cv2.imshow("RGB",img_verde)
	return img_verde



img = cv2.imread (GREEN_IMAGE)
img2 = cv2.imread (PUT_IMAGE)

rgb_verde = greenessRGB(img)
magRGB = magnitude(rgb_verde)
cv2.imshow("magRGB",magRGB)


if img is None:
		print ('Erro abrindo a imagem.\n')
		sys.exit ()

img = img.astype(np.float32)/255
img2 = img2.astype(np.float32)/255


#img = cv2.normalize(img,None,alpha=0,beta=1,norm_type=cv2.NORM_MINMAX)
#img2 = cv2.normalize(img,None,alpha=0,beta=1,norm_type=cv2.NORM_MINMAX)
#mag = magnitude(img)
#cv2.imshow("-01 - mag",mag)




rows,cols,c = np.shape(img)
img2 = cv2.resize(img2,(cols,rows))

cv2.imshow("00 - original",img)

img = cv2.cvtColor(img,cv2.COLOR_BGR2HLS)
img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2HLS)
copia = img.copy()

img_verde = greeness(img)
mag = magnitude(img_verde)
substituir(img,img2,img_verde)
img = catch_borda(copia,img,img2,mag)
#substituir(img,img2,img_verde)
img_verde = cv2.cvtColor(img_verde,cv2.COLOR_HLS2BGR)
img = cv2.cvtColor(img,cv2.COLOR_HLS2BGR)
img2 = cv2.cvtColor(img2,cv2.COLOR_HLS2BGR)
#cv2.imshow("01 - verde",img_verde)
cv2.imwrite("01 - verde.png",img_verde*255)


#cv2.imshow("02 - sub",img)
cv2.imwrite("02 - sub.png",img*255)




cv2.waitKey()