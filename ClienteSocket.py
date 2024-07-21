import socket
import tkinter as tk

def enviar_trama():
    trama = trama_var.get()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5060))

    try:
        client_socket.send(trama.encode('utf-8'))
        respuesta = client_socket.recv(1024).decode('utf-8')
        respuesta_var.set(respuesta)
    except Exception as e:
        respuesta_var.set(f"Error al enviar la trama: {str(e)}")

    client_socket.close()

# Implementación de la interfaz gráfica de tkinter
cliente_root = tk.Tk()
cliente_root.title("Cliente")

frame = tk.Frame(cliente_root, padx=20, pady=20, bg="#f0f0f0")
frame.pack(expand=True, fill="both")

trama_var = tk.StringVar()
trama_label = tk.Label(frame, text="Trama de entrada", bg="#f0f0f0", font=("Helvetica", 14))
trama_label.pack(pady=5)

# Implementación de la parte de trama
trama_entry = tk.Entry(frame, textvariable=trama_var, bd=3, font=("Helvetica", 12), justify="center")
trama_entry.pack(pady=10)

enviar_button = tk.Button(frame, text="Enviar Trama", command=enviar_trama, bd=3, font=("Helvetica", 12))
enviar_button.pack(pady=10)

# Usar LabelFrame para mostrar la respuesta con bordes
respuesta_frame = tk.LabelFrame(frame, text="Respuesta del Servidor", font=("Helvetica", 12), padx=10, pady=10)
respuesta_frame.pack(pady=10, expand=True, fill="both")

respuesta_var = tk.StringVar()
respuesta_label = tk.Label(respuesta_frame, textvariable=respuesta_var, font=("Helvetica", 12), bg="white")
respuesta_label.pack()

cliente_root.mainloop()
