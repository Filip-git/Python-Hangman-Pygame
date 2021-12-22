import pygame
import math
import random
import os
from pygame import mixer  #import za zvukove
pygame.mixer.init()       #import za zvukove

#setup prozora programa
pygame.init() 
WIDTH, HEIGHT = 800, 500                           #inicijalizacija varijabli koje ću koristiti kao visinu i širinu prozora programa. Velikim slovom jer su to konstantne i neće se mijenjati nikako
PROZOR = pygame.display.set_mode((WIDTH, HEIGHT))  #inicijalizacija prozora 
pygame.display.set_caption("HANGMAN PYGAME - FILIP OROZ")       #naslov prozora programa                                   

#pozadinska muzika
music = pygame.mixer.music.load(os.path.join("zvukovi", 'pozadinski.mp3')) #odabir pjesme iz direktorija "zvukovi"
pygame.mixer.music.play(-1)                                                #pozadinska muzika na loop 


# varijable za buttone
RADIUS = 20
RAZMAK = 15
slova = []  #lista u koju ću staviti sva slova 
startx = round((WIDTH - (RADIUS * 2 + RAZMAK) * 13) / 2) #koordinata x
starty = 400 #koordinata y
A = 65 #prvo slovo

for i in range (26):
    x = startx + RAZMAK * 2 + ((RADIUS * 2 + RAZMAK) * ( i % 13))  #i%13 daje ostatak 
    y = starty + ((i // 13) * (RAZMAK + RADIUS * 2))
    slova.append([x, y, chr(A + i), True]) #karakter od 65 + i , a karakter 65 je A


#fontovi
slova_font = pygame.font.SysFont('comicsans', 40)            #font i veličina slova
rijec_font = pygame.font.SysFont('dejavusansmono', 40)       #font i veličina rijeci
naslov_font = pygame.font.SysFont('comicsans', 70)           #font i veličina naslova
potpis_font = pygame.font.SysFont('javanesetext', 65)           #font i veličina potpisa


#učitavanje slika
images = [] #lista slika
for i in range(7):
    image = pygame.image.load(os.path.join("Slike","hangman" + str(i) + ".png"))
    images.append(image)          #dodavanje slike u listu


# game varijable
hangman_status = 0     # varijabla pogriješenih slova da znam koja mi slika treba 
riječi = ["PYTHON", "HANGMAN", "PYGAME", "ETHEREUM"] #lista riječi za pogadanje
riječ = random.choice(riječi) #riječ je random izabrana iz liste riječi
pogodeno = []  #lista slova koja su pogodena


#boje
BIJELA = (255,255,255)  #varijabla bijele RGB boje
CRNA = (0,0,0)          #varijabla crne RGB boje
POTPIS_BOJA = (31,206,170) #varijabla boje potpisa


# setup game loop
FPS = 60  #frames per second
clock = pygame.time.Clock() 
run = True

def draw():                #funkcija za crtanje
    PROZOR.fill((BIJELA))  #postavljanje boje prozora, sa bojom u RGB

    text = naslov_font.render("Dobrodošli!", 1 , CRNA)    #render texta
    PROZOR.blit(text, (WIDTH/2 - text.get_width()/2, 20)) #blitanje texta na prozor

    # draw loop
    display_word = ""
    for slovo in riječ:
        if slovo in pogodeno:
            display_word += slovo + " " #iduće slovo da bude odvojeno od proslog zato space
        else: #ako nije pogodeno
            display_word += "_ " #nepogodeni

    text = rijec_font.render(display_word, 1, CRNA)
    PROZOR.blit(text, (400, 200))
    

    #crtanje buttona
    for slovo in slova:
        x,y,ltr, vidljivo = slovo 
        if vidljivo:
            pygame.draw.circle(PROZOR, CRNA, (x, y), RADIUS, 3)
            text = slova_font.render(ltr, 1, CRNA) #render slova u crnoj boji
            PROZOR.blit(text, (x - text.get_width()/2 , y - text.get_height()/2 )) #piši na prozor text na koordinate na sredinu 

    PROZOR.blit(images[hangman_status], (150, 100)) #blit override sve preko filla, i crta po prozoru. Uzimam sliku iz liste images sa indeksom hangman status i stavljam je na koordinate 150, 100
    pygame.display.update()  #update prozora


def ispis_poruke(poruka):    #metoda s parametrom poruka 
     pygame.time.delay(1000) #delay 1 sec, 1000 ms
     PROZOR.fill(BIJELA)     #ispuni ekran samo bijelom bojom
     text = rijec_font.render(poruka, 1, CRNA) #render teksta
     PROZOR.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2 )) #blitanje na ekran
     potpis = potpis_font.render("Filip Oroz", 1 , POTPIS_BOJA)    #render texta za potpis
     PROZOR.blit(potpis, (WIDTH/2 - potpis.get_width()/2, 395 )) #blitanje texta potpisa na prozor
     pygame.display.update()  #update ekrana
     pygame.time.delay(3000)  #3sec delay, 3 sec trajanje teksta 


while run:          #dok je god varijabla run true, petlja se izvrsava
    clock.tick(FPS) #otkucaji FPS brzinom
    
    for event in pygame.event.get():  #svaki event koji bude će se dodati
        if event.type == pygame.QUIT: # provjerava je li kliknuto X na prozoru gašenje programa
            run = False               # ako je kliknuto, onda varijablu run stavlja na false i gasi petlju
        if event.type == pygame.MOUSEBUTTONDOWN:  #ako je kliknuto mišem 
            miš_x, miš_y = pygame.mouse.get_pos() #dobivanje koordinata miša
            for slovo in slova:
                x,y,ltr, vidljivo = slovo
                if vidljivo:
                    dis = math.sqrt((x - miš_x) **2 + (y - miš_y) **2 ) #dobivanje distance izmedu misa i slova
                    if dis < RADIUS:
                        slovo[3] = False     #ne pokazuj slovo
                        pogodeno.append(ltr) #dodaj ga u listu slova "pogodeno"
                        if ltr in riječ:
                            pogodak = mixer.Sound(os.path.join("zvukovi",'pogodak.wav'))  #inicijalizacija zvuka pogotka
                            pogodak.play() #puštanje zvuka pogotka
                        if ltr not in riječ: #ako odabrano slovo nije u traženoj riječi
                            kiks = mixer.Sound(os.path.join("zvukovi",'pogresno_slovo.wav'))  #inicijalizacija zvuka pogreške
                            kiks.play() #puštanje zvuka pogreške
                            hangman_status += 1 #povecaj hangman_status za 1, tj. promijeni sliku iz liste za 1
    
    draw()   #pozivanje funkcije draw

    pobjeda = True
    for slovo in riječ:
        if slovo not in pogodeno:
            pobjeda = False
            break #izlazak iz petlje
    
    if pobjeda:
        pygame.mixer.music.stop()
        win = mixer.Sound(os.path.join("zvukovi",'win.wav'))  #inicijalizacija zvuka pobjede
        win.play() #puštanje zvuka pobjede
        ispis_poruke("Pobjeda!") #metoda s parametrom pobjeda
        break

    if hangman_status == 6:
        pygame.mixer.music.stop()
        gameover = mixer.Sound(os.path.join("zvukovi",'gameover.wav'))  #inicijalizacija gameover zvuka   
        gameover.play() #puštanje gameover zvuka
        ispis_poruke("Izgubili ste!") #metoda s parametrom izgubili ste
        break 

pygame.quit()