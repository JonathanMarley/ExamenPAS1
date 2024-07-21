import socket
import tkinter as tk
from datetime import datetime


def procesar_trama(trama):
    try:
        codigo_pais = trama[0:2]
        categoria_edad = trama[2:4]
        genero = trama[4]
        fecha_nacimiento_str = trama[5:13]
        nombre_completo = trama[13:]

        # Validaciones
        if codigo_pais not in ["01", "02", "03", "00"]:
            raise ValueError("Código de país no válido.")
        if not (categoria_edad == "01" or (categoria_edad.isdigit() and 20 <= int(categoria_edad) <= 50) or (categoria_edad.isdigit() and int(categoria_edad) >= 51)):
            raise ValueError("Categoría de edad no válida.")
        if genero not in ["M", "F"]:
            raise ValueError("Género no válido (debe ser M o F).")

        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y%m%d")

        # Lógica de la respuesta
        edad = (datetime.now() - fecha_nacimiento).days // 365
        respuesta = f"Hola {nombre_completo}, "
        if codigo_pais == "01":
            respuesta += "veo que eres de Honduras"
        elif codigo_pais == "02":
            respuesta += "veo que eres de Costa Rica"
        elif codigo_pais == "03":
            respuesta += "veo que eres de México"
        elif codigo_pais == "00":
            respuesta += "País Desconocido"
        else:
            respuesta += "no puedo determinar de qué país eres"

        respuesta += f" y tienes {edad} años, lo que indica que eres "

        # Verificación de género y categoría de edad
        if genero == "M":
            if categoria_edad == "01":
                respuesta += "un niño."
            elif int(categoria_edad) == 19:
                respuesta += "un adulto joven."
            elif 20 <= int(categoria_edad) <= 50:
                respuesta += "un adulto."
            elif int(categoria_edad) >= 51:
                respuesta += "una persona de la tercera edad."
        elif genero == "F":
            if categoria_edad == "01":
                respuesta += "una niña."
            elif int(categoria_edad) == 19:
                respuesta += "una adulta joven."
            elif 20 <= int(categoria_edad) <= 50:
                respuesta += "una adulta."
            elif int(categoria_edad) >= 51:
                respuesta += "una persona de la tercera edad."

        # Verificación de coherencia entre la edad y la fecha de nacimiento
        if int(categoria_edad) == edad:
            respuesta += f"\nAl observar tu fecha de nacimiento, noto que está correcta ({fecha_nacimiento_str})."
        else:
            respuesta += f"\nSin embargo, al observar tu fecha de nacimiento, noto que está incorrecta ({fecha_nacimiento_str})."

        return respuesta

    except ValueError as e:
        return f"Error en la trama: {str(e)}"


def manejar_conexion(client_socket):
    trama = client_socket.recv(1024).decode("utf-8")
    respuesta = procesar_trama(trama)
    client_socket.send(respuesta.encode("utf-8"))
    client_socket.close()


def iniciar_servidor():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5060))
    server_socket.listen(1)

    while True:
        print("Esperando conexiones...")
        client_socket, addr = server_socket.accept()
        print("Conexión establecida desde:", addr)
        manejar_conexion(client_socket)


if __name__ == "__main__":
    # Inicia el servidor en un hilo separado
    import threading

    server_thread = threading.Thread(target=iniciar_servidor)
    server_thread.start()

    # Interfaz gráfica mejorada para mostrar la respuesta
    root = tk.Tk()
    root.title("Respuesta del Servidor")

    frame = tk.Frame(root, padx=20, pady=20, bg="#3498db")  # Color de fondo azul
    frame.pack(expand=True, fill="both")

    respuesta_var = tk.StringVar()
    respuesta_label = tk.Label(frame, textvariable=respuesta_var, font=("Arial", 12), bg="#3498db")
    respuesta_label.pack(padx=10, pady=10)

    # Actualiza la respuesta
    def actualizar_respuesta():
        respuesta_var.set("Respuesta del servidor aparecerá aquí.")

    actualizar_respuesta()

    root.mainloop()
