import string

# Paso 1: Preprocesamiento
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

# Paso 3: Crear diccionario de sentimientos
sentiment_words = {
    'feliz': 1, 'alegría': 1, 'contento': 1, 'amor': 1,
    'triste': -1, 'miedo': -1, 'enojado': -1, 'odio': -1,
    'neutral': 0
}

# Paso 4: Tokenización
def tokenize_text(text):
    return text.split()

# Paso 5: Asignar puntuación de sentimiento
def sentiment_analysis(text, sentiment_words):
    words = tokenize_text(text)
    score = 0
    for word in words:
        if word in sentiment_words:
            score += sentiment_words[word]
    return score

# Paso 6: Análisis de sentimiento
def analyze_sentiment(text):
    text = clean_text(text)
    text = remove_stopwords(text)
    score = sentiment_analysis(text, sentiment_words)
    
    if score > 0:
        return "Positivo"
    elif score < 0:
        return "Negativo"
    else:
        return "Neutral"

# Ejemplo de uso
texto = "Me siento muy feliz y contento hoy, pero ayer estaba triste"
resultado = analyze_sentiment(texto)
print(f"El sentimiento del texto es: {resultado}")
