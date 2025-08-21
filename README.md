# Hiding Secrets

Acest proiect în Python implementează o metodă de steganografie și compresie de imagine, folosind algoritmul AMBTC (Absolute Moment Block Truncation Coding) pentru comprimarea unei imagini grayscale și ulterior incapsularea unui mesaj secret direct în blocurile imaginii.

## Etapele procesului

Proiectul urmează trei etape principale: 
- conversia în grayscale
- compresia prin AMBTC
- ascunderea mesajului. <br>
### 1️⃣ Conversia imaginii RGB în grayscale

Imaginea inițială este în format RGB, fiecare pixel având 24 de biți (8 pentru roșu, 8 pentru verde, 8 pentru albastru). <br>
Noi o sa pornim de la aceasta poza, numita "wolf.jpg". <br><br>
<img width="600" height="448" alt="Fig 1" src="https://github.com/user-attachments/assets/9cfe6d79-4435-4a61-be17-c552c9da2183" /> <br>
Fig 1. Imaginea originala RGB<br><br>

Dupa cum se poate observa are o dimensiune de 64x64. <br>
Putem sa extragem valorile R,G si B din fiecare pixel intr-un tabel sau fisier txt. <br>
Acest tabel ar avea o forma de 64 linii si 64x3 coloane, asadar nu este un format ideal pentru problema noastra. <br><br>
Pentru simplificarea procesului de compresie și ascundere a informației, imaginea este convertită în grayscale, folosind formula NTSC:

𝑌 = 0.299 𝑅 + 0.587 𝐺 + 0.114 𝐵

Astfel, fiecare pixel este reprezentat pe un singur canal (valoare între 0 și 255) conform formulei de calcul. <br>
Rezultatul este o imagine de 64×64 pixeli în tonuri de gri. <br>
Acum putem sa extragem o singura valoare pentru fiecare pixel, adica putem sa afisam valorile sub forma unei matrice de 64x64. <br>

Dupa aplicarea algoritmului de Grayscale obtinem imaginea: <br><br>
<img width="600" height="448" alt="Fig 2" src="https://github.com/user-attachments/assets/ebda3b9e-b536-439a-9abb-fc4e5d45d889" /> <br>
Fig 2. Imaginea transformata in Grayscale<br><br>

Hai sa vedem si valorile efective pentru fiecare pixel. <br>
Mai jos am extras matricea de 16x16 din coltul stanga sus pentru a face o comparatie intre varianta vizuala si cea numerica pentru verificare. <br>
Valorile mari tind spre alb, in timp ce cele mici tind spre negru. <br><br>
<img width="600" height="400" alt="Fig 3" src="https://github.com/user-attachments/assets/b95f737c-9f5f-45db-a59b-aab56035dbe5" /> <br>
Fig 3. Valoarea pixelilor imaginii Grayscale<br><br>

### 2️⃣ Compresia imaginii cu metoda AMBTC

Pana acum doar am transformat imaginea originala in grayscale si am extras valoarea tonului de gri pentru fiecare pixel. <br>
Dar avem un mic incoveniement si anume faptul ca valorile sunt foarte diferite si fiecare pixel aproape ca are alta valoare. <br>
Nu putem sa codam niciun mesaj secret in acest "haos" de valori, deoarece nu am stii apoi cum sa descifram ceea ce se afla acolo fara o regula clara. <br>
Aici intervine etapa a 2 a a proiectului. <br><br>
Algoritmul AMBTC (Absolute Moment Block Truncation Coding) împarte imaginea grayscale în blocuri de 4×4 pixeli. <br> 
Pentru fiecare astfel de bloc se gasesc două niveluri de intensitate: Lm și Hm, adica low mean values si high mean values. <br>

Pentru inceput sa vedem cum ar atata blocurile 4x4 si ce valori au pixelii. <br>
<img width="600" height="448" alt="Fig 4" src="https://github.com/user-attachments/assets/b8667966-a7e2-4491-a35d-7671a8ed6907" /> <br>
Fig 4. Sectionarea imaginii Grayscale in blocuri 4x4<br><br>

Acum hai sa analizam si valorile numerice ale pixelilor. <br>
Se poate observa cum tonurile de gri confirma valoarea numerica a pixelilor. <br>
<img width="600" height="400" alt="Fig 5" src="https://github.com/user-attachments/assets/10c3771a-d889-4b4b-9c4b-804e97886add" /> <br>
Fig 5. Sectionarea matricei de pixeli in blocuri 4x4<br><br>

