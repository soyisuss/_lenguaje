import csv
import math
from collections import defaultdict

def read_emotions(file):
    words = {}
    with open(file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 2:  
                continue
            word, intensity = row[0].strip().lower(), row[1].strip()  
            try:
                words[word] = int(intensity) 
            except ValueError:
                pass  
    return words

def read_modifiers(file):
    modifiers = {}
    with open(file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 2:
                continue
            word, factor = row[0].strip().lower(), row[1].strip()
            try:
                modifiers[word] = float(factor)
            except ValueError:
                pass
    return modifiers

def read_negations(file):
    negations = set()
    with open(file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                negation = row[0].strip().lower()
                negations.add(negation)
    return negations

def load_resources():
    global emotions, intensifiers, negations
    emotions = {}
    emotions.update(read_emotions('enojo.csv'))
    emotions.update(read_emotions('felicidad.csv'))
    emotions.update(read_emotions('miedo.csv'))
    emotions.update(read_emotions('tristeza.csv'))

    intensifiers = read_modifiers('intensifiers.csv')
    negations = read_negations('negations.csv')

def compute_tf(text):
    """Calcular la frecuencia de término (TF) de cada palabra en el texto."""
    words = text.split()
    word_count = defaultdict(int)
    for word in words:
        word_count[word] += 1
    total_words = len(words)
    tf = {word: count / total_words for word, count in word_count.items()}
    return tf

def compute_idf(documents):
    """Calcular la frecuencia inversa de documento (IDF) para cada palabra en el conjunto de documentos."""
    doc_count = len(documents)
    word_doc_count = defaultdict(int)
    
    for doc in documents:
        words = set(doc.split())  # Tomamos palabras únicas por documento
        for word in words:
            word_doc_count[word] += 1
    
    idf = {word: math.log(doc_count / (1 + count)) for word, count in word_doc_count.items()}
    return idf

def compute_tfidf(tf, idf):
    """Calcular el TF-IDF multiplicando TF y IDF."""
    tfidf = {word: tf_value * idf.get(word, 0) for word, tf_value in tf.items()}
    return tfidf

def preprocess_text(text):
    text = text.lower()
    sentences = text.replace('!', '.').replace(';', '.').split('.')
    sentences = [s.strip() for s in sentences if s]
    return sentences

def analyze_sentence(sentence, idf):
    words = sentence.split()
    score = 0
    counters = {"enojo": 0, "felicidad": 0, "miedo": 0, "tristeza": 0}
    
    tf = compute_tf(sentence)  # Calculamos el TF para la oración
    tfidf = compute_tfidf(tf, idf)  # Calculamos el TF-IDF
    
    i = 0
    while i < len(words):
        word = words[i].strip().lower()  # Normalizamos la palabra
        if word in negations:
            # Si encontramos una negación, no agregamos ningún valor para la siguiente emoción
            i += 1  # Saltamos a la siguiente palabra
            if i < len(words):
                next_word = words[i].strip().lower()
                if next_word in emotions:
                    emotion_value = 0  # La emoción es anulada por la negación
                    score += emotion_value
                    classify_emotion(counters, next_word, emotion_value)
        elif word in intensifiers:
            i += 1
            if i < len(words):
                next_word = words[i].strip().lower()
                if next_word in emotions:
                    emotion_value = emotions[next_word] * intensifiers[word] * tfidf.get(next_word, 0)
                    score += emotion_value
                    classify_emotion(counters, next_word, emotion_value)
        elif word in emotions:
            emotion_value = emotions[word] * tfidf.get(word, 0)
            score += emotion_value
            classify_emotion(counters, word, emotion_value)
        i += 1
    return score, counters

def classify_emotion(counters, word, value):
    # Tomar el valor absoluto de la emoción para asegurar que sea positiva
    absolute_value = abs(value)
    
    if word in emotions:
        if word in read_emotions('enojo.csv'):
            counters["enojo"] += absolute_value
        elif word in read_emotions('felicidad.csv'):
            counters["felicidad"] += absolute_value
        elif word in read_emotions('miedo.csv'):
            counters["miedo"] += absolute_value
        elif word in read_emotions('tristeza.csv'):
            counters["tristeza"] += absolute_value


def analyze_text(text):
    sentences = preprocess_text(text)
    total_score = 0
    emotion_counters = {"enojo": 0, "felicidad": 0, "miedo": 0, "tristeza": 0}
    
    # Calculamos IDF para todo el conjunto de oraciones
    idf = compute_idf(sentences)
    
    for sentence in sentences:
        sentence_score, sentence_counters = analyze_sentence(sentence, idf)
        total_score += sentence_score
        for emotion, count in sentence_counters.items():
            emotion_counters[emotion] += count
    return total_score, emotion_counters

# Nueva funcionalidad: Lista de palabras por emoción
def get_words_by_emotion(text):
    words = text.split()
    emotion_words = {"enojo": [], "felicidad": [], "miedo": [], "tristeza": []}

    for word in words:
        word = word.strip().lower()
        if word in read_emotions('enojo.csv'):
            emotion_words["enojo"].append(word)
        elif word in read_emotions('felicidad.csv'):
            emotion_words["felicidad"].append(word)
        elif word in read_emotions('miedo.csv'):
            emotion_words["miedo"].append(word)
        elif word in read_emotions('tristeza.csv'):
            emotion_words["tristeza"].append(word)

    return emotion_words
# Nueva funcionalidad: Palabra más y menos predominante
def get_predominant_words(emotion_counters):
    predominant_word = max(emotion_counters, key=emotion_counters.get, default=None)
    least_predominant_word = min(emotion_counters, key=emotion_counters.get, default=None)
    return predominant_word, least_predominant_word