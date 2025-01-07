import flet as ft
from PIL import Image
from library import load_resources, analyze_text, get_words_by_emotion, get_predominant_words
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def main(page: ft.Page):
    # Configurar la página de Flet
    page.title = "Análisis de Sentimiento y Emociones"
    page.bgcolor = "#F4F4F9"  # Fondo suave
    page.horizontal_alignment = "center"  # Centrar horizontalmente todo el contenido
    page.vertical_alignment = "center"    # Centrar verticalmente todo el contenido
    page.scroll = "auto"
    
    # Cargar recursos iniciales
    load_resources()
    
    # Funciones para nuevos botones
    def show_words_by_emotion(e):
        text = text_entry.value
        words_by_emotion = get_words_by_emotion(text)
        result_text = f"Palabras por emoción: {words_by_emotion}"
        words_label.value = result_text
        words_label.update()

    def show_predominant_words(e):
        text = text_entry.value
        _, emotion_counters = analyze_text(text)
        predominant, least_predominant = get_predominant_words(emotion_counters)
        result_text = f"Más predominante: {predominant}, Menos predominante: {least_predominant}"
        predom_label.value = result_text
        predom_label.update()

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
    try:
        logo_img = Image.open("logo.png").resize((200, 200))
        buf = BytesIO()
        logo_img.save(buf, format="PNG")
        logo_img_base64 = base64.b64encode(buf.getvalue()).decode()
        buf.close()
        logo = ft.Image(src_base64=logo_img_base64, width=200, height=200)
    except Exception as e:
        print("Error al cargar el logo:", e)
        logo = ft.Text("[Logo no disponible]", size=20, color="red")
    
    title = ft.Text("Hola, bienvenido", size=40, weight="bold", color="#4B4E6D", text_align="center")
    
    # Entrada de texto
    text_entry = ft.TextField(
        label="Cuéntanos de tu día, ¿Cómo te sientes?", 
        multiline=True, 
        min_lines=10, 
        text_size=16, 
        width=800,  # Ancho total para centrar
        border_color="#4B4E6D",
        bgcolor="#a25882"
    )

    # Resultados
    words_label = ft.Text("", size=25, color="#4B4E6D", text_align="center")
    predom_label = ft.Text("", size=25, color="#4B4E6D", text_align="center")
    result_label = ft.Text("", size=25, color="#a25882", text_align="center")
    numeric_label = ft.Text("", size=25, color="#4B4E6D", text_align="center")
    graph_image = ft.Image(width=600, height=400)
    
    # Botones adicionales
    graph_button = ft.ElevatedButton(
        "Mostrar gráfico",
        on_click=analyze_text_input,
        bgcolor="#FF6F61",
        color="white"
    )
    
    words_button = ft.ElevatedButton(
        "Palabras por emoción",
        on_click=show_words_by_emotion,
        bgcolor="#6B728E",
        color="white"
    )
    
    predom_button = ft.ElevatedButton(
        "Palabra predominante",
        on_click=show_predominant_words,
        bgcolor="#4B4E6D",
        color="white"
    )

    # Contenido en una sola columna centrada
    content = ft.Column(
        [
            logo,
            title,
            text_entry,
            graph_button,
            ft.Row(
                [
                    words_button,
                    predom_button
                ],
                alignment="center",
                spacing=10
            ),
            words_label,
            predom_label,
            result_label,
            numeric_label,
            graph_image
        ],
        alignment="center",
        horizontal_alignment="center",
        spacing=20
    )

    page.add(content)

if __name__ == "__main__":
    ft.app(target=main)





