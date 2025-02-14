import cv2

#Esta es la función que ayuda a detectar los puntos mediante el uso de FAST
def video_points_detect (frame, fast_points_detector):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    keypoints = fast_points_detector.detect(gray_frame, None)
    fast_detector_video_points = cv2.drawKeypoints(frame, keypoints, None, color=(255, 0, 0))
    return fast_detector_video_points

def main():
    # Iniciar la captura de la cámara usando DirectShow para mayor compatibilidad en Windows
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    # Verificar si la cámara se abrió correctamente
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Establecer la resolución de la cámara (puedes ajustar esto según lo que soporte tu cámara)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Configuración para grabar video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Formato del codec para el video
    out = None  # Inicializar el objeto de grabación de video
    recording = False  # Estado de grabación

    fast_detector = cv2.FastFeatureDetector.create()

    print("Presiona 'c' para capturar una foto.")
    print("Presiona 'r' para empezar a grabar un video.")
    print("Presiona 's' para detener la grabación.")
    print("Presiona 'q' para salir del programa.")

    while True:
        ret, frame = cap.read()
        
        frames_with_fast_detector = video_points_detect(frame, fast_detector)
        cv2.imshow('Camera Feed', frames_with_fast_detector)

        if not ret:
            print("Error: Could not read frame.")
            break

        # Mostrar el feed de la cámara
        cv2.imshow('Camera Feed', frame)

        # Si estamos grabando, guardar los frames
        if recording:
            out.write(frame)

        # Capturar la tecla presionada
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            # Capturar una foto
            cv2.imwrite('captured_image.jpg', frame)
            print("Foto capturada y guardada como 'captured_image.jpg'")

        elif key == ord('r') and not recording:
            # Empezar a grabar video
            out = cv2.VideoWriter('output.avi', fourcc, 20.0, (1280, 720))
            recording = True
            print("Grabación iniciada...")

        elif key == ord('s') and recording:
            # Detener la grabación de video
            recording = False
            out.release()
            print("Grabación detenida y guardada como 'output.avi'")

        elif key == ord('q'):
            # Salir del programa
            if recording:
                out.release()  # Asegurarse de liberar el archivo de video si está grabando
            print("Saliendo del programa...")
            break

    # Liberar la cámara y cerrar las ventanas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
