import math
import random

import pygame

from const import ALTURA_TELA, BRANCO, DIST_ENEMY2, LARGURA_TELA, SHOT_DAMAGE, SHOT_RATE, SHOT_SPEED, TAM_ENEMY2, TAM_SHOT_PLAYER, TAMANHO_ENEMY, TITULO, VEL_ENEMY, VEL_ENEMY2, VERDE, VERMELHO, TAMANHO_PLAYER, VEL_PLAYER, VIDA_PLAYER, DANO_COLISAO, VEL_SHOT_PLAYER


# Configurações da tela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption(TITULO)
relogio = pygame.time.Clock()

# MENU
menu_bg = pygame.image.load('./asset/bgmenu.png').convert_alpha()
menu_bg = pygame.transform.scale(menu_bg, (LARGURA_TELA, ALTURA_TELA))
game_mode = None

def draw_text(surface, text, size, color, center):
  font = pygame.font.SysFont("arial", size)
  text_surface = font.render(text, True, color)
  text_rect = text_surface.get_rect(center=center)
  surface.blit(text_surface, text_rect)

def main_menu(screen):
  menu_running = True
  click = False
  pygame.mixer_music.load('./asset/menusong.wav') #música do menu
  pygame.mixer_music.play(-1) #música em loop
  while menu_running:
      screen.blit(menu_bg, (0,0)) #fundo do menu

      #título
      draw_text(screen, "Spaceship Shooter", 48, (BRANCO), (LARGURA_TELA // 2, ALTURA_TELA // 4))

      #botões
      mx, my = pygame.mouse.get_pos()

      #define botões
      buttons = {
          "New Game - Normal": pygame.Rect(LARGURA_TELA // 2 - 150, ALTURA_TELA // 2 - 30, 300, 50),
          "New Game - Hard": pygame.Rect(LARGURA_TELA // 2 - 150, ALTURA_TELA // 2 + 40, 300, 50),
          "Exit": pygame.Rect(LARGURA_TELA // 2 - 150, ALTURA_TELA // 2 + 100, 300, 50)
      }

      for name, rect in buttons.items():
          color = (70, 70, 70)
          if rect.collidepoint((mx, my)):
              color = (100, 100, 100)
              if click:
                  if name == "New Game - Normal":
                      pygame.time.set_timer(SPAWN_INIMIGO_EVENT, 2000)
                      return
                  elif name == "New Game - Hard":
                      pygame.time.set_timer(SPAWN_INIMIGO_EVENT, 1000)
                      return
                  elif name == "Exit":
                      pygame.quit()
                      sys.exit()
          pygame.draw.rect(screen, color, rect)
          draw_text(screen, name, 28, (255, 255, 255), rect.center)

      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()
          if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
              click = True

      pygame.display.flip()
      pygame.time.Clock().tick(60)

# Imagens de Fundo para Paralaxe
fundo1 = pygame.image.load('./asset/imagembg1.png').convert_alpha()
fundo2 = pygame.image.load('./asset/imagembg2.png').convert_alpha()
fundo3 = pygame.image.load('./asset/imagembg3.png').convert_alpha()

# Escala para o tamanho da tela
fundo1 = pygame.transform.scale(fundo1, (LARGURA_TELA, ALTURA_TELA))
fundo2 = pygame.transform.scale(fundo2, (LARGURA_TELA, ALTURA_TELA))
fundo3 = pygame.transform.scale(fundo3, (LARGURA_TELA, ALTURA_TELA))

# Variáveis de Paralaxe
bg1_y = 0
bg2_y = 0
bg3_y = 0

pygame.init()

# Fontes
fonte = pygame.font.Font(None, 36)
fonte_game_over = pygame.font.Font(None, 72)

# Carregamento das Imagens

player_img = pygame.image.load('./asset/player.png').convert_alpha()
player_shot_img = pygame.image.load('./asset/shot.png').convert_alpha()

# Sprites dos inimigos
enemy_chaser_img = pygame.image.load('./asset/enemy.png').convert_alpha()
enemy_shooter_img = pygame.image.load('./asset/enemy_shooter.png').convert_alpha() 

# Sprites dos tiros dos inimigos
enemy_shot_red_img = pygame.image.load('./asset/enemy_shot_red.png').convert_alpha() 
enemy_shot_purple_img = pygame.image.load('./asset/enemy_shot_purple.png').convert_alpha()

# Classes do Jogo

class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imagem_original = pygame.transform.scale(player_img, TAMANHO_PLAYER)
        self.image = self.imagem_original
        self.rect = self.image.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA / 2))
        self.velocidade = VEL_PLAYER
        self.vida = VIDA_PLAYER
        self.dano_colisao = DANO_COLISAO # Dano que o jogador sofre ao colidir
    def update(self, *args, **kwargs):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a]: self.rect.x -= self.velocidade
        if teclas[pygame.K_d]: self.rect.x += self.velocidade
        if teclas[pygame.K_w]: self.rect.y -= self.velocidade
        if teclas[pygame.K_s]: self.rect.y += self.velocidade

        # Manter dentro da tela
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(LARGURA_TELA, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(ALTURA_TELA, self.rect.bottom)

        pos_mouse = pygame.mouse.get_pos()
        dx, dy = pos_mouse[0] - self.rect.centerx, pos_mouse[1] - self.rect.centery
        angulo = math.degrees(math.atan2(-dy, dx)) - 90

        self.image = pygame.transform.rotate(self.imagem_original, angulo)
        self.rect = self.image.get_rect(center=self.rect.center)

    def atirar(self):
        return ProjetilJogador(self.rect.center, pygame.mouse.get_pos())

class ProjetilJogador(pygame.sprite.Sprite):
    def __init__(self, pos_inicial, pos_mouse):
        super().__init__()
        self.image = pygame.transform.scale(player_shot_img, TAM_SHOT_PLAYER)
        self.rect = self.image.get_rect(center=pos_inicial)
        self.velocidade = VEL_SHOT_PLAYER

        dx, dy = pos_mouse[0] - pos_inicial[0], pos_mouse[1] - pos_inicial[1]
        distancia = math.hypot(dx, dy)
        if distancia == 0: distancia = 1
        self.dx, self.dy = dx / distancia, dy / distancia

        angulo = math.degrees(math.atan2(-self.dy, self.dx)) - 90
        self.image = pygame.transform.rotate(self.image, angulo)

    def update(self, *args, **kwargs):
        self.rect.x += self.dx * self.velocidade
        self.rect.y += self.dy * self.velocidade
        if not tela.get_rect().colliderect(self.rect): self.kill()

# Classe base para projéteis de inimigos 
class ProjetilInimigo(pygame.sprite.Sprite):
    def __init__(self, pos_inicial, jogador, imagem, tamanho, velocidade, dano):
        super().__init__()
        self.image = pygame.transform.scale(imagem, tamanho)
        self.rect = self.image.get_rect(center=pos_inicial)
        self.velocidade = velocidade
        self.dano = dano

        dx, dy = jogador.rect.centerx - pos_inicial[0], jogador.rect.centery - pos_inicial[1]
        distancia = math.hypot(dx, dy)
        if distancia == 0: distancia = 1
        self.dx, self.dy = dx / distancia, dy / distancia

        angulo = math.degrees(math.atan2(-self.dy, self.dx)) - 90
        self.image = pygame.transform.rotate(self.image, angulo)

    def update(self, *args, **kwargs):
        self.rect.x += self.dx * self.velocidade
        self.rect.y += self.dy * self.velocidade
        if not tela.get_rect().colliderect(self.rect): self.kill()


# Classes de Inimigos

class InimigoPerseguidor(pygame.sprite.Sprite):
    # Inimigo que apenas persegue o jogador.
    def __init__(self, jogador):
        super().__init__()
        self.jogador = jogador
        self.imagem_original = pygame.transform.scale(enemy_chaser_img, TAMANHO_ENEMY)
        self.image = self.imagem_original
        self.rect = self.image.get_rect()
        self.velocidade = VEL_ENEMY
        self.dano_colisao = DANO_COLISAO # Dano que causa ao colidir

        # Posição inicial aleatória
        borda = random.choice(['top', 'bottom', 'left', 'right'])
        if borda == 'top': self.rect.midbottom = (random.randint(0, LARGURA_TELA), 0)
        elif borda == 'bottom': self.rect.midtop = (random.randint(0, LARGURA_TELA), ALTURA_TELA)
        elif borda == 'left': self.rect.midright = (0, random.randint(0, ALTURA_TELA))
        else: self.rect.midleft = (LARGURA_TELA, random.randint(0, ALTURA_TELA))

    def update(self, *args, **kwargs):
        dx, dy = self.jogador.rect.centerx - self.rect.centerx, self.jogador.rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)
        if distancia > 0:
            self.rect.x += (dx / distancia) * self.velocidade
            self.rect.y += (dy / distancia) * self.velocidade

        angulo = math.degrees(math.atan2(-dy, dx)) - 90
        self.image = pygame.transform.rotate(self.imagem_original, angulo)
        self.rect = self.image.get_rect(center=self.rect.center)


class InimigoAtirador(pygame.sprite.Sprite):
    # Inimigo que mantém distância e atira.
    def __init__(self, jogador):
        super().__init__()
        self.jogador = jogador
        self.imagem_original = pygame.transform.scale(enemy_shooter_img, TAM_ENEMY2)
        self.image = self.imagem_original
        self.rect = self.image.get_rect()
        self.velocidade = VEL_ENEMY2
        self.dano_colisao = DANO_COLISAO
        self.distancia_ideal = DIST_ENEMY2 # Distância que tenta manter do jogador

        # Atributos de tiro
        self.frequencia_tiro = SHOT_RATE # 2000 ms = 2 segundos
        self.ultimo_tiro = pygame.time.get_ticks()
        self.tiro_imagem = enemy_shot_purple_img
        self.tiro_dano = SHOT_DAMAGE
        self.tiro_velocidade = SHOT_SPEED

        borda = random.choice(['top', 'bottom', 'left', 'right'])
        if borda == 'top': self.rect.midbottom = (random.randint(0, LARGURA_TELA), 0)
        elif borda == 'bottom': self.rect.midtop = (random.randint(0, LARGURA_TELA), ALTURA_TELA)
        elif borda == 'left': self.rect.midright = (0, random.randint(0, ALTURA_TELA))
        else: self.rect.midleft = (LARGURA_TELA, random.randint(0, ALTURA_TELA))

    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > self.frequencia_tiro:
            self.ultimo_tiro = agora
            return ProjetilInimigo(self.rect.center, self.jogador, self.tiro_imagem, (20,20), self.tiro_velocidade, self.tiro_dano)
        return None

    def update(self, *args, **kwargs):
        dx, dy = self.jogador.rect.centerx - self.rect.centerx, self.jogador.rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)

        # Movimento: Afasta-se se estiver muito perto, aproxima-se se longe
        if distancia > 0:
            if distancia < self.distancia_ideal: # muito perto, afasta
                self.rect.x -= (dx / distancia) * self.velocidade
                self.rect.y -= (dy / distancia) * self.velocidade
            else: # longe, aproxima
                self.rect.x += (dx / distancia) * self.velocidade
                self.rect.y += (dy / distancia) * self.velocidade

        angulo = math.degrees(math.atan2(-dy, dx)) - 90
        self.image = pygame.transform.rotate(self.imagem_original, angulo)
        self.rect = self.image.get_rect(center=self.rect.center)


# Grupos de Sprites
todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
projeteis_jogador = pygame.sprite.Group() 
projeteis_inimigos = pygame.sprite.Group() # NOVO grupo

jogador = Jogador()
todos_sprites.add(jogador)

# Variáveis do Jogo
pontuacao = 0
game_over = False
SPAWN_INIMIGO_EVENT = pygame.USEREVENT + 1

# Loop Principal
rodando = True
main_menu(tela)
# música do jogo
pygame.mixer_music.load('./asset/gamesong.wav') # música do jogo
pygame.mixer_music.play(-1) # música em loop

while rodando:
    # Atualiza posições das camadas de fundo
    bg1_y += 0.05  # camada mais distante
    bg2_y += 0.06  # camada intermediária
    bg3_y += 0.1  # camada mais próxima

    # Reinicia o loop vertical
    if bg1_y >= ALTURA_TELA: bg1_y = 0
    if bg2_y >= ALTURA_TELA: bg2_y = 0
    if bg3_y >= ALTURA_TELA: bg3_y = 0
    relogio.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: rodando = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and event.button == 1:
            tiro = jogador.atirar()
            todos_sprites.add(tiro); projeteis_jogador.add(tiro)
        if event.type == SPAWN_INIMIGO_EVENT and not game_over:
            # Escolhe aleatoriamente qual inimigo criar
            tipo_inimigo = random.choice([InimigoPerseguidor, InimigoAtirador])
            inimigo = tipo_inimigo(jogador)
            todos_sprites.add(inimigo); inimigos.add(inimigo)
        if event.type == pygame.KEYDOWN and game_over and event.key == pygame.K_r:
            # Reinicia o jogo
            game_over = False; pontuacao = 0
            todos_sprites.empty(); inimigos.empty(); projeteis_jogador.empty(); projeteis_inimigos.empty()
            jogador = Jogador()
            todos_sprites.add(jogador)
        if event.type == pygame.KEYDOWN and game_over and event.key == pygame.K_m:
            # Retorna ao menu
            main_menu(tela)
            

    if not game_over:
        todos_sprites.update()

        # Inimigos Atiradores tentam atirar
        for inimigo in inimigos:
            if isinstance(inimigo, InimigoAtirador):
                tiro = inimigo.atirar()
                if tiro:
                    todos_sprites.add(tiro); projeteis_inimigos.add(tiro)

        # Tiros do jogador acertam inimigos
        colisoes_tiro_inimigo = pygame.sprite.groupcollide(projeteis_jogador, inimigos, True, True)
        for tiro, inimigo_atingido in colisoes_tiro_inimigo.items():
            pontuacao += 10

        # Tiros inimigos acertam o jogador
        colisoes_tiro_jogador = pygame.sprite.spritecollide(jogador, projeteis_inimigos, True)
        for tiro in colisoes_tiro_jogador:
            jogador.vida -= tiro.dano

        # Inimigos colidem com o jogador
        colisoes_inimigo_jogador = pygame.sprite.spritecollide(jogador, inimigos, True)
        for inimigo in colisoes_inimigo_jogador:
            jogador.vida -= inimigo.dano_colisao

        if jogador.vida <= 0:
            jogador.vida = 0
            game_over = True

    # Desenho do Fundo com Paralaxe
    tela.blit(fundo1, (0, bg1_y - ALTURA_TELA))
    tela.blit(fundo1, (0, bg1_y))
    tela.blit(fundo2, (0, bg2_y - ALTURA_TELA))
    tela.blit(fundo2, (0, bg2_y))
    tela.blit(fundo3, (0, bg3_y - ALTURA_TELA))
    tela.blit(fundo3, (0, bg3_y))

    todos_sprites.draw(tela)

    # HUD
    texto_vida = fonte.render(f"Vida: {jogador.vida}", True, VERDE)
    tela.blit(texto_vida, (10, 10))
    texto_pontuacao = fonte.render(f"Pontuação: {pontuacao}", True, BRANCO)
    tela.blit(texto_pontuacao, (LARGURA_TELA - texto_pontuacao.get_width() - 10, 10))
    pygame.draw.rect(tela, VERMELHO, (10, 40, 100, 10))
    if jogador.vida > 0:
        pygame.draw.rect(tela, VERDE, (10, 40, jogador.vida, 10))

    if game_over:
        texto_go = fonte_game_over.render("GAME OVER", True, VERMELHO)
        texto_restart = fonte.render("Pressione 'R' para reiniciar", True, BRANCO)
        texto_menu = fonte.render("Pressione 'M' para voltar ao menu", True, BRANCO)
        tela.blit(texto_go, (LARGURA_TELA/2 - texto_go.get_width()/2, ALTURA_TELA/2 - texto_go.get_height()/2))
        tela.blit(texto_restart, (LARGURA_TELA/2 - texto_restart.get_width()/2, ALTURA_TELA/2 + 50))
        tela.blit(texto_menu, (LARGURA_TELA/2 - texto_menu.get_width()/2, ALTURA_TELA/2 + 80))

    pygame.display.flip()

pygame.quit()