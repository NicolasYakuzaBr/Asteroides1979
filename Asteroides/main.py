import pygame
import random 
import math 

# Iniciar módulo
pygame.init()
pygame.font.init()
# ----------------

# Janela
largura = 800
altura = 600
janela = pygame.display.set_mode((largura, altura))
icon = pygame.image.load('AsTI.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Asteroides')
fundo = pygame.image.load('Menu.png')
# ----------------------------------------------------

# Menu + Musicas (Em construção!)
pygame.mixer.music.load('menu+.wav')
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1)
som = True
som_enter = pygame.mixer.Sound('coin.wav')

def menu():
    rodando_menu = True
    img_menu = pygame.image.load('MainMenu.png')
    while rodando_menu:
        janela.blit(fundo, (0,0))
        janela.blit(img_menu, (largura//2 - img_menu.get_width()//2, altura//2 - img_menu.get_height()//2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando_menu = False
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    som_enter.play()
                    rodando_menu = False
        pygame.display.update()

menu()


# Player ( A Fazer)

# Asteroids (A Fazer)

# Colisão  (A Fazer)

# Movimento  (A Fazer)

# Provalvente tem outras coisas para fazer ainda mas eu esqueci, se der erro eu lembro kkk<3







rodando = True
while rodando:
    janela.blit(fundo, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False   
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                 som = not som
                 if som:
                      pygame.mixer.music.set_volume(1.0)
                      pygame.mixer.music.play(-1)
                 else:
                      pygame.mixer.music.set_volume(0.0)
                      pygame.mixer.music.stop()

    score = 0
    high_score = 0
    if score > high_score:
        high_score = score

    arcade_font = pygame.font.Font('font/ARCADE_N.TTF', 10)
    ponto_text = arcade_font.render(f'Score:{score}', True, (255, 255, 255))
    janela.blit(ponto_text, (10, 10))

    high_score_text = arcade_font.render(f'High Score:{high_score}', True, (255, 255, 255))
    janela.blit(high_score_text, (10, 30))

    pygame.display.update()

pygame.quit()
