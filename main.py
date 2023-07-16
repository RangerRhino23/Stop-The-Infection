from ursina import *
from ursina.shaders import *
from ursina.prefabs.first_person_controller import FirstPersonController
import assets.APIs.first_person_movement_api as fpm
import random, csv


app = Ursina()
Sky(texture='sky.png')

# Variables
WORLD_SIZE = 50
virus = []
timer = 0
player = FirstPersonController()
ground = Entity(model='plane',scale=(WORLD_SIZE*3),texture='grass',texture_scale=40,collider='box')
wall = Entity(model='cube',scale=(WORLD_SIZE*2,10,1),position=(0,0,WORLD_SIZE),collider='box',visible=False)
wall = Entity(model='cube',scale=(-WORLD_SIZE*2,10,1),position=(0,0,-WORLD_SIZE),collider='box',visible=False)
wall = Entity(model='cube',scale=(1,10,WORLD_SIZE*2),position=(WORLD_SIZE,0,0),collider='box',visible=False)
wall = Entity(model='cube',scale=(1,10,-WORLD_SIZE*2),position=(-WORLD_SIZE,0,0),collider='box',visible=False)
virusBlockText = Text(text=len(virus), scale=2,y=.45)
timerText = Text(text=timer,y=-.43,x=-.85,scale=2)
finishedText = Text(text=f'You finish with a time of {round(timer,2)}!',x=-.35,y=5,scale=2.5)
virusSpawnTimer = 0
leaderboard = False
ambient = Audio('assets/audio/ambient.ogg',autoplay=True,loop=True)

class LeaderBoard():
    def __init__(self):
        self.background = Entity(model='quad',parent=camera.ui,scale=(0.65,0.55),color=color.dark_gray)
        self.LeaderBoard = Text(text='LeaderBoard \n-------------------', position=(-.15,.25),scale=2)
        with open('leaderboard.txt','r') as csvfile:
            file = csv.reader(csvfile)
            new_file = ''
            leaderboardPOS = .15
            leaderboardSpot = 1
            found = False
            for row in file:
                if row != '':
                    if timer <= float(row[0]) and not found:
                        Text(text=f'{leaderboardSpot}. {round(timer,2)} <-- YOU!',y=leaderboardPOS,scale=2,x=-.055)
                        new_file += f'{round(timer,2)}\n'
                        found = True
                        leaderboardPOS -= .05
                        leaderboardSpot += 1
                        Text(text=f'{leaderboardSpot}. {row[0]}',y=leaderboardPOS,scale=2,x=-.055)
                        new_file += f'{row[0]}\n'
                    else:
                        Text(text=f'{leaderboardSpot}. {row[0]}',y=leaderboardPOS,scale=2,x=-.055)
                        new_file += f'{row[0]}\n'
                    leaderboardPOS -= .05
                    leaderboardSpot += 1
            csvfile.close()
        with open('leaderboard.txt', 'w') as csvfile:
            csvfile.write(new_file)
                


class VirusBlock(Button):
    def __init__(self):
        super().__init__(self)
        self.model='cube'
        self.parent = scene
        self.scale=(random.randint(10,50)/10,2,random.randint(10,50)/10)
        self.position=(random.randint(-WORLD_SIZE+1,WORLD_SIZE-1),-.5,random.randint(-WORLD_SIZE+1,WORLD_SIZE-1))
        self.color=color.lime
        self.highlight_color=color.lime
        self.pressed_color=color.lime
        self.collider='box'
        self.shader=lit_with_shadows_shader
        virus.append(self)
    
    def on_click(self):
        if distance(self, player) <= self.scale*1.2:
            Audio('assets/audio/slime.ogg',autoplay=True,loop=False)
            virus.remove(self)
            destroy(self)

def update():
    global timer, virusSpawnTimer, leaderboard
    fpm.player_movement(player, 20)
    virusBlockText.text = len(virus)
    #Runs if there are viruses left
    if len(virus) >= 1:
        virusSpawnTimer += time.dt
        timer += time.dt
        if virusSpawnTimer >= 4:
            VirusBlock()
            virusSpawnTimer = 0
        timerText.text = round(timer,2)
        finishedText.text=f'You finish with a time of {round(timer,2)}!'
    #Runs if there are no viruses left
    if len(virus) <= 0:
        player.position = (0,0,0)
        finishedText.y=.35
        if not leaderboard:
            LeaderBoard()
            leaderboard = True


def input(key):
    if key == 'q' or key == 'esc':
        application.quit()
    if key == 'g':
        VirusBlock()

for i in range(5):
    VirusBlock()

app.run()