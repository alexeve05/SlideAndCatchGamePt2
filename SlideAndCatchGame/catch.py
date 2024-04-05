# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 12:09:55 2024

@author: axeve

Alexis Evans
cs120
prof harris
Apr 5 2024
Catch Game part 2

"""

import pygame, simpleGE, random

class Bean(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("bean.png")
        self.setSize(20, 20)
        self.minSpeed = 3
        self.maxSpeed = 9
        self.reset()
        
    def reset(self):
        self.y = 10
        self.x = random.randint(0, self.screenWidth)
        self.dy = random.randint(self.minSpeed, self.maxSpeed)
        
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()
            
class cup(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("cup.png")
        self.setSize(50, 50)
        self.position = (320, 400)
        self.moveSpeed = 6
        
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed
            
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (100, 30)
        
class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time left: 15"
        self.center = (500, 30)
        
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.background.fill((18, 22, 41))
        self.setImage("cafe.png")
        
        self.sndBean = simpleGE.Sound("pop.ogg")
        self.numBean = 15
        self.score = 0
        self.lblScore = LblScore()
        
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 15
        self.lblTime = LblTime()
        
        self.cup = cup(self)
        
        self.bean = []
        for i in range(self.numBean):
            self.bean.append(Bean(self))
            
        self.sprites = [self.cup,
                        self.bean,
                        self.lblScore,
                        self.lblTime]
        
    def process(self):
        for bean in self.bean:
            if bean.collidesWith(self.cup):
                bean.reset()
                self.score += 1
                self.lblScore.text = f"Score: {self.score}"
                
            self.lblTime.text = f"Time left: {self.timer.getTimeLeft():.2f}"
            if self.timer.getTimeLeft() < 0:
                print(f"Score: {self.score}")
                self.stop()
                
class Instructions(simpleGE.Scene):
    def __init__(self, prevScore):
        super().__init__()
        self.prevScore = prevScore
        self.setImage("cafe.png")
        self.response = "Quit"
        
        self.directions = simpleGE.MultiLabel()
        self.directions.textLines = [
        "You are making a cup of coffee",
        "Move with left and right arrow keys.",
        "Catch as many coffee beans as you can,",
        "in the time provided",
        "",
        "Good luck!"]
        
        self.directions.center = (320, 200)
        self.directions.size = (500, 250)
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play"
        self.btnPlay.center = (100, 400)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (540, 400)
        
        self.lblScore = simpleGE.Label()
        self.lblScore.text = "Last score: 0"
        self.lblScore.center = (320, 400)
        
        self.lblScore.text = f"Last score: {self.prevScore}"
        
        self.sprites = [self.directions,
                        self.btnPlay,
                        self.btnQuit,
                        self.lblScore]
    def process(self):
        if self.btnPlay.clicked:
            self.response = "Play"
            self.stop()
            
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()
            
def main():
    keepGoing = True
    lastScore = 0
    while keepGoing:
        instructions = Instructions(lastScore)
        instructions.start()
        if instructions.response == "Play":
            game = Game()
            game.start()
            lastScore = game.score
        else:
            keepGoing = False
if __name__ == "__main__":
    main()
    