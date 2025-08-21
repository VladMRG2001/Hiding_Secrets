from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
# Functie pentru a putea vizualiza matricele in notepad de exemplu
def salveaza_matrice_txt(matrice, path):
    np.savetxt(path, matrice, fmt='%3d')
    print(f"Matrice salvată în {path}")

path = Path(__file__).resolve().parent # Path-ul folderului curent

# 1. Încarcă imaginea și convertește în RGB
image_path = f"{path}/fox.jpg"  # wolf, fox, knight sau ghost
img = Image.open(image_path).convert('RGB') # Deschidere imagine
img = img.resize((64, 64)) # Ne asiguram ca are 64x64

# Afișăm imaginea reala pentru a ne asigura ca este corect citita
plt.imshow(img)
plt.title('Imagine Reala')
plt.axis('off')
plt.show()

# 2. Convertim într-un array (64, 64, 3)
rgb_array = np.array(img) # Valorile R,G,B pentru fiecare pixel
# print("Valorile RGB pentru fiecare pixel: \n")
# print(rgb_array)
# print('\n')

# 3. Calculăm grayscale folosind formula NTSC
# Y = 0.299*R + 0.587*G + 0.114*B
# Luam valoarea de pe fiecare canal, apoi convertim totul din zecimal in valori intregi (intre 0 si 255)
grayscale_array = (0.299 * rgb_array[:, :, 0] + 
                   0.587 * rgb_array[:, :, 1] + 
                   0.114 * rgb_array[:, :, 2]).astype(np.uint8)

# 4. Afișăm imaginea grayscale pentru a verifica corectitudinea
plt.imshow(grayscale_array, cmap='gray')
plt.title('Imagine Grayscale (NTSC)')
plt.axis('off')
plt.show()

# Pana aici doar am convertit imaginea originala in "alb-negru".
# Am facut acest lucru, deoarece doar asa putem sa inseram un mesaj secret in forma dorita
# Acum practic pentru fiecare pixel avem R=G=B, de aceea matricea va deveni doar 64x64, intrucat doar un canal ne intereaza

# 5. Afișăm matricea grayscale completă (doar primele 8 linii ca să nu fie prea mare)
# print("Matrice grayscale:")
# print(grayscale_array[:8])  # primele 8

# Salvam matricea grayscale
salveaza_matrice_txt(grayscale_array, f"{path}/1_imagine_grayscale.txt")

# Inițializăm imaginea comprimată
# initial o matrice de 64x64 doar cu valori de 0 peste care vom contrui imaginea comprimata
compressed_img = np.zeros_like(grayscale_array)

# Parcurgem imaginea în blocuri de 4x4
block_size = 4 # dimensiunea fiecarui bloc (M in documentatie)
# Parcurgem imaginea linie cu linie și coloană cu coloană, cu pas de 4, ca să extragem fiecare bloc 4x4.
for i in range(0, grayscale_array.shape[0], block_size):
    for j in range(0, grayscale_array.shape[1], block_size):
        # Extragem blocul
        block = grayscale_array[i:i+block_size, j:j+block_size]
        flat_block = block.flatten() # Pentru a transforma cele 4x4 valori intr-un vector de 16 elemente
        
        # 1. Media AVG
        avg = np.mean(flat_block) # Media aritmetica a celor 16 valori
        
        # 2. Calculăm deviația absolută medie (var)
        var = np.mean(np.abs(flat_block - avg)) # Media aritmetica pentru toate diferentele de (valoare pixel - medie)

        # 3. Construim bitmap: 1 dacă pixel >= avg, altfel 0
        bitmap = (flat_block >= avg).astype(int)

        # 4. Calculăm β (număr de 1 în bitmap)
        beta = np.count_nonzero(bitmap)

        # Evităm împărțirea la 0
        if beta == 0 or beta == block_size * block_size:
            # Nu putem aplica formulele, copiem blocul original
            compressed_block = np.full((block_size, block_size), avg)
        else:
            M = block_size  # pentru claritate
            total_pixels = M * M

            # 5. Calculăm Lm și Hm conform formulelor
            Lm = avg - (total_pixels * var) / (2 * (total_pixels - beta))
            Hm = avg + (total_pixels * var) / (2 * beta)

            # 6. Reconstruim blocul
            compressed_flat = np.where(bitmap == 1, Hm, Lm) # Unde avem 1 in bitmap puten Hm, altfel Lm
            compressed_block = compressed_flat.reshape((block_size, block_size)) # Transformam vectroul de 16 elem in bloc 4x4

        # Punem blocul în imaginea comprimată
        compressed_img[i:i+block_size, j:j+block_size] = compressed_block.astype(np.uint8)

