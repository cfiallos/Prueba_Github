import cv2
import matplotlib.pyplot as plt

class ImageProcessor:
    def __init__(self, ruta):
        self.ruta = ruta
        self.imagen_original = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
        if self.imagen_original is None:
            raise ValueError(f"No se pudo cargar la imagen desde la ruta: {ruta}")
        self.imagen_umbralizada_simple = None
        self.imagen_umbralizada_adaptativa = None

    def mostrar_imagen(self, imagen, titulo):
        plt.imshow(imagen, cmap='gray')
        plt.title(titulo)
        plt.axis('off')
        plt.show()

    def umbralizacion_simple(self, umbral=127, maxvalue=255):
        _, self.imagen_umbralizada_simple = cv2.threshold(self.imagen_original, umbral, maxvalue, cv2.THRESH_BINARY)
        return self.imagen_umbralizada_simple

    def umbralizacion_adaptativa(self, maxvalue=255, window_size=11, constante=5):
        self.imagen_umbralizada_adaptativa = cv2.adaptiveThreshold(self.imagen_original, maxvalue, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, window_size, constante)
        return self.imagen_umbralizada_adaptativa

    def procesar_imagen(self):
        self.mostrar_imagen(self.imagen_original, 'Imagen Original Escala de Grises')

        self.umbralizacion_simple()
        self.mostrar_imagen(self.imagen_umbralizada_simple, 'Umbralización Simple')

        self.umbralizacion_adaptativa()
        self.mostrar_imagen(self.imagen_umbralizada_adaptativa, 'Umbralización Adaptativa')


if __name__ == "__main__":
    ruta_imagen = 'cr7.png'
    procesador = ImageProcessor(ruta_imagen)
    procesador.procesar_imagen()