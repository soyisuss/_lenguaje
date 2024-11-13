import flet as ft
from PIL import Image
from library import load_resources, analyze_text
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def main(page: ft.Page):
    # Configurar la página de Flet
    page.title = "Análisis de Sentimiento y Emociones"
    page.bgcolor = "#F4F4F9"  # Fondo suave
    page.scroll = "auto"
    
    # Cargar recursos iniciales
    load_resources()
    
    # Función para actualizar el análisis de texto
    def analyze_text_input(e):
        # Realizar análisis de texto
        text = text_entry.value
        sentiment_score, emotion_counters = analyze_text(text)

        # Mostrar resultados
        result_text = f"Contadores por emoción: {emotion_counters}"
        result_label.value = result_text
        result_label.update()

        # Mostrar gráfico
        update_graph(emotion_counters)
    
    # Función para actualizar el gráfico
    def update_graph(emotion_counters):
        emotions = list(emotion_counters.keys())
        counts = list(emotion_counters.values())
        
        # Crear gráfico de barras con Matplotlib
        pastel_colors = ["#FFADAD", "#FFD6A5", "#FDFFB6", "#CAFFBF", "#9BF6FF", "#A0C4FF", "#BDB2FF", "#FFC6FF"]
        colors = pastel_colors[:len(emotions)]
        fig, ax = plt.subplots(figsize=(10, 7))
        ax.bar(emotions, counts, color=colors)
        ax.set_xlabel("Emociones", fontsize=16)
        ax.set_ylabel("Conteo", fontsize=16)
        ax.set_title("Conteo de Emociones en el Texto", fontsize=20)

        # Guardar gráfico como imagen en base64
        buf = BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        img_str = base64.b64encode(buf.getvalue()).decode()
        buf.close()
        
        # Mostrar imagen en Flet
        graph_image.src_base64 = img_str
        graph_image.update()
    
    # Encabezado con título y logo
    title = ft.Text("Hola, bienvenido", size=40, weight="bold", color="#4B4E6D")
    
    # Cargar logo
    try:
        logo_img = Image.open("logo.png").resize((200, 200))
        buf = BytesIO()
        logo_img.save(buf, format="PNG")
        logo_img_base64 = base64.b64encode(buf.getvalue()).decode()
        buf.close()
        logo = ft.Image(src_base64=logo_img_base64, width=200, height=200)
    except Exception as e:
        print("Error al cargar el logo:", e)
        logo = None
    
    # Entrada de texto
    text_entry = ft.TextField(
        label="Cuéntanos de tu día, ¿Cómo te sientes?", 
        multiline=True, 
        min_lines=5, 
        text_size=16, 
        width=1300,
        border_color="#4B4E6D",
        bgcolor="#a25882"
    )

    # Resultado de análisis
    result_label = ft.Text("", size=25, color="#a25882")
    
    # Gráfico de emociones
    graph_image = ft.Image(width=600, height=400)
    
    # Botón para analizar el texto
    analyze_button = ft.ElevatedButton(
        "Analizar",
        on_click=analyze_text_input,
        bgcolor="#4B4E6D",
        color="white",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.Padding(top=12, right=24, bottom=12, left=24),  # Especificar padding
        )
    )
    
    # Agregar componentes en un contenedor centrado
    content = ft.Column(
        [
            ft.Row([logo], alignment="center") if logo else None,
            title,
            text_entry,
            analyze_button,
            result_label,
            graph_image
        ],
        alignment="center",
        horizontal_alignment="center",
        spacing=20
    )

    page.add(content)

# Ejecutar la aplicación de Flet
if __name__ == "__main__":
    ft.app(target=main)
