'''import pygame
from shoot import Shoot
#original 
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed): #construtor
        super().__init__() #inicializar metodo super
        self.image = pygame.image.load('/home/otavio/OO/Projeto PyGame/graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos) #posicao será passada quando iniciar a classe
        self.speed = speed
        self.max_x_constraint = constraint #restricao do personnagem no eixo X
        self.ready = True
        self.shoot_time = 0
        self.shoot_cooldown = 600 #6 milissegundos

        self.shoots = pygame.sprite.Group()
        
        self.shoot_sound = pygame.mixer.Sound('/home/otavio/OO/Projeto PyGame/audio/canon.mp3')
        self.shoot_sound.set_volume(0.5)
    
    def get_input(self): #entrada do player / teclas 
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d or pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_a or pygame.K_LEFT]: 
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.ready: #tiro
            self.shoot() #metodo para tiro
            self.ready = False
            self.shoot_time = pygame.time.get_ticks()#usado somente uma vez
            self.shoot_sound.play()

    def recarregar(self):
        if not self.ready:
            currrent_time = pygame.time.get_ticks()#usado mas vezes/continuo
            if currrent_time - self.shoot_time >= self.shoot_cooldown:
                self.ready = True

    def constraint(self): #metodo para restricao
        if self.rect.left <= 0: #verificacao do lado esquerdo do player para nao restringir a borda
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint
    
    def shoot(self):
        self.shoots.add(Shoot(self.rect.center,-8,self.rect.bottom))
        
    def shoot(self):
        # Adiciona tiros baseado no nível do tiro
        if self.shoot_level == 1:
            self.shoots.add(Shoot(self.rect.center, -8, self.rect.bottom))
        elif self.shoot_level == 2:
            self.shoots.add(Shoot((self.rect.centerx - 20, self.rect.centery), -8, self.rect.bottom))
            self.shoots.add(Shoot((self.rect.centerx + 20, self.rect.centery), -8, self.rect.bottom))

    def upgrade_shoot(self):
        self.shoot_level += 1

    def update(self): #fazer o update   
        self.get_input()
        self.constraint()
        self.recarregar()
        self.shoots.update()

    def check_upgrade(player, enemies_destroyed, total_enemies):
        if enemies_destroyed >= total_enemies // 2:
            player.upgrade_shoot()
'''
import pygame
from shoot import Shoot

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed): #construtor
        super().__init__() #inicializar metodo super
        self.image = pygame.image.load('/home/otavio/OO/Projeto PyGame/graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos) #posição será passada quando iniciar a classe
        self.speed = speed
        self.max_x_constraint = constraint #restrição do personagem no eixo X
        self.ready = True
        self.shoot_time = 0
        self.shoot_cooldown = 600 #600 milissegundos

        self.shoots = pygame.sprite.Group()
        self.shoot_level = 1  # Iniciando com nível 1 do tiro
        
        self.shoot_sound = pygame.mixer.Sound('/home/otavio/OO/Projeto PyGame/audio/canon.mp3')
        self.shoot_sound.set_volume(0.0)
    
    def get_input(self): #entrada do player / teclas 
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]: 
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.ready: #tiro
            self.shoot() #método para tiro
            self.ready = False
            self.shoot_time = pygame.time.get_ticks() #usado somente uma vez
            self.shoot_sound.play()

    def recarregar(self):
        if not self.ready:
            current_time = pygame.time.get_ticks() #usado várias vezes/continuamente
            if current_time - self.shoot_time >= self.shoot_cooldown:
                self.ready = True

    def constraint(self): #método para restrição
        if self.rect.left <= 0: #verificação do lado esquerdo do player para não restringir a borda
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint
    
    def shoot(self):
        # Adiciona tiros baseado no nível do tiro
        if self.shoot_level == 1:
            self.shoots.add(Shoot(self.rect.center, -8, self.rect.bottom))
        elif self.shoot_level == 2:
            self.shoots.add(Shoot((self.rect.centerx - 20, self.rect.centery), -8, self.rect.bottom))
            self.shoots.add(Shoot((self.rect.centerx + 20, self.rect.centery), -8, self.rect.bottom))

    def upgrade_shoot(self):
        if self.shoot_level < 2:  # Supondo que o nível máximo é 2
            self.shoot_level += 1

    def update(self): #fazer o update   
        self.get_input()
        self.constraint()
        self.recarregar()
        self.shoots.update()














'''class Upgrade:
    def __init__(self, player, total_enemies):
        self.player = player
        self.total_enemies = total_enemies
        self.enemies_destroyed = 0

    def enemy_destroyed(self):
        self.enemies_destroyed += 1
        if self.enemies_destroyed >= self.total_enemies // 2:
            self.player.upgrade_shoot()
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