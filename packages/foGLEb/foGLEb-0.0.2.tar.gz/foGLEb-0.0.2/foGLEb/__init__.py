import pygame
import threading

class Object:
    def __init__(self, display:pygame.display, fps:int, initialX:float, initialY:float, hitBoxWidth:int, hitBoxHeight:int, friction:float, image:str):

        # initial stuff
        self.screen = display
        self.drawImage = True
        self.drawHitBox = False
        self.fps = fps
        self.clock = pygame.time.Clock()

        self.friction = friction
        self.speedX = 0
        self.speedY = 0

        # thread
        self.thread = threading.Thread(target=self._changePos)
        self.thread.start()

        # else
        self.rectangle = pygame.Rect(initialX, initialY, hitBoxWidth, hitBoxHeight)
        self.image = pygame.image.load(image)

    # background thread that changes position via speed
    def _changePos(self):
        
        self.rectangle.x += self.speedX
        self.rectangle.y += self.speedY

        self.clock.tick(self.fps)

    def draw(self):

        if self.drawImage:
            self.screen.blit(self.image, (self.rectangle.x, self.rectangle.y))

        if self.drawHitBox:
            pygame.draw.rect(self.screen, (200, 0, 0), self.rectangle)
    
    def collideWith(self, rectangle:pygame.Rect) -> bool:
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

    def setPosition(self, x, y):
        self.rectangle.x = x
        self.rectangle.y = y