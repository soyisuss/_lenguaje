import csv

# Función para normalizar palabras (convertir a minúsculas)
def normalize_csv(filename):
    normalized_data = []

    # Leer el archivo CSV
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        # Procesar cada fila
        for row in reader:
            word = row[0].strip().lower()  # Normalizar la palabra
            intensity = row[1].strip()  # Mantener la intensidad como está
            normalized_data.append([word, intensity])  # Guardar palabra e intensidad normalizadas

    # Sobrescribir el archivo con las palabras normalizadas
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(normalized_data)  # Escribir los datos normalizados

# Normalizar los archivos positivas.csv y negativas.csv
normalize_csv('enojo.csv')
normalize_csv('felicidad.csv')
normalize_csv('miedo.csv')
normalize_csv('tristeza.csv')

print("Archivos normalizados exitosamente.")
