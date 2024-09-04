import pygame

#shoot normal
'''class Shoot(pygame.sprite.Sprite):
    def __init__(self,pos,speed,screen_height):
        super().__init__()
        self.image = pygame.Surface((4,10))
        self.image.fill('black')
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.height_y_constraint = screen_height

    def destroy(self): #destrruir os shoots quando sair da tela
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self): #movimenta o objeto retangulo shoot pra cima no eixo y em uma certa velocidade
        self.rect.y += self.speed
        self.destroy()
'''
#shoot buffado
class Shoot(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height, big_bullet=False):
        super().__init__()
        if big_bullet:
            self.image = pygame.Surface((20, 40))  # Tamanho maior para o tiro grande
            self.image.fill('red')  # Cor diferente para o tiro grande
            self.speed = speed * 2  # Velocidade maior para o tiro grande
        else:
            self.image = pygame.Surface((4, 10))
            self.image.fill('black')
            self.speed = speed
        self.rect = self.image.get_rect(center=pos)
        self.height_y_constraint = screen_height

    def destroy(self):  # Destruir o tiro quando sair da tela
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):  # Movimenta o tiro no eixo y
        self.rect.y += self.speed
        self.destroy()