# Afișează imaginea reconstruită după AMBTC (Absolute Moment Block Truncation Coding)
plt.imshow(compressed_img, cmap='gray')
plt.title('Imagine comprimată AMBTC (blocuri 4x4)')
plt.axis('off')
plt.show()

# Salvăm matricea finala dupa compresie
salveaza_matrice_txt(compressed_img, f"{path}/2_imagine_compressed.txt")

# CRIPTARE + DECRIPTARE mesaj secret în imaginea AMBTC

def embed_large_message(compressed_img, text):
    """Codifică un mesaj în blocuri 4x4 folosind metoda AMBTC + codificare în baza 3."""
    ternary_chunks = text_to_ternary_chunks_correct(text)  # Listă de liste de 14 trits
    watermarked_final = compressed_img.copy()
    block_count = 0

    for i in range(0, compressed_img.shape[0], 4):
        for j in range(0, compressed_img.shape[1], 4):
            if block_count >= len(ternary_chunks):
                break  # Am terminat de codificat mesajul

            block = compressed_img[i:i+4, j:j+4]
            flat_block = block.flatten()

            # Găsirea lui Hm și Lm + pozițiile lor
            Hm_pos = 0
            Hm_val = flat_block[Hm_pos].item()
            Lm_pos = None
            Lm_val = None

            for idx in range(1, len(flat_block)):
                current_val = flat_block[idx].item()
                if current_val != Hm_val:
                    Lm_pos = idx
                    Lm_val = current_val
                    break

            if Lm_pos is None:
                Lm_pos = Hm_pos
                Lm_val = Hm_val

            # Asigură că Hm > Lm, inclusiv pozițiile
            if Hm_val < Lm_val:
                Hm_val, Lm_val = Lm_val, Hm_val
                Hm_pos, Lm_pos = Lm_pos, Hm_pos

            # Verificăm dacă diferența Hm - Lm este suficient de mare pentru a codifica
            if abs(Hm_val - Lm_val) < 3:
                continue  # Bloc invalid pentru codare, trecem mai departe

            # Obținem chunk-ul inversat pentru LSB-first
            reversed_chunk = ternary_chunks[block_count][::-1]

            # Identificăm indici modificabili (excludem Hm și Lm)
            modifiable_indices = [idx for idx in range(len(flat_block)) if idx not in (Hm_pos, Lm_pos)]

            # Aplicăm modificările în funcție de cifra ternară
            new_flat = flat_block.copy()
            for ternary_idx, idx in zip(range(14), modifiable_indices):
                s = reversed_chunk[ternary_idx]
                if s == 0:
                    new_flat[idx] += 0
                elif s == 1:
                    new_flat[idx] += 1
                elif s == 2:
                    new_flat[idx] -= 1

            # Rescriem blocul codificat în imagine
            watermarked_final[i:i+4, j:j+4] = np.array(new_flat).reshape(4, 4)
            block_count += 1

    return watermarked_final

def text_to_ternary_chunks_correct(text):
    """Converteste textul în chunk-uri ternare de 14 cifre (2 caractere per bloc)."""
    ternary_chunks = []
    
    # Completează cu spațiu dacă lungimea e impară
    if len(text) % 2 != 0:
        text += " "
    
    for i in range(0, len(text), 2):
        # 1. Extrage perechea de caractere
        char1, char2 = text[i], text[i+1]
        
        # 2. Converteste fiecare caracter în binar pe 8 biți
        bin_str = format(ord(char1), '08b') + format(ord(char2), '08b')  # Ex: "EA" → "0100010101000001"
        
        # 3. Combină binarul într-un număr zecimal
        decimal_val = int(bin_str, 2)  # "0100010101000001" → 17729
        
        # 4. Converteste zecimal în baza 3 (ca șir de cifre)
        ternary_str = ""
        num = decimal_val
        while num > 0:
            num, remainder = divmod(num, 3)
            ternary_str += str(remainder)
        ternary_str = ternary_str[::-1]  # Inversează ordinea cifrelor
        
        # 5. Adaugă padding de 0 în față până la 14 cifre
        ternary_str = ternary_str.zfill(14)
        ternary_chunks.append([int(c) for c in ternary_str])
    
    return ternary_chunks

