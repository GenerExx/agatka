import os
from pydub.utils import mediainfo
from webvtt import WebVTT, Caption

def get_mp3_duration(file_path):
    """Zwraca czas trwania pliku MP3 w sekundach."""
    info = mediainfo(file_path)
    return float(info['duration'])

def shift_time(time_str, shift_seconds):
    """Przesuwa czas o określoną liczbę sekund i zwraca w formacie VTT."""
    time_parts = time_str.split(':')
    hours = int(time_parts[0])
    minutes = int(time_parts[1])
    seconds = float(time_parts[2].replace(',', '.'))
    
    total_seconds = hours * 3600 + minutes * 60 + seconds + shift_seconds
    
    new_hours = int(total_seconds // 3600)
    new_minutes = int((total_seconds % 3600) // 60)
    new_seconds = total_seconds % 60
    
    return f"{new_hours:02}:{new_minutes:02}:{new_seconds:06.3f}"

def merge_vtt_files(input_folder, output_file, mp3_folder):
    """Łączy pliki VTT, uwzględniając czas trwania plików MP3 i zmienia oznaczenia mówców."""
    all_captions = []
    shift_seconds = 0
    fragment_number = 1
    
    for file_name in sorted(os.listdir(input_folder)):
        if file_name.endswith('.vtt'):
            vtt_file_path = os.path.join(input_folder, file_name)
            mp3_file_name = file_name.replace('.vtt', '.mp3')
            mp3_file_path = os.path.join(mp3_folder, mp3_file_name)
            
            if os.path.exists(mp3_file_path):
                mp3_duration = get_mp3_duration(mp3_file_path)
            else:
                mp3_duration = 0
            
            print(f"Processing {file_name}...")  # Diagnostyka
            
            for caption in WebVTT().read(vtt_file_path):
                start = shift_time(caption.start, shift_seconds)
                end = shift_time(caption.end, shift_seconds)
                
                # Process and format speaker text
                speaker_text = caption.text.strip()
                if speaker_text.startswith('[SPEAKER_'):
#                    print("Etap 1.\n")
                    # Extract the speaker prefix and add the fragment number
                    speaker_prefix = speaker_text.split(']')[0]  # Extract the [SPEAKER_## part
                    speaker_prefix += f"_{fragment_number}]"  # Add the fragment number
                    
                    # Correctly split text after speaker prefix
                    text_parts = speaker_text.split(']', 1)
                    if len(text_parts) > 1:
#                        print("Etap 2.\n")

                        text_after_prefix = text_parts[1].strip()  # Get the text after the speaker prefix
#                        print("Text_after_prefix 1 ===",text_after_prefix)
                        # Remove leading " : " if present
                        if text_after_prefix.startswith(': '):
                            text_after_prefix = text_after_prefix[2:].strip()
#                            print("Text_after_prefix 2 ===",text_after_prefix)
#                        else:
#                            print("Nie zaczyna się od : ")
                        caption_text = f"{speaker_prefix}: {text_after_prefix}"
#                        print("Caption text = ",caption_text)
                    else:
                        caption_text = speaker_prefix  # Handle cases where there is no text after the speaker prefix
                else:
                    caption_text = speaker_text
                
                # Diagnostyka
#                print(f"Raw Caption: {caption.start} --> {caption.end}")
#                print(f"Raw Text:\n{caption.text}")
#                print(f"Processed Caption: {start} --> {end}")
#                print(f"Processed Text:\n{caption_text}")
                
                if caption_text.strip():
                    all_captions.append(Caption(start, end, caption_text))
                else:
                    print(f"Warning: Empty caption text for {start} --> {end}")

            shift_seconds += mp3_duration
            fragment_number += 1
    
    print("Writing to output file...")  # Diagnostyka
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("WEBVTT\n\n")
        for caption in all_captions:
            f.write(f"{caption.start} --> {caption.end}\n")
            f.write(f"{caption.text}\n\n")

# Ścieżki do folderów i pliku wyjściowego
input_folder = './K09S06'  # Folder z plikami VTT
mp3_folder = './K09S06'    # Folder z plikami MP3
output_file = './K09S06/K09S06.vtt'  # Wyjściowy plik VTT

# Uruchomienie funkcji łączącej pliki VTT
merge_vtt_files(input_folder, output_file, mp3_folder)
