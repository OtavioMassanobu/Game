import pygame

#from main import SCREEN_HEIGHT
from shoot import Shoot
from random import choice,randint

class Enemy(pygame.sprite.Sprite):
    def __init__(self,type,x,y):
        super().__init__()
        file_path = '/home/otavio/OO/Projeto PyGame/graphics/' + type + '.png' #evito varios ifs
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y)) #enemy basico

        '''#adicionado valores aos inimigos
        if type == 'inimigo1': self.value = 100
        elif type == 'inimigo2': self.value = 200
        else: self.value = 300'''

    def increase_fire_rate(self, shoot_group, screen_height, shoot_sound):
        """Aumenta a quantidade de tiros dos inimigos."""
        for _ in range(randint(1, 3)):  # Inimigos podem atirar de 1 a 3 tiros ao mesmo tempo
            random_enemy = choice(self.groups()[0].sprites())
            shoot_sprite = Shoot(random_enemy.rect.center, 6, screen_height)
            shoot_group.add(shoot_sprite)
            shoot_sound.play()

    def update(self, direction): #metodo que fara com que os enemys se movimentem
        self.rect.x += direction #funcao que atualiza tambem todos enemys

#boss atira normal
'''class Boss(pygame.sprite.Sprite): #enemy mais forte como se fosse um boss
        def __init__(self,side,screen_width):
            super().__init__()
            self.image = pygame.image.load('/home/otavio/OO/Projeto PyGame/graphics/boss.png').convert_alpha()

            if  side == 'rigth': #movimentacao e espaco de manobra
                x = screen_width + 50
                self.speed = -3
            else:
                x = -50
                self.speed = 3

            self.rect = self.image.get_rect(topleft = (x,80))
        
        def shoot(self, shoot_group, screen_height, shoot_sound):
            """Boss atira um tiro em direção ao player."""
            shoot_sprite = Shoot(self.rect.center, 12, screen_height)
            shoot_group.add(shoot_sprite)
            shoot_sound.play()

        def update(self,):
            self.rect.x += self.speed
'''
#boss atira grande e morre
'''class Boss(pygame.sprite.Sprite):
    def __init__(self, side, screen_width, screen_height):
        super().__init__()
        self.image = pygame.image.load('/home/otavio/OO/Projeto PyGame/graphics/boss.png').convert_alpha()
        self.health = 3  # Adicionando vida ao boss

        if side == 'right':  # Movimentação e espaço de manobra
            x = screen_width + 50
            self.speed = -3
        else:
            x = -50
            self.speed = 3

        self.rect = self.image.get_rect(topleft=(x, 80))
        self.screen_height = screen_height

    def update(self):
        self.rect.x += self.speed

    def take_damage(self):
        self.health -= 1
        if self.health == 1:
            return self.shoot_big_bullet()  # Atira um tiro maior
        elif self.health <= 0:
            self.kill()
        return None

    def shoot_big_bullet(self):
        big_bullet = Shoot(self.rect.center, 10, self.screen_height, big_bullet=True)  # Criar Big Bullet
        return big_bullet
'''
class Boss(pygame.sprite.Sprite):
    def __init__(self, side, screen_width, screen_height):
        super().__init__()
        self.image = pygame.image.load('/home/otavio/OO/Projeto PyGame/graphics/boss.png').convert_alpha()
        self.health = 3  # Adicionando vida ao boss

        if side == 'right':  # Movimentação e espaço de manobra
            x = screen_width + 50
            self.speed = -3
        else:
            x = -50
            self.speed = 3

        self.rect = self.image.get_rect(topleft=(x, 80))
        self.screen_height = screen_height

    def update(self):
        self.rect.x += self.speed

    def take_damage(self):
        self.health -= 1
        if self.health == 1:
            return self.shoot_big_bullet()  # Atira um tiro maior
        elif self.health <= 0:
            self.kill()
        return None

    def shoot_big_bullet(self):
        big_bullet = Shoot(self.rect.center, 10, self.screen_height, big_bullet=True)  # Criar Big Bullet
        return big_bullet

    def shoot(self, enemy_shoots, shoot_sound):
        """Método para o boss atirar normalmente"""
        new_shot = Shoot(self.rect.center, 5, self.screen_height)  # Disparar um tiro normal
        enemy_shoots.add(new_shot)

        if shoot_sound:
            shoot_sound.play()