Acum hai sa aplicam comprimarea pentru primul bloc 4x4. <br>

Pașii principali sunt:

1. Se calculează media blocului (AVG):

     AVG = $\frac{\sum_{i=1}^{M \cdot M} \mu_i}{M \cdot M}$

In cazul nostru am ajunge la valoarea 178.1875.

2. Se calculează deviația medie absolută (var):

     var = $\frac{\sum_{i=1}^{M \cdot M} \left| \mu_i - AVG \right|}{M \cdot M}$

La acest pas calculam practic media aritmetica a diferentelor dintre fiecare pixel si media aritmetica a blocului. <br>
Aceasta valoare este egala cu: <br>
17.8125 + 18.8125 + 11.8125 + 25.1875 +       <br>
11.8125 + 12.8125 + 15.8125 + 12.8125 +       <br>
35.1875 + 29.1875 + 12.8125 + 17.8125 +       <br>
39.1875 + 34.1875 + 11.8125 + 17.8125 ) / 16  <br>

Deviatia medie este: 20.3046875

3. Se construiește o hartă binară (bitmap 4×4) pe baza pragului AVG:

     pixel < AVG → 0

     pixel ≥ AVG → 1

4. Se determină valorile Lm și Hm:

     L_m = $AVG - \frac{M \cdot M \cdot var}{2 \cdot (M \cdot M - \beta)}$

     H_m = $AVG + \frac{M \cdot M \cdot var}{2 \cdot \beta}$

unde β reprezintă numărul de „1” din bitmap.

Hai sa vedem in cazul nostru ce am obtine. <br>
M reprezinta marimea blocului, deci putem inlocui M * M direct cu 16. <br>
β reprezinta numarul de blocuri de 1, adica nr de blocuri cu o valoare peste 178.1875, deci de la 179 in sus. <br>
In cazul nostru beta este 11. <br>

Deci Lm = 178.1875 - (16 * 20.3046875) / (2 * 5) = 145.7. Adica putem considera Lm = 145. <br>
Acum Hm = 178.1875 + 16 * 20.3046875 / 22 = 192.954545455. Eu am ales sa tai partea zecimala si avem Hm = 192. <br>
Diferenta vizuala intre 145 si 146 sau 192 si 193 este infima si nu reprezinta scopul proiectului. 

5. Blocul este reconstruit:

     pe pozițiile cu 0 → valoarea Lm

     pe pozițiile cu 1 → valoarea Hm

Aplicam pentru fiecare bloc 4x4 ceea ce am explicat mai sus. <br>
Astfel ajungem la imaginea comprimata finala. <br>
<img width="600" height="448" alt="Fig 6" src="https://github.com/user-attachments/assets/3f3d3f0f-6915-40a2-af5a-91884d81ad18" /> <br>
Fig 6. Imaginea comprimata prin tehnica AMBTC<br><br>

Acum hai sa vedem si valorile numerice pentru aceasta imagine. <br>
<img width="600" height="400" alt="Fig 7" src="https://github.com/user-attachments/assets/a3f2802b-a3a0-4e4f-9b6d-e90238979faa" /> <br>
Fig 7. Matricea de pixeli a imaginii comprimate<br><br>

Sa tragem si limitele blocurilor pentru o imagine mai clara. <br>
<img width="600" height="448" alt="Fig 8" src="https://github.com/user-attachments/assets/6239e997-8e38-4c5d-9aa6-2c920c6149d0" /> <br>
Fig 8. Imaginea comprimata impartita in blocuri<br><br>

Iar in varianta numerica avem: <br>
<img width="600" height="400" alt="Fig 9" src="https://github.com/user-attachments/assets/bb6ecaa1-5a82-49b9-be2a-018f18651b17" /> <br>
Fig 9. Matricea de pixeli impartita in blocuri<br><br>

Observam cum fiecare bloc 4x4 are doar 2 valori. Acest lucru se oserva si cu ochiul liber. <br>
Evident, imaginea a fost alterata, dar foarte putin, astfel inca poate fi recunoscuta. <br>
Aceasta strategie este foarte eficienta. <br>
In urma acestei compresii am ajuns la etapa in care vom incapsula un mesaj secret in imagine. <br>
Prezenta a doar 2 valori pentru fiecare bloc o sa faca lucrurile mult mai usoare. <br><br>

