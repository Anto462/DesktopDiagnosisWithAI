import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import time
from main import transcribe_audio_to_text, generate_response, speak_text, listen_for_keyword, record_audio
from PIL import Image, ImageTk  


class SistemaIA(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Diagnóstico de PC con AI")
        self.geometry("600x600")  
        self.configure(bg="lavender")

        self.diagnostico_iniciado = False
        
        self.icon_microfono = self.cargar_imagen("DiagnosticoDePcPorAI\\microfono_icono.png", (35, 35))
        self.icon_diagnostico = self.cargar_imagen("DiagnosticoDePcPorAI\\diagnostico_icono.png", (35, 35))
        self.create_widgets()


    def cargar_imagen(self, ruta, tamaño):
        """Carga imagen."""
        try:
            img = Image.open(ruta)
            img_resized = img.resize(tamaño, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img_resized)
        except Exception as e:
            print(f"Error al cargar la imagen {ruta}: {e}")
            return None
         
     
        self.create_widgets()

    def create_widgets(self):
        # título 
        titulo_label = tk.Label(self, text="Diagnóstico de PC con IA", font=("Rockwell", 20), fg="#33577a", bg="lavender")
        titulo_label.pack(pady=20)

        # agregar imagen debajo del titulo
        ruta_imagen = "DiagnosticoDePcPorAI\\ai.png"  
        try:
            img = Image.open(ruta_imagen)  # abrir la imagen
            img_resized = img.resize((100, 100), Image.Resampling.LANCZOS)  # redimensionar la imagen
            img_tk = ImageTk.PhotoImage(img_resized)  
            imagen_label = tk.Label(self, image=img_tk, bg="lavender")
            imagen_label.image = img_tk  
            imagen_label.pack(pady=10)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

        

         # boton para activar laIA
        if self.icon_microfono:  
            self.microfono_button = tk.Button(
                self,
                text=" Activar IA",
                image=self.icon_microfono,
                compound=tk.LEFT,
                command=self.activar_ia,
                bg="#36498a",
                fg="white",
                font=("Rockwell", 12),
                borderwidth = 0
                
            )
        else:  
            self.microfono_button = tk.Button(
                self,
                text="Activar IA",
                command=self.activar_ia,
                bg="#36498a",
                fg="white",
                font=("Rockwell", 12),
                borderwidth = 0
            )
        self.microfono_button.pack(pady=20)


        # botón para iniciar diagnóstico
        if self.icon_diagnostico:  
            self.diagnostico_button = tk.Button(
                self,
                text=" Iniciar Diagnóstico",
                image=self.icon_diagnostico,
                compound=tk.LEFT,
                command=self.iniciar_diagnostico,
                bg="#36498a",
                fg="white",
                font=("Rockwell", 12),
                borderwidth = 0
            )
        else:  
            self.diagnostico_button = tk.Button(
                self,
                text="Iniciar Diagnóstico",
                command=self.iniciar_diagnostico,
                bg="#36498a",
                fg="white",
                font=("Rockwell", 12),
                borderwidth = 0
            )
        self.diagnostico_button.pack(pady=20)

        # area  para mostrar resultados
        self.resultado_text = scrolledtext.ScrolledText(self, width=60, height=20, font=("Rockwell", 12), wrap=tk.WORD)
        self.resultado_text.pack(pady=20)
        self.resultado_text.config(state=tk.DISABLED)

    def activar_ia(self):
        """Activar IA y escuchar comandos de voz"""
        threading.Thread(target=self.escuchar_ia).start()

    def escuchar_ia(self):
        """Escuchar activación por palabra clave 'Sistema'"""
        while True:
            if listen_for_keyword():  # espera por palabra clave
                self.resultado_text.config(state=tk.NORMAL)
                self.resultado_text.insert(tk.END, "Esperando orden...\n")
                self.resultado_text.config(state=tk.DISABLED)
                self.update()
                filename = "input.wav"
                if record_audio(filename):  # se graba el audio cuando detecta la palabra clave
                    text = transcribe_audio_to_text(filename)
                    if text:
                        self.resultado_text.config(state=tk.NORMAL)
                        self.resultado_text.insert(tk.END, f"Orden recibida: {text}\n")
                        self.resultado_text.config(state=tk.DISABLED)
                        self.update()
                        response = generate_response(text)  # genera respuesta 
                        speak_text(response)
                        self.resultado_text.config(state=tk.NORMAL)
                        self.resultado_text.insert(tk.END, f"Respuesta IA: {response}\n\n")
                        self.resultado_text.config(state=tk.DISABLED)
                        self.update()

    def iniciar_diagnostico(self):
        """Iniciar diagnóstico del sistema"""
        if not self.diagnostico_iniciado:
            self.diagnostico_iniciado = True
            self.resultado_text.config(state=tk.NORMAL)
            self.resultado_text.delete(1.0, tk.END)
            self.resultado_text.insert(tk.END, "Iniciando diagnóstico...\n")
            self.resultado_text.config(state=tk.DISABLED)
            self.update()

            
            threading.Thread(target=self.diagnosticar_sistema).start()
        else:
            messagebox.showwarning("Diagnóstico en progreso", "Ya se está realizando un diagnóstico.")

    def diagnosticar_sistema(self):
        """Diagnóstico del sistema"""
        time.sleep(3)  
        resultado_diag = generate_response("info del sistema")  
        self.resultado_text.config(state=tk.NORMAL)
        self.resultado_text.insert(tk.END, "Diagnóstico completado:\n")
        self.resultado_text.insert(tk.END, resultado_diag + "\n")
        self.resultado_text.config(state=tk.DISABLED)
        self.update()
        self.diagnostico_iniciado = False


if __name__ == "__main__":
    app = SistemaIA()
    app.mainloop()
