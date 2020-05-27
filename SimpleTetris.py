import pygame

if __name__ == "__main__":
    pygame.init()
    
    size = [1280, 720]
    screen = pygame.display.set_mode(size)
    
    pygame.display.set_caption("Simple Tetris")
    
    done = False
    clock = pygame.time.Clock()
    
    TMino = pygame.image.load('./Sprite/TMino.png')
    TMino_shadow = pygame.image.load('./Sprite/TMino_shadow.png')
    TBlock = pygame.image.load('./Sprite/TBlock.png')
    BG = pygame.image.load('./Sprite/Background.png')
    
    while not done:
        
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        screen.blit(BG, (0, 0))
        screen.blit(TMino, (180, 80))
        screen.blit(TMino_shadow, (180, 620))
        for i in range(7):
            screen.blit(TBlock, (450 - i * 30, 650))
        
        pygame.display.flip()
        
    pygame.quit()
                
        