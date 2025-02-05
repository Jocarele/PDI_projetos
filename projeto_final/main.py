import numpy as np
import cv2
import subprocess
#TODO : ESTOU TENTANDO FAZER ESTE CODIGO COM A MASCARA INTEIRA, SEM AS BORDAS
#AGR EDGE É A MASCARA, POR PREGUIÇA

#TODO: Procurar ao redor do 1 pixel achado ( que a probabilidade dele estar por perto é alta), e sortear
#alguns pixels na imagem, para caso tenha um melhor na imagem

NEGATIVE = 1
INPUT_IMAGE = "GT2.bmp"
MASK_IMAGE = "mask.png"
JANELA = 3


def cria_mascara():

    input_path = INPUT_IMAGE
    output_path = MASK_IMAGE

    command = ["pimask", "--input", input_path, "--output", output_path]

    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print("Criando mascara")
        print(result.stdout) 
    except subprocess.CalledProcessError as e:
        print("Erro ao criar mascara")
        print(e.stderr) 
    return 


def binariza (img, threshold):
    ''' Binarização simples por limiarização.

Parâmetros: img: imagem de entrada. Se tiver mais que 1 canal, binariza cada
              canal independentemente.
            threshold: limiar.
            
Valor de retorno: versão binarizada da img_in.'''

    img= np.where( img < threshold,0,255)
    return img.astype(np.uint8)

def contorno(img):
    kernel = np.ones((3,3), dtype=np.uint8)
    img2 = cv2.erode(img,kernel)
    edge = img - img2
    return img2,edge

def calcula_score(img, edge, row, col, row2, col2,rows,cols,mask):
    score = 0.0
    for i in range(-JANELA, JANELA + 1):
        for j in range(-JANELA, JANELA + 1):
            for c in range(3):
                # Exclui pixels que estao na mascara no somatório.
                if range_permitido(rows, cols, i, j, row, col) or edge[row + i, col + j] != 0 or mask[row + i, col + j] != 0:
                    continue 

                # Pixel que contem a mascara na janela deslizantes não são analisadas.
                if range_permitido(rows, cols, i, j, row2, col2) or mask[row2 + i, col2 + j] != 0:
                    return None  # Pixel invalido
                score += abs(float(img[row + i, col + j, c]) - float(img[row2 + i, col2 + j, c]))
    return score


def range_permitido(rows,cols,i,j,row,col):
    return row + i < 0 or row + i >= rows or col + j < 0 or col + j >= cols

def similiaridade(img,img2,edge,mask):
    rows,cols,_ = np.shape(img)
    print(rows,cols)
    #Procura pixel branco da mascara
    for row in range(0,rows):
        #print("row",row)
        for col in range (0,cols):
            if edge[row,col] == 0:
                continue
             
            #PERCORRER A IMAGEM
            valores = []
            scoreMin = float("inf")
            for row2 in range(0,rows):
                for col2 in range (0,cols):
                    if edge[row2, col2] != 0:
                        continue
                    score = 0.0
                    score = calcula_score(img2, edge, row, col, row2, col2,rows,cols,mask)
                    if score:
                        if scoreMin > score:
                            valores = [score,row,col,row2,col2]
                            scoreMin = score
            
                    #Row,col é a posição do pixel a ser substituido
                    #row2,col2 são a posição do pixel ideal para substituir
                    
            if valores:
                img2[valores[1],valores[2]] = img2[valores[3],valores[4]]
                edge[valores[1],valores[2]]= 0

    return img2
            
def main():
    cria_mascara()
    
    mask = cv2.imread(MASK_IMAGE, cv2.IMREAD_GRAYSCALE)


    img = cv2.imread(INPUT_IMAGE)

    rows,cols,_ =np.shape(img)

    if NEGATIVE == 1:
        mask = 255 - mask

    mask = binariza(mask,200)


    #---------------------FECHAMENTO DA MASCARA
    #TODO: As mascaras não conseguem ter formato S

    kernel = np.ones((250,250), dtype=np.uint8)#carro = 250
    mask = cv2.dilate(mask,kernel)
    #cv2.imshow("img0",img)
    mask = cv2.erode(mask,kernel)

    cv2.imshow("img",mask)
    cv2.imwrite("mascara.png",mask)

    #-----------------------------------------------------

    
    img = cv2.resize(img,(int(cols/8),int(rows/8)))
    mask = cv2.resize(mask,(int(cols/8),int(rows/8)))

    edge = mask.copy()
    img2 = img.copy()
    #EDGE É A ORDEM DE EXPLORAÇÃO DA MASCARA
    #MASK É A MASCARA PARA SER SUBSTITUIDA. 
    #é nessesário passar ambas para similiridade pois não podemos comparar os pixels que estão na mascara
    # após analizar o pixel da mascara, é necessário remover o pixel da mascara.
    while (np.max(mask)!= 0):
        mask,edge = contorno(mask)

        img2 = similiaridade(img,img2,edge,mask)
    

    img2 = cv2.resize(img2,(int(cols),int(rows)))
    img = cv2.resize(img,(int(cols),int(rows)))
    #mask = cv2.resize(mask,(int(rows/4),int(cols/4)))
    #cv2.imshow("contorno",edge)
    cv2.imwrite("resultado4.png",img2)

    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()