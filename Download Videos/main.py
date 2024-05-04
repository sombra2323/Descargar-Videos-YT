from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Progressbar
from threading import Thread
from pytube import YouTube

directorio_destino = ""  # Variable global para almacenar el directorio seleccionado
progress_bar = None  # Variable global para la barra de progreso

def seleccionar_directorio():
    global directorio_destino
    directorio_destino = filedialog.askdirectory()
    if directorio_destino:
        mensaje_label.config(text="Directorio seleccionado: " + directorio_destino)
    else:
        mensaje_label.config(text="")

def descargar_video():
    global directorio_destino, progress_bar
    try:
        yt_link = link_entry.get()
        if not yt_link.startswith('https://www.youtube.com/'):
            raise ValueError('El enlace debe ser de YouTube')

        yt = YouTube(yt_link)
        titulo_label.config(text="Título: " + yt.title)
        autor_label.config(text="Autor: " + yt.author)

        length_video = int(yt.length)
        min, sec = divmod(length_video, 60)
        duracion_label.config(text="Duración: {}:{} min".format(min, sec))

        if not directorio_destino:
            raise ValueError('Seleccione un directorio de destino para la descarga')

        mensaje_label.config(text="Descargando video...")
        progress_bar = Progressbar(ventana, orient="horizontal", length=200, mode='indeterminate')
        progress_bar.pack()

        Thread(target=descargar_video_thread, args=(yt,)).start()
    except ValueError as e:
        mensaje_label.config(text=str(e))
    except Exception as e:
        mensaje_label.config(text="Se ha producido un error inesperado.")

def descargar_video_thread(yt):
    global directorio_destino, progress_bar
    progress_bar.start()
    try:
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(directorio_destino)
        mensaje_label.config(text="Descarga finalizada: El video se ha descargado correctamente.")
    except Exception as e:
        mensaje_label.config(text="Se ha producido un error durante la descarga.")
    finally:
        progress_bar.stop()
        progress_bar.destroy()

# Crear ventana principal
ventana = Tk()
ventana.title("Descargar Video de YouTube")
ventana.geometry("400x400")

# Etiquetas y entrada
link_label = Label(ventana, text="Ingrese el enlace del video:")
link_label.pack()

link_entry = Entry(ventana, width=50)
link_entry.pack()

seleccionar_button = Button(ventana, text="Seleccionar directorio", command=seleccionar_directorio)
seleccionar_button.pack()

descargar_button = Button(ventana, text="Descargar", command=descargar_video)
descargar_button.pack()

titulo_label = Label(ventana, text="")
titulo_label.pack()

autor_label = Label(ventana, text="")
autor_label.pack()

duracion_label = Label(ventana, text="")
duracion_label.pack()

mensaje_label = Label(ventana, text="", fg="green")
mensaje_label.pack()

ventana.resizable(False, False)

ventana.mainloop()
