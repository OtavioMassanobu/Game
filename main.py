import pygame
import sys

from player import Player
from enemy import Enemy, Boss
from random import choice, randint
from shoot import Shoot
import shoot


class Game():
    def __init__(self): #construtor
        #player setup
        player_sprite = Player((SCREEN_HEIGHT / 2,SCREEN_WIDTH),SCREEN_WIDTH,5) # player na parte inferior da tela / com restricao de borda da tela e restricao de velocidade
        self.player = pygame.sprite.GroupSingle(player_sprite)

        #sistema de lives/health and score
        self.lives = 3
        self.live_surf = pygame.image.load('/home/otavio/OO/Projeto PyGame/graphics/player.png').convert_alpha() #exibindo no canto superior da tela
        self.live_x_start_pos = SCREEN_WIDTH - (self.live_surf.get_size()[0] * 2 + 20) #aparecer na tela em x #2 para largura e 20 para deslocamneto na tela como se fosse um offset
        self.score = 0 #metodo de criacao do score
        self.font = pygame.font.Font('/home/otavio/OO/Projeto PyGame/font/Pixeled.ttf', 15) #fonte para o texto
        #enemy setup
        self.enemys = pygame.sprite.Group() #enemys estarao nesse grupo
        self.enemy_shoots = pygame.sprite.Group()
        self.total_enemies = 6 * 8 #numero total de enemies
        self.enemies_destroyed = 0 #contador
        self.enemy_setup(rows=6,cols=8) #funcao que ira criar os enemys em posicoes especificas
        self.enemy_direction = 1

        #boss setup
        self.boss = pygame.sprite.GroupSingle() #grupo somente para o boss para nao atrapalhar a logica dos outros enemys
        self.boss_spawn_time = randint(40,80)

        #audio
        music = pygame.mixer.Sound('/home/otavio/OO/Projeto PyGame/audio/piratas.mp3')
        music.set_volume(0.0)
        music.play(loops = -1)
        self.shoot_sound = pygame.mixer.Sound('/home/otavio/OO/Projeto PyGame/audio/canon.mp3')
        self.shoot_sound.set_volume(0.0)
        self.explosion_sound = pygame.mixer.Sound('/home/otavio/OO/Projeto PyGame/audio/explosaot.mp3')
        self.explosion_sound.set_volume(0.0)
    def enemy_setup(self,rows,cols,distance_x = 60,distance_y = 48, offset_x = 70, offset_y = 100): #criacao dos enemys
        for row_index, row in enumerate(range(rows)): #manipulacao de linhas
            for col_index, col in enumerate(range(cols)): #manipulacao de colunas
                x = col_index * distance_x + offset_x#indice da coluna #distancia x entre os enemys #offset x para nao iniciarem todos no canto superior esquerdo
                y = row_index * distance_y + offset_y#indice da linha #distancia y entre os enemys #offset x para nao iniciarem todos no canto superior esquerdo
                
                if row_index == 0: enemy_sprite = Enemy('inimigo1',x,y) #a partir da linha vamos saber qual tipo de enemy que estara la #yellow
                elif 1 <= row_index <= 2: enemy_sprite = Enemy('inimigo2',x,y) #green
                else: enemy_sprite = Enemy('inimigo3',x,y) #red
                self.enemys.add(enemy_sprite)

    def enemy_setup_check(self): #movimento dos enemys para ambos os lados
        all_enemys = self.enemys.sprites() #quando atingirem o limite para direita ele inverte a direcao e vice-versa
        for enemy in all_enemys:
            if enemy.rect.right >= SCREEN_WIDTH:
                self.enemy_direction = -1
                self.enemy_move_down(2)
            elif enemy.rect.left <= 0:
                self.enemy_direction = 1
                self.enemy_move_down(2)
    

    def enemy_move_down(self, distance): #movimenta a matriz de anemys levemente para baixo
        if self.enemys: #se o player abater todos os enemys nao precisa mais do metodo
            for enemy in self.enemys.sprites():
                enemy.rect.y += distance
    
    '''def enemy_shoot(self):
        if self.enemys.sprites():
            random_enemy = choice(self.enemys.sprites()) #randomiza qual enemy que atira
            shoot_sprite = Shoot(random_enemy.rect.center,6,SCREEN_HEIGHT)
            self.enemy_shoots.add(shoot_sprite)
            self.shoot_sound.play()'''

    def enemy_shoot(self):
        if self.enemys.sprites():
            # Chama a função para aumentar a taxa de disparo dos inimigos
            random_enemy = choice(self.enemys.sprites())
            random_enemy.increase_fire_rate(self.enemy_shoots, SCREEN_HEIGHT, self.shoot_sound)

    '''def boss_timer(self):
        self.boss_spawn_time -= 1
        if self.boss_spawn_time <= 0:
            self.boss.add(Boss(choice(['right',['left']]),SCREEN_WIDTH))
            self.boss_spawn_time = randint(400,800) #faz com que o timer vai diminuindo para que possa spawnar o boss'''
    
    def boss_timer(self):
        self.boss_spawn_time -= 1
        if self.boss_spawn_time <= 0:
            boss_side = choice(['right', 'left'])
            new_boss = Boss(boss_side, SCREEN_WIDTH, SCREEN_HEIGHT)
            self.boss.add(new_boss)
            self.boss_spawn_time = randint(400, 800)
        else:
            # Faz o boss atirar a cada intervalo específico
            if self.boss and randint(0, 50) == 0:
                self.boss.sprite.shoot(self.enemy_shoots, self.shoot_sound)
    
    def collision(self): #verificacao das colisões
        big_bullet = None       
        # player shoots
        if self.player.sprite.shoots:
            for shoot in self.player.sprite.shoots:
            # enemys collision
                if pygame.sprite.spritecollide(shoot, self.enemys, True):
                    shoot.kill()
                    self.explosion_sound.play()
                    self.enemies_destroyed +=1 #incrementa o contador de enemies
                    if self.enemies_destroyed >= self.total_enemies // 2: #verificacao se for necessario aplicar upgrade
                        self.player.sprite.upgrade_shoot()

            # Verificação de colisão com o Boss
                if pygame.sprite.spritecollide(shoot, self.boss, False):
                    shoot.kill()
                    boss = self.boss.sprite
                    big_bullet = boss.take_damage()
                    if big_bullet:
                        self.enemy_shoots.add(big_bullet)  # Adiciona o tiro grande ao grupo de tiros do inimigo

        # enemy shoots
        if self.enemy_shoots:
            for shoot in self.enemy_shoots:
                if pygame.sprite.spritecollide(shoot, self.player, False):
                    shoot.kill()
                    self.lives -= 1
                if self.lives <= 0:
                    pygame.quit()
                    sys.exit()

        # enemys collide with player
        if self.enemys:
            if pygame.sprite.spritecollide(self.player.sprite, self.enemys, False):
                pygame.quit()
                sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1): #mostra 2vidas, 1vida, 0vida, porem com 0 ainda tamo vivo ate tomar um shoot
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            tela.blit(self.live_surf, (x,8))
    
    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}',False, 'Black') #superficie para onde o score vai aparecer na tela / utilizando anti-alising para bordas ja que vai ser font pixeled
        score_rect = score_surf.get_rect(topleft = (10,-10)) #rect para se localizar na tela o score
        tela.blit(score_surf,score_rect)
        
    def victory_message(self):
        if not self.enemys.sprites() and not self.boss.sprites():
            victory_surf = self.font.render('Voce Ganhou', False, 'White')
            victory_rect = victory_surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            tela.blit(victory_surf,victory_rect)

    def run(self): # atualizar e desenhar sprites na janela
        self.player.update()
        self.enemys.update(self.enemy_direction) #enemy_direction seta a velocidade que eles se movem
        self.enemy_setup_check()
        self.enemy_shoots.update()
        self.boss_timer()
        self.boss.update()
        self.collision()
        self.display_lives()
        self.display_score()
        self.victory_message()

        self.player.sprite.shoots.draw(tela) #shoots do player tem que estar fora da isntancia dos shoots do enemys
        self.player.draw(tela) # desenhando o player na tela
        
        self.enemys.draw(tela)
        self.enemy_shoots.draw(tela)
        self.boss.draw(tela)