### 3️⃣ Încapsularea mesajului în imagine

Aceasta etapa este cea mai complicata, dar si cea mai interesanta parte a proiectului. <br>
Scopul este sa incapsulam un mesaj secret, care poate fi apoi recuperat din pixelii imaginii. <br>
Acest mesaj este format dintr-un șir de caractere ASCII (8 biți per caracter). <br>
Fiecare bloc de 4x4 are 16 pixeli, deci putem stoca o informatie echivalenta cu 16 biti. <br>
Totusi, pentru a putea decripta apoi mesajul trebuie neaparat sa rezervam 2 pixeli pentru valorile Hm si Lm, deci doar 14 sunt cu adevarat disponibili. <br><br>

Acum criptarea poate fi gandita in doua moduri: <br>
- Prima varianta este sa codificam 2 caractere de 7 biti fiecare in format binar pe spatiul liber de 14 pixeli din fiecare bloc. Dar asta ar insemna sa putem folosi doar caracterele ASCII de baza (pana la 127 = 2^7 - 1). Mai mult, pentru fiecare pixel am putea avea doar 2 optiuni: ramane la fel sau este modificat cu +1, deci o codificare mult prea slaba. <br>
- A doua varianta este folosirea codificarii in baza 3. Astfel sirul de 16 cifre binare (2 caractere ASCII) va fi transformat in 14 triti (denumirea pentru baza 3) cu paddingul necesar. Astfel, putem folosi toate caractere ASCII. Mai mult, fiecare pixel are 3 stari posibile: ramane la fel, este incrementat cu 1 sau este decrementat cu 1. <br>
Logic, o sa folosim a doua varianta. Astfel, mesajul este împărțit în perechi de caractere și convertit din baza 2 în baza 3 (ternar). <br>
Asa cum am zis, fiecare bloc 4×4 va stoca 2 caractere din mesaj. <br><br>

Procesul de inserare: <br>

Se identifica prima pozitie a valorilor Lm si Hm. Acestea 2 vor ramane neschimbate si vor fi folosite apoi la decriptare, deci e important sa le pastram. <br>
Ceilalti 14 pixeli sunt folositi pentru criptare. <br>
Se converteste codul ASCII al perechii de caractere in binar, iar apoi in ternar (sir cu valori de 0,1 si 2).
Se selectează pixelii din bloc (exceptând pozițiile corespunzătoare lui Lm și Hm). <br><br>

Pentru fiecare cifră ternară din sir se aplică regula:

     0 → pixel nemodificat

     1 → pixel = pixel + 1

     2 → pixel = pixel - 1

Astfel, mesajul este distribuit în toată imaginea, păstrând structura blocurilor AMBTC. <br><br>

Bun, inca o restrictie pe care trebuie neaparat sa o punem este faptul ca Hm - Lm >= 3. <br>
De ce? Pentru ca daca am avea Hm = 72 si Lm = 70, ne-am putea intalni cu urmatoarele situatii: <br>
Pixel = 69, evident Lm - 1. Pixel = 73, evident Hm + 1. Pixel = 71... nu stim daca e Hm - 1 sau Lm + 1. <br>
Acest lucru ar compromite decriptarea mesajului. <br>
Asadar, vom ignora blocurile care nu respecta aceasta cerinta si nu vom codifica nimic in ele. <br><br>
Dar cum o sa stim ca am sarit acel bloc si nu are nimic in el? <br>
Pai usor, toate valorile sunt Hm sau Lm, deci e clar ca acolo nu a avut loc nimic. <br><br>
Ok, dar atunci de unde stim ca un bloc gol nu reprezinta de fapt sfarsitul mesajului? <br>
Usor, daca un bloc e gol, dar are Hm - Lm >= 3, este evident ca acel bloc trebuia sa fie folosit pentru codificare. In cazul in care nu este, se intampla deoarece mesajul deja s-a terminat. <br<br>

Pentru a intelege mai usor hai sa codificam mesajul "SALUT". <br>

Pentru asta trebuie neaparat sa avem tabelul ASCII: <br>
<img width="700" height=" 500" alt="Fig 10" src="https://github.com/user-attachments/assets/907119be-9d46-450a-95c6-4f5345b7d61e" /> <br>
Fig 10. Tabelul ASCII<br><br>

