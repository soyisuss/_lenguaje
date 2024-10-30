import csv
import string

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

def load_resources():
    global emotions, intensifiers, negations
    emotions = {}
    emotions.update(read_emotions('enojo.csv'))
    emotions.update(read_emotions('felicidad.csv'))
    emotions.update(read_emotions('miedo.csv'))
    emotions.update(read_emotions('tristeza.csv'))

    intensifiers = {"muy": 1.5, "bastante": 1.2, "poco": 0.5}
    negations = {"no", "nunca", "jamás"}

def correct_spelling(word, dictionary):
    closest_word = min(dictionary.keys(), key=lambda w: levenshtein_distance(word, w))
    return closest_word if levenshtein_distance(word, closest_word) <= 2 else word

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def preprocess_text(text):
    text = text.lower()
    sentences = text.replace('!', '.').replace(';', '.').split('.')
    sentences = [s.strip() for s in sentences if s]
    return sentences

def analyze_sentence(sentence):
    words = sentence.split()
    score = 0
    counters = {"enojo": 0, "felicidad": 0, "miedo": 0, "tristeza": 0}
    i = 0
    while i < len(words):
        word = correct_spelling(words[i], emotions) 
        if word in negations:
            i += 1
            if i < len(words):
                next_word = correct_spelling(words[i], emotions)
                if next_word in emotions:
                    emotion_value = -emotions[next_word]
                    score += emotion_value
                    classify_emotion(counters, next_word, emotion_value)
        elif word in intensifiers:
            i += 1
            if i < len(words):
                next_word = correct_spelling(words[i], emotions)
                if next_word in emotions:
                    emotion_value = emotions[next_word] * intensifiers[word]
                    score += emotion_value
                    classify_emotion(counters, next_word, emotion_value)
        elif word in emotions:
            emotion_value = emotions[word]
            score += emotion_value
            classify_emotion(counters, word, emotion_value)
        i += 1
    return score, counters

def classify_emotion(counters, word, value):
    if word in emotions:
        if word in read_emotions('enojo.csv'):
            counters["enojo"] += value
        elif word in read_emotions('felicidad.csv'):
            counters["felicidad"] += value
        elif word in read_emotions('miedo.csv'):
            counters["miedo"] += value
        elif word in read_emotions('tristeza.csv'):
            counters["tristeza"] += value

def analyze_text(text):
    sentences = preprocess_text(text)
    total_score = 0
    emotion_counters = {"enojo": 0, "felicidad": 0, "miedo": 0, "tristeza": 0}
    for sentence in sentences:
        sentence_score, sentence_counters = analyze_sentence(sentence)
        total_score += sentence_score
        for emotion, count in sentence_counters.items():
            emotion_counters[emotion] += count
    return total_score, emotion_counters