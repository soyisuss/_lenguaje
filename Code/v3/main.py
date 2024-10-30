from library import load_resources, analyze_text

def main():
    load_resources()
    text = "Ultimamente he estado muy feliz, empiezo el dia sonriendo y con mucha alegría. Sin embargo, en las noches me siento un poco triste"
    sentiment_score = analyze_text(text)
    print(f"Puntaje final de sentimiento: {sentiment_score}")

if __name__ == "__main__":
    main()