Bun, hai sa o luam pas cu pas: <br>
Primul pas este sectionarea mesajului in portiuni de 2 caractere (perechi). <br>
Oridnea de parcurgere este de la stanga la dreapta. <br>
Astfel obtinem: SA + LU + T. <br>
Daca numarul de caractere este impar se va codifica doar ultimul caracter iar pentru al doilea se va folosi "space". <br>
Deci informatia va fi codificata in doar 3 blocuri. <br><br>

Trebuie sa transformam fiecare pereche in binar, iar apoi in ternar. <br>
SA = 83_65 = 01010011_01000001 = 1002020101 (baza 3), cu padding avem 00001002020101 <br>
LU = 76_85 = 01001100_01010101 = 222210202 (baza 3), cu padding avem 00000222210202 <br>
T  = 84_32 = 01010100_00100000 = 1002112122 (baza 3), cu padding avem 00001002112122 <br><br>

Sa incepem cu "SA" in primul bloc. <br>
Acum aceasta secventa va fi codificata LSB -> MSB, deci ordinea de aparitie in primul bloc este 10102020010000. (14 triti). <br>
Primul bloc este: <br>
192 192 192 145 <br> 
192 192 192 192 <br>
145 145 192 192 <br>
145 145 192 192 <br><br>

Inainte de toate trebuie sa identificam Hm si Lm, adica prima pozitie in care aceste valori apar. <br>
Pentru noi Hm = poz(1,1), Lm = (1,4). Toti ceilalti pixeli vor fi schimbati. <br><br>

Primul bloc codificat este: <br>
**192Hm** 192+1 192+0 **145Lm** <br> 
192+1 192+0 192-1 192+0 <br>
145-1 145+0 192+0 192+1 <br>
145+0 145+0 192+0 192+0 <br><br>

Asadar obtinem: <br>
192 193 192 145 <br>
193 192 191 192 <br>
144 145 192 193 <br>
145 145 192 192 <br>
<br>

Daca ne uitam in figura urmatoare la primul bloc observam ca este corect. <br>

Urmatoarea pereche este "LU". <br>
LU = 00000222210202, deci ordinea de codificare este: 20201222200000. <br>
Acest mesaj o sa fie codificat in al doilea bloc. <br>
Dar mai intai sa verificam daca este un bloc valid, adica daca Hm - Lm >= 3, asa cum amintisem. <br><br>

Al doilea bloc este: <br>
189 189 107 107 <br>
189 189 189 107 <br>
189 189 189 107 <br> 
189 189 107 107 <br><br>

Cele 2 valori prezente in bloc sunt 189 si 107, deci diferenta este >=3, adica un bloc valid in care vom codifica. <br>
Hai sa identificam Hm si Lm. Hm = poz(1,1), Lm = poz(1,3). <br><br>
Asadar, blocul codificat este: <br>
**189Hm** 189-1 **107Lm** 107+0 <br>
189-1 189+0 189+1 107-1 <br>
189-1 189-1 189-1 107+0 <br> 
189+0 189+0 107+0 107+0 <br><br>

Al doilea bloc codificat este: <br>
189 188 107 107 <br>
188 189 190 106 <br>
188 188 188 107 <br> 
189 189 107 107 <br><br>

Putem verifica si in matrice si observam ca este corect. <br>

Acum trebuie sa codificam si ultima pereche, adica "T ". <br>
Secventa corespunzatoare este: 00001002112122, deci 22121120010000. <br><br>
Hai sa verificam daca al treilea bloc este valid. <br>
82  80  82  82 <br>
80  82  82  82 <br>
80  82  82  80 <br>
82  82  82  80 <br><br>

Cele 2 valori existente sunt 82 si 80, deci Hm = 82 si Lm = 80. <br>
Dar acest lucru incalca regula noastra de validitate, deci acest bloc o sa ramana la fel. <br><br>
Trecem la al 4-lea bloc. <br>
86  86  86  86 <br>
86  86  86  86 <br>
86 206 206 206 <br>
86  86  86  86 <br><br>

