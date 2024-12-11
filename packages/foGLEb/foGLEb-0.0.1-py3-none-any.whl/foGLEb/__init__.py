import pygame

class Object:
    def __init__(self, display:pygame.display, initialX:float, initialY:float, hitBoxWidth:int, hitBoxHeight:int, image:str):

        # initial stuff
        self.screen = display
        self.drawImage = True
        self.drawHitBox = False

        # else
        self.rectangle = pygame.Rect(initialX, initialY, hitBoxWidth, hitBoxHeight)
        self.image = pygame.image.load(image)

    def draw(self):

        if self.drawImage:
            self.screen.blit(self.image, (self.rectangle.x, self.rectangle.y))

        if self.drawHitBox:
            pygame.draw.rect(self.screen, (200, 0, 0), self.rectangle)
    
    def collideWith(self, rectangle) -> bool:
        if self.rectangle.colliderect(rectangle):
            return True
        return False
    
    def hide(self):
        self.drawImage = False

    def show(self):
        self.drawImage = True

    def hideHitBox(self):
        self.drawHitBox = False

    def showHitBox(self):
        self.drawHitBox = True

    def liang(self):
        print("he is a guy")