if __name__ == '__main__': #boa prática
    pygame.init()

    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600


    tela = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    #objeto clock
    clock = pygame.time.Clock()
    jogo = Game() #logica vai estar na classe run

    ENEMYSHOOT = pygame.USEREVENT + 1
    pygame.time.set_timer(ENEMYSHOOT,800) #timer de quando o enemy vai atirar

    pygame.display.set_caption('War')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ENEMYSHOOT:
                jogo.enemy_shoot()
        tela.fill((204, 179, 110))
        jogo.run()

        pygame.display.flip()
        clock.tick(60)# limitador de fps


'''import pygame
import sys
from random import choice, randint
from player import Player
from enemy import Enemy, Boss
from shoot import Shoot

class Game:
    def __init__(self):
        # Player setup
        player_sprite = Player((SCREEN_HEIGHT / 2, SCREEN_WIDTH), SCREEN_WIDTH, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Sistema de vidas
        self.lives = 3
        self.live_surf = pygame.image.load('/home/otavio/OO/Projeto PyGame/graphics/player.png').convert_alpha()
        self.live_x_start_pos = SCREEN_WIDTH - (self.live_surf.get_size()[0] * 2 + 20)

        # Enemy setup
        self.enemys = pygame.sprite.Group()
        self.enemy_shoots = pygame.sprite.Group()
        
        self.enemy_setup(rows=6, cols=8)
        self.enemy_direction = 1

        # Boss setup
        self.boss = pygame.sprite.GroupSingle()
        self.boss_spawn_time = randint(400, 800)

    def enemy_setup(self, rows, cols, distance_x=60, distance_y=48, offset_x=70, offset_y=100):
        for row_index in range(rows):
            for col_index in range(cols):
                x = col_index * distance_x + offset_x
                y = row_index * distance_y + offset_y
                
                if row_index == 0:
                    enemy_sprite = Enemy('inimigo1', x, y)
                elif 1 <= row_index <= 2:
                    enemy_sprite = Enemy('inimigo2', x, y)
                else:
                    enemy_sprite = Enemy('inimigo3', x, y)
                
                self.enemys.add(enemy_sprite)

    def enemy_setup_check(self):
        all_enemys = self.enemys.sprites()
        for enemy in all_enemys:
            if enemy.rect.right >= SCREEN_WIDTH:  # Acessa `rect` diretamente
                self.enemy_direction = -1
                self.enemy_move_down(2)
            elif enemy.rect.left <= 0:
                self.enemy_direction = 1
                self.enemy_move_down(2)

    def enemy_move_down(self, distance):
        for enemy in self.enemys.sprites():
            enemy.rect.y += distance

    def enemy_shoot(self):
        if self.enemys.sprites():
            random_enemy = choice(self.enemys.sprites())
            shoot_sprite = Shoot(random_enemy.rect.center, 6, SCREEN_HEIGHT)
            self.enemy_shoots.add(shoot_sprite)

    def boss_timer(self):
        self.boss_spawn_time -= 1
        if self.boss_spawn_time <= 0:
            self.boss.add(Boss(choice(['right', 'left']), SCREEN_WIDTH))
            self.boss_spawn_time = randint(400, 800)

    def collision(self):
        # Player shoots
        if self.player.sprite.shoots:
            for shoot in self.player.sprite.shoots:
                if pygame.sprite.spritecollide(shoot, self.enemys, True):
                    shoot.kill()
                if pygame.sprite.spritecollide(shoot, self.boss, True):
                    shoot.kill()

        # Enemy shoots
        if self.enemy_shoots:
            for shoot in self.enemy_shoots:
                if pygame.sprite.spritecollide(shoot, self.player, False):
                    shoot.kill()
                    self.lives -= 1
                if self.lives <= 0:
                    pygame.quit()
                    sys.exit()

        # Enemys collide with player
        if self.enemys:
            if pygame.sprite.spritecollide(self.player.sprite, self.enemys, False):
                pygame.quit()
                sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            tela.blit(self.live_surf, (x, 8))
    
    def victory_message(self):
        if not self.enemys.sprites():
            victory_surf = self.font.render('Você Ganhou', False, 'White')
            victory_rect = victory_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            tela.blit(victory_surf, victory_rect)

    def run(self):
        self.player.update()
        self.enemys.update(self.enemy_direction)
        self.enemy_setup_check()
        self.enemy_shoots.update()
        self.boss_timer()
        self.boss.update()
        self.collision()
        self.display_lives()
        self.victory_message()

        self.player.sprite.shoots.draw(tela)
        self.player.draw(tela)
        self.enemys.draw(tela)
        self.enemy_shoots.draw(tela)
        self.boss.draw(tela)

if __name__ == '__main__':
    pygame.init()

    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600

    tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    jogo = Game()

    ENEMYSHOOT = pygame.USEREVENT + 1
    pygame.time.set_timer(ENEMYSHOOT, 800)

    pygame.display.set_caption('War')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ENEMYSHOOT:
                jogo.enemy_shoot()
        
        tela.fill((204, 179, 110))
        jogo.run()

        pygame.display.flip()
        clock.tick(60)
'''
'''import pygame
from shoot import Shoot

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed): 
        super().__init__()
        self.__image = pygame.image.load('/home/otavio/OO/Projeto PyGame/graphics/player.png').convert_alpha()
        self.__rect = self.__image.get_rect(midbottom=pos)
        self.__speed = speed
        self.__max_x_constraint = constraint
        self.__ready = True
        self.__shoot_time = 0
        self.__shoot_cooldown = 600

        self.__shoots = pygame.sprite.Group()

    # Getters e Setters
    def get_image(self):
        return self.__image

    def get_rect(self):
        return self.__rect

    def get_speed(self):
        return self.__speed

    def set_speed(self, speed):
        self.__speed = speed

    def get_shoots(self):
        return self.__shoots

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d or pygame.K_RIGHT]:
            self.__rect.x += self.__speed
        elif keys[pygame.K_a or pygame.K_LEFT]:
            self.__rect.x -= self.__speed

        if keys[pygame.K_SPACE] and self.__ready:
            self.shoot()
            self.__ready = False
            self.__shoot_time = pygame.time.get_ticks()

    def recarregar(self):
        if not self.__ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.__shoot_time >= self.__shoot_cooldown:
                self.__ready = True

    def constraint(self):
        if self.__rect.left <= 0:
            self.__rect.left = 0
        if self.__rect.right >= self.__max_x_constraint:
            self.__rect.right = self.__max_x_constraint

    def shoot(self):
        self.__shoots.add(Shoot(self.__rect.center, -8, self.__rect.bottom))

    def update(self):
        self.get_input()
        self.constraint()
        self.recarregar()
        self.__shoots.update()
'''