Aici observam Hm = 206 si Lm = 86, deci acest bloc este valid. Aici vom codifica ultima pereche din mesajul secret. <br><br>
Conform sirului ternar o sa avem: <br>
**86Lm**  86-1  86-1  86+1 <br>
86-1  86+1  86+1  86-2 <br>
86+0 **206Hm** 206+0 206+1 <br>
86+0  86+0  86+0  86+0 <br><br>

Asadar obtinem: <br>
86  85  85  87 <br>
85  87  87  85 <br>
86 206 206 207 <br>
86  86  86  86 <br><br>

Doar aceste blocuri vor fi codificate. Mesajul s-a terminat, asa ca restul blocurilor vor ramane asa cum sunt. <br>
Sirul Ternar cu padding este: [[0, 0, 0, 0, 1, 0, 0, 2, 0, 2, 0, 1, 0, 1], [0, 0, 0, 0, 0, 2, 2, 2, 2, 1, 0, 2, 0, 2], [0, 0, 0, 0, 1, 0, 0, 2, 1, 1, 2, 1, 2, 2]] <br>

Imaginea codificata este: <br>
<img width="600" height="448" alt="Fig 11" src="https://github.com/user-attachments/assets/6667fe86-7433-45f1-a571-8fe96148b77e" /> <br>
Fig 11. Imaginea rezultata in urma codificarii mesajului secret<br><br>

Iar numeric vorbind avem: <br>
<img width="600" height="400" alt="Fig 12" src="https://github.com/user-attachments/assets/29a647a0-072b-4572-ab1b-52604cc2dfb6" /> <br>
Fig 12. Matricea de pixeli dupa codificare <br>


### 4️⃣ Decodificarea mesajului secret (Un exemplu)

Acum urmeaza sa procedam si in sens invers. <br>
O sa prezint o imagine care are un mesaj criptat, dar nu stim care. <br>
Pas cu pas o sa descifram ceea ce este codat acolo. <br>
Avem imaginea cu mesajul codat in pixelii sai: <br>
<img width="600" height="400" alt="Fig 13" src="https://github.com/user-attachments/assets/66b29492-540b-4f21-be4b-6a1f126635bf" /> <br>
Fig 13. Imaginea de la care pornim pt decodificare<br><br>

Diferenta de intensitate a pixelilor este imposibil de vazut cu ochiul liber. <br>

Hai sa vedem si numeric <br>
<img width="800" height="250" alt="Fig 14" src="https://github.com/user-attachments/assets/a1a60514-ca44-4e2a-9921-932dbdd9fcb1" /> <br>
Fig 14. Primele 2 linii din matricea de pixeli<br><br>

Urmeaza sa analizam imaginea in blocuri de 4x4 si sa descifram mesajul secret. <br>
Matricea de pixeli are 64x64 de elemente, adica 16x16 blocuri. De aceea a doua linie incepe de la 17. <br>
Aici avem listate primele 2 linii. Deoarece era greu sa afisez 16 coloane de blocuri cele 2 linii sunt impartite in stanga si dreapta. <br>
Fiecare bloc are numarul sau scris cu verde. <br>
O sa parcurgem fiecare bloc de la 1,2,3... <br>

Acestea fiind spuse, sa ne apucam de treaba. <br>

Primul bloc arata astfel: <br>
192 193 193 145 <br>
191 193 193 192 <br>
145 145 192 193 <br>
145 145 192 192 <br><br>

Scopul nostru este sa identificam Hm si Lm, iar apoi sa extragem secventa ternara. <br>
Acesti 2 pixeli se numesc pixeli de decodificare. <br>
Cum Hm si Lm se afla pe prima pozitie in care respectiva valoare apare, inseamna ca primul element este intotdeauna ori Hm ori Lm. <br>
Asadar 192 este primul pixel de decodificare. <br>
Al doilea astfel de pixel este urmatoarea valoare diferita cu minim 3 de primul pixel. <br>
In cazul nostru se observa ca acesta este valoarea 145 de pe poz(1,4). <br>
Astfel, avem Hm = 192 si Lm = 145. <br><br>
Putem rescrie blocul asa: <br>
**192Hm** 192+1 192+1 **145Lm** <br>
192-1 192+1 192+1 192+0 <br>
145+0 145+0 192+0 192+1 <br>
145+0 145+0 192+0 192+0 <br><br>

