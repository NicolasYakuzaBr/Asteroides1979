import pygame
import random 
import math 
import sys


# Bugs - Hitbox do jogador com o asteroide, ressurgimento dos asteroides, música principal que não para mesmo no menu de game over e impede outras músicas ou efeitos sonoros sejam reproduzidos
# Bugs 2 - atirar não funciona enquanto se move para a esquerda e se move para frente
# Dimensão Player(50x50), asteroide 50 (50x50), asteroide_100(100x100), asteroide_150(150x150)

# Iniciar módulo
pygame.init()
pygame.font.init()

# Janela
largura = 800
altura = 600
janela = pygame.display.set_mode((largura, altura))
icon = pygame.image.load('AsTI.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Asteroides')
fundo = pygame.image.load('Menu.png')
clock = pygame.time.Clock()
# ----------------------------------------------------

# Menu + Musicas (Em construção!)
def menu():
    pygame.mixer.music.load('menu+.wav')
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(-1)
    som_enter = pygame.mixer.Sound('coin.wav')
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

tiros_som = pygame.mixer.Sound('laser.wav')
colisao_som = pygame.mixer.Sound('explosion.wav')

# Player ( Atenção)
class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('nave.png')
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.angle = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle += self.speed
        if keys[pygame.K_RIGHT]:
            self.angle -= self.speed

        # Girar a imagem do jogador em torno do centro
        self.image = pygame.transform.rotate(pygame.image.load('nave.png'), self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Movimento do jogador
        if keys[pygame.K_UP]:
            dx = -self.speed * math.sin(math.radians(self.angle))
            dy = -self.speed * math.cos(math.radians(self.angle))
            self.rect.move_ip(dx, dy)
        if keys[pygame.K_DOWN]:
            dx = self.speed * math.sin(math.radians(self.angle))
            dy = self.speed * math.cos(math.radians(self.angle))
            self.rect.move_ip(dx, dy)

        # Fazer o jogador aparecer do outro lado da tela ao encostar nas bordas
        if self.rect.left > largura:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = largura
        if self.rect.bottom < 0:
            self.rect.top = altura
        if self.rect.top > altura:
            self.rect.bottom = 0
        if pygame.sprite.spritecollide(self, grupo_asteroides, True):
            print("O jogador colidiu com um asteroide!")
            colisao_som.play()
            global vidas 
            vidas -= 1
            print('Vidas:', vidas)  
        janela.blit(self.image, self.rect)
player = Player(largura//2, altura//2)


vidas = 3
game_over = False
congelar = False

# Asteroides
class Asteroide(pygame.sprite.Sprite):
    def __init__(self, imagem, x, y):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2
        self.angle = random.randint(0, 360)

    def update(self):
        dx = -self.speed * math.sin(math.radians(self.angle))
        dy = -self.speed * math.cos(math.radians(self.angle))
        self.rect.move_ip(dx, dy)

        # Fazer o asteroide aparecer do outro lado da tela ao encostar nas bordas
        if self.rect.left > largura:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = largura
        if self.rect.bottom < 0:
            self.rect.top = altura
        if self.rect.top > altura:
            self.rect.bottom = 0

        asteroides_destruidos = pygame.sprite.spritecollide(self, grupo_tiros, True)
        if asteroides_destruidos:
            grupo_asteroides.add(Asteroide(random.choice(imagens_asteroides), random.randint(0, largura), random.randint(0, altura)))
            print("Um tiro destruiu um asteroide!")
        if asteroides_destruidos:
            colisao_som.play()
        if asteroides_destruidos:
            global score
            global high_score
            score += 50
        if score > high_score:
            high_score = score
        if asteroides_destruidos:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

grupo_asteroides = pygame.sprite.Group()

imagem_asteroide_50 = pygame.image.load('Asteroids/50.png')
imagem_asteroide_100 = pygame.image.load('Asteroids/100.png')
imagem_asteroide_150 = pygame.image.load('Asteroids/150.png')
imagens_asteroides = [imagem_asteroide_50, imagem_asteroide_150, imagem_asteroide_100]


# Adicionar asteroides ao grupo
for i in range(6):
    x = random.randint(0, largura)
    y = random.randint(0, altura)
    imagem = random.choice([imagem_asteroide_50, imagem_asteroide_100, imagem_asteroide_150])
    asteroide = Asteroide(imagem, x, y)
    grupo_asteroides.add(asteroide)

# Tiros
class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()

        # Cria uma superfície vazia para representar o tiro
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)

        # Desenha um círculo branco no centro do tiro
        pygame.draw.circle(self.image, (255, 255, 255), (5, 5), 2)

        # Rotaciona a imagem para a direção correta
        self.image = pygame.transform.rotate(self.image, -angle)

        # Define o retângulo de colisão com base na posição do tiro
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10
        self.angle = angle
        
    def update(self):
        dx = -self.speed * math.sin(math.radians(self.angle))
        dy = -self.speed * math.cos(math.radians(self.angle))
        self.rect.move_ip(dx, dy)

        if self.rect.left > largura or self.rect.right < 0 or self.rect.top > altura or self.rect.bottom < 0:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    tiros_som = pygame.mixer.Sound('laser.wav')
grupo_tiros = pygame.sprite.Group()

# Pontos
score = 0
high_score = 0

# Var_Global
game_over = False
congelar = False
rodando = True
som = True  

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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    tiro = Tiro(player.rect.centerx, player.rect.centery, player.angle)
                    grupo_tiros.add(tiro)
                    tiros_som.play()

    if score > high_score:
        high_score = score
    arcade_font = pygame.font.Font('font/ARCADE_N.TTF', 10)
    ponto_text = arcade_font.render(f'Score:{score}', True, (255, 255, 255))
    janela.blit(ponto_text, (10, 10))
    high_score_text = arcade_font.render(f'High Score:{high_score}', True, (255, 255, 255))
    janela.blit(high_score_text, (10, 30))

    vida_fonte = pygame.font.Font('font/ARCADE_N.TTF', 10)
    vida_texto = arcade_font.render(f'lifes:{vidas}', True, (255, 255, 255))
    janela.blit(vida_texto, (10, 50))

    if vidas == 0:
        game_over = True
        congelar = True

    if game_over == True:
       gm = pygame.image.load('GM.png')
       lista_gm = []


    while congelar:
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
            game_over = True
            pygame.quit
            sys.exit()
        janela.blit(gm, (0,0))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                game_over = False
                congelar = False
                score = 0
                vidas = 3
                grupo_asteroides.empty()
                grupo_tiros.empty()
                player.rect.centerx = largura // 2
                player.rect.centery = altura // 2
                player.angle = 0
                for i in range(6):
                    x = random.randint(0, largura)
                    y = random.randint(0, altura)
                    imagem = random.choice([imagem_asteroide_50, imagem_asteroide_100, imagem_asteroide_150])
                    asteroide = Asteroide(imagem, x, y)
                    grupo_asteroides.add(asteroide)

        pygame.display.update()

    for asteroide in grupo_asteroides:
        asteroide.update()
        asteroide.draw(janela)
        
    for tiro in grupo_tiros:
        tiro.update()
        tiro.draw(janela)

    player.update()
    pygame.display.update()

pygame.quit()

