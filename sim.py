import pygame
import random

class Clapper:
    def __init__(self, position, cooldown, volume, suggestibility):
        self.pos = position
        self.cd = cooldown
        self.nat_cd = cooldown
        self.vol = volume
        self.timer = cooldown
        self.is_clapping = False
        self.suggestibility = suggestibility
        self.got_modified = False
        
    def update(self, dt):
        self.timer -= dt
        
        self.is_clapping = False
        self.got_modified = False
        
        if self.timer < 0:
            self.timer = self.cd
            self.clap()
        #print("update " + str(dt))
        #print(self.pos)
    
    def clap(self):
        self.is_clapping = True
        
    def conform(self):
        self.cd = self.cd - self.timer
        self.got_modified = True
        
            
class Audience:
    def __init__(self, rows, seats, size):
        self.size = size
        self.members = [Clapper((r * size, s * size), random.uniform(1000/4, 1000/1), random.uniform(0, 255), random.uniform(0.60, 0.90)) for s in range(seats) for r in range (rows)]
        
        pygame.init()
        self.font = pygame.font.SysFont("monospace", 15)

        self.screen = pygame.display.set_mode([400, 300])
        self.clock = pygame.time.Clock()
 
        self.is_running = True
        self.vol_log = [0]
        
        print(sum([c.cd for c in self.members])/len(self.members))

        
    def update(self):
        vol = 0
        for c in self.members:
            c.update(10)
            vol += c.is_clapping * c.vol
            
        for c in self.members:
            if vol * random.uniform(0, c.suggestibility) > 600:
                #c.clap()
                c.conform()
        if len(self.vol_log) > 150:
            self.vol_log.pop(0)
        self.vol_log.append(vol)
        
        
            
    def draw(self):
        self.screen.fill((0,0,0))
        for c in self.members:
            dim = pygame.Rect((c.pos[0] + 10, c.pos[1] + 10), (self.size, self.size))
            if c.is_clapping:
                pygame.draw.rect(self.screen, (c.vol, 0, 64), dim)
            else:
                if c.got_modified:
                    pygame.draw.rect(self.screen, (0, c.suggestibility * 255, 64), dim)
                else:
                    pygame.draw.rect(self.screen, (0, 0, 64), dim)
            pygame.display.flip()
            
        #draw plot of "resulting volume"
            lines = [(i * 2 + 50, 290 - 0.01 * self.vol_log[i]) for i in range(len(self.vol_log))]
            pygame.draw.lines(self.screen, (0, 0, 255), False, lines, 1)
            
        # render text
            l_cur = self.font.render(str(int(self.vol_log[-1])), 1, (255,255,0))
            l_max = self.font.render(str(int(max(self.vol_log))), 1, (255,255,0))
            self.screen.blit(l_cur, (0, 280))
            self.screen.blit(l_max, (360, 280))
            
    def run(self):
        while(self.is_running):
            self.clock.tick(10)
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self.is_running = False
            
            self.update()
            self.draw()
        
        pygame.quit()
            
            
        
aud = Audience(12, 8, 30)
aud.run()
