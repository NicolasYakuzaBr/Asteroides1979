import pygame
import random 
import math 

# Tentando clonar o Jogo Asteroids lançado em 1979 (Coisas a fazer: Colisão, Jogador, Asteroides, Menu)

# Iniciar módulo 
pygame.init()

# Janela
largura = 800
altura = 600
janela = pygame.display.set_mode((largura, altura))
icon = pygame.image.load('AsTI.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Asteroides')
fundo = pygame.image.load('AsTF.png')

# ----------------------------------------------------

# Menu + Musicas (Em construção!)

pygame.mixer.music.load('')
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1)
som = True

# Coloque sua música!, não pude deixar a minha pois tinha 34 MB, e lembre se que o formato é WAV

rodando = True

while rodando:
    janela.blit(fundo, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = not True   
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                     som = not som
                     if som:
                          pygame.mixer.music.set_volume(1.0)
                          pygame.mixer.music.play(-1)
                     else:
                          pygame.mixer.music.set_volume(0.0)
                          pygame.mixer.music.stop()
    pygame.display.update()

pygame.quit()
