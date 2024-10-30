from library import load_resources, analyze_text

def main():
    load_resources()
    text = "Estoy muy feliz. Me desperte sonriendos. No me gusta el enojo. No me gusta el miedo."
    sentiment_score, emotion_counters = analyze_text(text)
    print(f"Puntaje final de sentimiento: {sentiment_score}")
    print(f"Contadores por emoción: {emotion_counters}")

if __name__ == "__main__":
    main()