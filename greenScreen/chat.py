import numpy as np
import cv2

# Caminhos das imagens
GREEN_IMAGE = "img/4.bmp"
PUT_IMAGE = "img/Wind Waker GC.bmp"

# Leitura das imagens
img = cv2.imread(GREEN_IMAGE)
img2 = cv2.imread(PUT_IMAGE)

# Redimensionar img2 para as dimensões de img
rows, cols, c = img.shape
img2 = cv2.resize(img2, (cols, rows))

# Normalizar as imagens para o intervalo [0, 1]
img = img.astype(np.float32) / 255.0
img2 = img2.astype(np.float32) / 255.0

# Cálculo da "verdeza" (greeness)
greeness = img[:, :, 1] - np.maximum(img[:, :, 0], img[:, :, 2])
greeness = np.clip(greeness, 0, 1)  # Garante que os valores fiquem no intervalo [0, 1]
greeness = cv2.normalize(greeness, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

# Inverso da verdeza
greeness = 1 - greeness
#greeness_inv = np.repeat(greeness_inv[:, :, np.newaxis], 3, axis=-1)  # Expande para 3 canais

# Aplicar um filtro Gaussiano na verdeza
greeness = cv2.GaussianBlur(greeness, (0, 0), 1)

# Aplicar threshold na verdeza para destacar áreas relevantes
threshold = 0.86
greeness_threshold = np.where(greeness < threshold, 0, greeness)
greeness_threshold = np.repeat(greeness_threshold[:, :, np.newaxis], 3, axis=-1)  # Expande para 3 canais

# Combinar img com a máscara verde
img_parcial = np.where(greeness_threshold < threshold, 0, img)

# Combinar img_parcial e img2 para criar o resultado final
img_final = img_parcial * greeness_threshold + img2 * (1 - greeness_threshold)

# Visualizar e salvar os resultados
cv2.imshow("Greeness", greeness)
cv2.imwrite("Greeness.png", (greeness * 255).astype(np.uint8))

#cv2.imshow("Greeness Inverse", greeness_inv)
#cv2.imwrite("Greeness_Inverse.png", (greeness_inv * 255).astype(np.uint8))

cv2.imshow("Image Partial", img_parcial)
cv2.imwrite("Image_Partial.png", (img_parcial * 255).astype(np.uint8))

cv2.imshow("Final Image", img_final)
cv2.imwrite("Final_Image.png", (img_final * 255).astype(np.uint8))

cv2.waitKey(0)
cv2.destroyAllWindows()