Deci secventa noastra este: 11211000010000. Aceasta este in format LSB -> MSB. <br>
Secventa ternara este 00001000011211, deci in binar 01001101_01100101, in zecimal: 77_101, adica in ASCII avem: "Me". <br>
Asadar primul bloc ascunde informatia "**Me**". <br>

Al doilea bloc este: <br>
189 188 107 106 <br>
188 190 190 108 <br>
190 190 190 108 <br>
189 189 107 107 <br><br>

Hm = 189, Lm = 107 <br>

**189Hm** 189-1 **107Lm** 107-1 <br>
189-1 189+1 189+1 107+1 <br>
189+1 189+1 189+1 107+1 <br>
189+0 189+0 107+0 107+0 <br><br>

Avem: 22211111110000, adica 00001111111222 in ternar. <br>
In binar rezulta 01110011_01100001, in zecimal: 115_97, in ASCII: "sa". <br>
Al doilea bloc ascunde "**sa**". <br>

Al treilea bloc are doar 2 valori si diferenta dintre Hm si Lm sub 3, deci il sarim. <br><br>

Blocul nr 4: <br>
86 86 85 86 <br>
87 85 86 87 <br>
86 206 207 207 <br>
86 86 86 86 <br>

Deci: <br>
**86Lm** 86+0 86-1 86+0 <br>
86+1 86-1 86+0 86+1 <br>
86+0 **206Hm** 206+1 206+1 <br>
86+0 86+0 86+0 86+0 <br>

Rezulta: 02012010110000 -> 00001101021020 -> 01101010_00100000 -> 106_32 -> "**j_**"", _ inseamna de fapt space = 32. <br>

Blocul nr 5: <br>
81 82 81 80 <br>
82 80 81 80 <br>
136 81 81 82 <br>
136 136 81 81 <br>

Deci: <br>
**81Lm** 81+1 81+0 81-1 <br>
81+1 81-1 81+0 81-1 <br>
**136Hm** 81+0 81+0 81+1 <br>
136+0 136+0 81+0 81+0 <br>

Rezulta: 10212020010000 -> 00001002021201 -> 01010011_01100101 -> 83_101 -> "**Se**". <br>

Blocul nr 6 are doar valoarea 82, deci Hm = Lm = 82. Nu e nimic codificat acolo. <br>

Blocul nr 7: <br>
81 81 80 95 <br>
80 81 94 94 <br>
82 80 81 96 <br>
81 81 81 81 <br>

Deci: <br>
**81Lm** 81+0 81-1 **95Hm** <br>
81-1 81+0 95-1 95-1 <br>
81+1 81-1 81+0 95+1 <br>
81+0 81+0 81+0 81+0 <br>

Rezulta: 02202212010000 -> 00001021220220 -> 01100011_01110010 -> 99_114 -> "**cr**". <br>

Blocul nr 8: <br>
84 81 82 80 <br>
83 82 80 82 <br>
80 80 81 82 <br>
81 81 81 81 <br>

Aici pare putin ciudat faptul ca aceste valori sunt asa de apropiate, dar blocul este valid. <br>

Deci: <br>
**84Hm** **81Lm** 81+1 81-1 <br>
84-1 81+1 81-1 81+1 <br>
81-1 81-1 81+0 81+1 <br>
81+0 81+0 81+0 81+0 <br>

Rezulta: 12212122010000 -> 00001022121221 -> 01100101_01110100 -> 101_116 -> "**et**". <br>

Blocurile 9 si 10 au doar valoarea 82, deci sunt invalide. <br>

Blocul 11 are doar 2 valori: 81 si 87. Dar acestea nu sunt valori incompatibile pt Hm si Lm. Inseamna ca mesajul s-a terminat daca nu e nimic codat aici. <br>
In continuare, se observa cum toate blocurile au doar 2 valori, confirmand faptul ca de aici nu mai exista niciun mesaj codat. <br><br>

Acum hai sa concatenam perechile gasite pana acum. <br>
Rezultatul final este "**Mesaj Secret**". <br>
Astfel am reusit sa descifram ceea ce era ascuns in pixelii imaginii. <br>
<br>

### Bibliografie si referinte: <br>
[1] https://ocw.cs.pub.ro/courses/_media/ac-is/teme/tema2/articol.pdf <br>
[2] https://ocw.cs.pub.ro/courses/ac-is/teme/tema2 (Ideea temei) <br>
[3] https://calculator.name/base-converter/ternary/binary <br>