def ternary_chunks_to_text_correct(ternary_chunks):
    """Converteste chunk-uri ternare înapoi în text."""
    text = ""
    
    for chunk in ternary_chunks:
        # Inversează înapoi la MSB-first pentru conversie
        #reversed_chunk = chunk[::-1]
        # 1. Elimină padding-ul (păstrează doar cifrele semnificative)
        ternary_str = ''.join(map(str, chunk)).lstrip('0') or '0'
        
        # 2. Converteste baza 3 în zecimal
        decimal_val = int(ternary_str, 3)
        
        # 3. Converteste zecimal în 2 caractere ASCII
        bin_str = format(decimal_val, '016b')  # 16 biți pentru 2 caractere
        char1 = chr(int(bin_str[:8], 2))
        char2 = chr(int(bin_str[8:], 2))
        text += char1 + char2
    
    return text.strip()

# Codificare mesaj 
message_final = "Mesaj Secret"
print("Mesaj original:", message_final)
ternary_chunks = text_to_ternary_chunks_correct(message_final)
print("Ternar cu padding:", ternary_chunks)

watermarked_final = embed_large_message(compressed_img, message_final)  # Apelează funcția de test
salveaza_matrice_txt(watermarked_final, f"{path}/3_imagine_watermarked.txt")

def decode_large_message(watermarked_img):
    block_size = 4
    height, width = watermarked_img.shape
    extracted_chunks = []

    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            block = watermarked_img[i:i+block_size, j:j+block_size]
            flat = block.flatten().tolist()

            # 1. Identifică Hm și Lm
            first_val = flat[0]
            second_val = None
            Hm_pos = 0
            Lm_pos = None

            # Găsește poziția celeilalte valori nemodificabile
            for idx, val in enumerate(flat[1:], start=1):
                if val not in {first_val - 1, first_val, first_val + 1}:
                    second_val = val
                    if first_val > second_val:
                        Hm_val, Lm_val = first_val, second_val
                        Hm_pos, Lm_pos = 0, idx
                    else:
                        Hm_val, Lm_val = second_val, first_val
                        Hm_pos, Lm_pos = idx, 0
                    break

            if second_val is None or abs(Hm_val - Lm_val) < 3:
                continue  # bloc invalid sau necodificat

            # 2. Extrage valorile codificate de la TOATE pozițiile, în afară de Hm și Lm
            chunk = []
            for idx, val in enumerate(flat):
                if idx in {Hm_pos, Lm_pos}:
                    continue
                if val == Hm_val + 1 or val == Lm_val + 1:
                    chunk.append(1)
                elif val == Hm_val - 1 or val == Lm_val - 1:
                    chunk.append(2)
                else:
                    chunk.append(0)

            if len(chunk) >= 14:
                # Inversează ordinea elementelor în chunk înainte de a le adăuga
                reversed_chunk = chunk[:14][::-1]
                extracted_chunks.append(reversed_chunk)

    return extracted_chunks

chunks = decode_large_message(watermarked_final)
# print(f"Am extras {len(chunks)} chunk-uri.\n")

# for idx, ch in enumerate(chunks):
#     print(f"Chunk #{idx+1}: {ch}")

# print(chunks)
# print(ternary_chunks)
# Decodare
decoded_message = ternary_chunks_to_text_correct(chunks)
print("Mesaj reconstruit din imagine direct:", decoded_message)

# Afișează imaginea dupa codificarea mesajului secret
plt.imshow(watermarked_final, cmap='gray')
plt.title('Imagine cu mesajul criptat')
plt.axis('off')
plt.show()
# 300 LINES #
