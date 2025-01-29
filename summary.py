from transformers import pipeline

# Funkcja do ekstrakcji tekstu z pliku VTT
def extract_text_from_vtt(vtt_file):
    with open(vtt_file, 'r') as file:
        lines = file.readlines()
    
    text_lines = []
    for line in lines:
        # Filtrujemy linie, które nie zawierają czasu ani są pustymi liniami
        if '-->' not in line and line.strip() and not line.startswith('WEBVTT'):
            text_lines.append(line.strip())
    
    return ' '.join(text_lines)

# Funkcja do tworzenia streszczenia
def summarize_text(text):
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# Ścieżka do pliku VTT
vtt_file = './K09S04/k09s04.vtt'

# Ekstrakcja tekstu z pliku VTT
text = extract_text_from_vtt(vtt_file)

# Generowanie streszczenia
summary = summarize_text(text)

# Wyświetlenie streszczenia
print("Streszczenie:")
print(summary)
