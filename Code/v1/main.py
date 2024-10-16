import csv
import string

# Paso 1: Preprocesamiento (convertir a minúsculas y eliminar puntuación)
def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# Paso 2: Eliminar palabras vacías
stop_words = ['el', 'la', 'los', 'las', 'un', 'una', 'de', 'que', 'y', 'a']

def remove_stopwords(text):
    words = text.split()
    words_filtered = [word for word in words if word not in stop_words]
    return ' '.join(words_filtered)

# Paso 3: Cargar palabras de los archivos CSV (con normalización de palabras)
def load_words_from_csv(filename):
    words = {}
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Saltar la fila de encabezado
        for row in reader:
            if len(row) < 2:  # Verificar que la fila tenga al menos dos columnas
                continue  # Ignorar filas vacías o mal formateadas
            word, intensity = row[0].strip().lower(), row[1].strip()  # Normalizar palabra
            try:
                words[word] = int(intensity)  # Asegúrate de que la intensidad sea un entero
            except ValueError:
                pass  # Ignorar filas con intensidades inválidas
    return words

# Cargar las palabras positivas y negativas desde archivos CSV
positive_words = load_words_from_csv('positivas.csv')
negative_words = load_words_from_csv('negativas.csv')

# Paso 4: Tokenización (dividir el texto en palabras)
def tokenize_text(text):
    return text.split()

# Paso 5: Asignar puntuación de sentimiento con la intensidad de las palabras
def sentiment_analysis(text, positive_words, negative_words):
    words = tokenize_text(text)
    score = 0
    for word in words:
        if word in positive_words:
            score += positive_words[word]  # Sumar la intensidad de la palabra positiva
        elif word in negative_words:
            score -= negative_words[word]  # Restar la intensidad de la palabra negativa
    return score

# Paso 6: Análisis de sentimiento
def analyze_sentiment(text):
    text = clean_text(text)  # Normaliza el texto
    text = remove_stopwords(text)  # Remueve palabras vacías
    score = sentiment_analysis(text, positive_words, negative_words)  # Calcula el puntaje
    
    if score > 0:
        return "Positivo"
    elif score < 0:
        return "Negativo"
    else:
        return "Neutral"

# Ejemplo de uso
texto = input("Introduce un texto: ")
resultado = analyze_sentiment(texto)
print(f"El sentimiento del texto es: {resultado}")
