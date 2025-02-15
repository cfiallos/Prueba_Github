import cv2
#Aquí se crea la clase que va a contener todo

class VideoProcessor:
    def __init__(self):
        self.cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            raise Exception("Error: Could not open camera.")
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = None
        self.recording = False
        
        #Este va a crear el detector FAST
        self.fast_detector = cv2.FastFeatureDetector.create()
        
        #Aquí va a estar todos los filtros definidos 
        self.filtro_gaussiano_activo = False
        self.filtro_promedio_activo = False
        self.filtro_sobel_activo = False
        self.filtro_canny_activo = False
        
        #Aquí están todos los detectores utilizados 
        self.fast_detector_activo = False
        self.harris_detector_activo = False
        self.sift_detector_activo = False

        #Esta va a servir para definir una escala de grises
        self.escala_de_grises_activa = False

#Esta función va a definir la aplicación de todos los filtros
    def apply_filter(self, frame):
        if frame is None:
            print("Error: El marco está vacío o no es válido.")
            return frame
        if self.escala_de_grises_activa:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.filtro_gaussiano_activo:
            return cv2.GaussianBlur(frame, (15, 15), 0)
        elif self.filtro_promedio_activo:
            return cv2.blur(frame, (15, 15))
        elif self.filtro_sobel_activo:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            aplicacion_filtro_sobel_x = cv2.Sobel(gray_frame, cv2.CV_64F, 1, 0, (15,15))
            aplicacion_filtro_sobel_y = cv2.Sobel(gray_frame, cv2.CV_64F, 0, 1, (15,15))
            sobel_aplicado = cv2.magnitude(aplicacion_filtro_sobel_x, aplicacion_filtro_sobel_y)
            return sobel_aplicado
        elif self.filtro_canny_activo:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return cv2.Canny(gray_frame, -1, 100, 200)
        else:
            return frame  
#Esta función va a definir la aplicación de los detectores 
    def video_points_detect(self, frame):
        if self.fast_detector_activo:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            keypoints = self.fast_detector.detect(gray_frame, None)
            frame = cv2.drawKeypoints(frame, keypoints, None, color=(255, 0, 0))
        
        if self.harris_detector_activo:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            harris_corners = cv2.cornerHarris(gray_frame, 2, 3, 0.06)
            frame[harris_corners > 0.01 * harris_corners.max()] = [0, 0, 255]
        
        if self.sift_detector_activo:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            sift = cv2.SIFT_create()
            keypoints_sift, _ = sift.detectAndCompute(gray_frame, None)
            frame = cv2.drawKeypoints(frame, keypoints_sift, None, color=(0, 255, 0))

        return frame

    def start(self):
        print("Presione 'c' para capturar una foto.")
        print("Presione 'r' para empezar a grabar un video.")
        print("Presione 's' para detener la grabación.")
        print("Presione 'g' para alternar el Filtro Gaussiano.")
        print("Presione 'a' para alternar el Filtro Promedio.")
        print("Presione '3' para alternar el Filtro Sobel.")
        print("Presione '4' para alternar el Filtro Canny.")
        print("Presione 'f' para alternar el detector FAST.")
        print("Presione 'h' para alternar el detector de Harris.")
        print("Presione 's' para alternar el detector SIFT.")
        print("Presione 't' para alternar la escala de grises")
        print("Presione 'q' para salir del programa.")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            # Aplicar el filtro seleccionado
            filtered_frame = self.apply_filter(frame)
            frames_with_detectors = self.video_points_detect(filtered_frame)
            cv2.imshow('Camera Feed', frames_with_detectors)

            if self.recording:
                self.out.write(frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord('c'):
                cv2.imwrite('captured_image.jpg', frame)
                print("Foto capturada y guardada como 'captured_image.jpg'")

            elif key == ord('r') and not self.recording:
                self.out = cv2.VideoWriter('output.avi', self.fourcc, 20.0, (1280, 720))
                self.recording = True
                print("Grabación iniciada...")

            elif key == ord('s') and self.recording:
                self.recording = False
                self.out.release()
                print("Grabación detenida y guardada como 'output.avi'")

            elif key == ord('g'):
                self.filtro_gaussiano_activo = not self.filtro_gaussiano_activo
                state = "activado" if self.filtro_gaussiano_activo else "desactivado"
                print(f"Filtro Gaussiano {state}.")

            elif key == ord('a'):
                self.filtro_promedio_activo = not self.filtro_promedio_activo
                state = "activado" if self.filtro_promedio_activo else "desactivado"
                print(f"Filtro Promedio {state}.")

            elif key == ord('3'):
                self.filtro_sobel_activo = not self.filtro_sobel_activo
                state = "activado" if self.filtro_sobel_activo else "desactivado"
                print(f"Filtro Sobel {state}.")

            elif key == ord('4'):
                self.filtro_canny_activo = not self.filtro_canny_activo
                state = "activado" if self.filtro_canny_activo else "desactivado"
                print(f"Filtro Canny {state}.")

            elif key == ord('f'):
                self.fast_detector_activo = not self.fast_detector_activo
                state = "activado" if self.fast_detector_activo else "desactivado"
                print(f"Detector FAST {state}.")

            elif key == ord('h'):
                self.harris_detector_activo = not self.harris_detector_activo
                state = "activado" if self.harris_detector_activo else "desactivado"
                print(f"Detector de Harris {state}.")

            elif key == ord('s'):
                self.sift_detector_activo = not self.sift_detector_activo
                state = "activado" if self.sift_detector_activo else "desactivado"
                print(f"Detector SIFT {state}.")

            elif key == ord('q'):
                if self.recording:
                    self.out.release()
                print("Saliendo del programa...")
                break

            elif key == ord('t'):
                self.escala_de_grises_activa = not self.escala_de_grises_activa
                state = "activado" if self.escala_de_grises_activa else "desactivado"
                print(f"Escala de grises {state}.")

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    video_processor = VideoProcessor()
    video_processor.start()

# Conclusión y recomendaciones
#En conclusión cada uno de los detectores cómo Harris corner, FAST y SIFT, resultan ser herramientas fundamentales para realizar el procesamiento de video, 
#cada uno tiene sus propias ventajas y desventajas, cada uno resulta ser útil en diferentes escenarios, 
#por esta razón se recomienda utilizar cada uno en donde corresponda. Por ejemplo, el Harris Corner tiende a ser muy efectivo para detectar esquinas y se utiliza mayormente en imagenes,
#el FAST al ser rapido y eficiente resulta ser el más adecuado para las aplicaciones en tiempo real, y por último, 
# el SIFT es generalmente utilizado para situaciones en las que se necesite robustez ante los cambios de escala y rotación.