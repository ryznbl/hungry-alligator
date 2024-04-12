from tkinter import *
import random
from PIL import Image

game_over_check = False
score = 0 #number of chickens eaten
lives = 3 #chicken hitting left wall decreases this
CHICKEN_RATE = 5000 #chicken spawn rate
CHICKEN_SPEED = 1000 #chicken move speed
BACKGROUND_COLOR = "#000000"

class Alligator:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.image = PhotoImage(file="alligator.png")
        self.id = canvas.create_image(x, y, anchor=NW, image = self.image)
        self.canvas.bind("<Motion>", self.follow_cursor)
    def follow_cursor(self, event):
        x_cursor, y_cursor = event.x - alligator_width, event.y - (alligator_height/2)
        self.canvas.coords(self.id, x_cursor, y_cursor)
class Chicken:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.image = PhotoImage(file="chicken.png")
        self.id = canvas.create_image(x, y, anchor=NW, image = self.image)
        self.canvas.tag_bind(self.id, "<Enter>", self.delete_chicken)
    def move(self):
        self.canvas.move(self.id, -chicken_width, 0)
    def delete_chicken(self, event):
        global score
        score += 1
        canvas.delete(self.id)
        chickens.remove(self)
        update_labels()
class Chef:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.image = PhotoImage(file="chef.png")
        self.id = canvas.create_image(x, y, anchor=NW, image = self.image)

def create_chicken():
    global chickens
    if not game_over_check:
        x = GAME_WIDTH - chef_width - chicken_width
        y = random.randint((GAME_HEIGHT/2)-(chef_height/2), (GAME_HEIGHT/2)-(chef_height/2)+chef_height)
        chicken = Chicken(canvas, x, y)
        chickens.append(chicken)
        window.after(CHICKEN_RATE, create_chicken)
def move_chickens():
    global first_move
    global lives
    if not first_move:
        chickens_copy = list(chickens)
        for chicken in chickens_copy:
            chicken.move()
            if check_left_wall(chicken):
                lives -= 1
                update_labels()
                canvas.delete(chicken.id)
                chickens.remove(chicken)
                if lives == 0:
                    game_over()
                    return
    else:
        first_move = False
    window.after(CHICKEN_SPEED, move_chickens)
def check_left_wall(chicken):
    x_chicken = canvas.coords(chicken.id)[0]
    if x_chicken <= 0:
        return True
    else:
        return False
    
def game_over():
    global game_over_check
    game_over_check = True
    canvas.delete("all")
    canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2, text = "Game Over :(", font = ('consolas', 40), fill = "red")
    canvas.after(4000, lambda: window.destroy())
    


def update_labels(): # run whenever player eats chicken or chickens reach left wall
    global CHICKEN_RATE
    global CHICKEN_SPEED
    if CHICKEN_RATE > 300:
        CHICKEN_RATE = int(CHICKEN_RATE * (7/10))
    if CHICKEN_SPEED > 100:
        CHICKEN_SPEED = CHICKEN_SPEED - 50
    canvas.itemconfig(score_label, text="Score:{}".format(score))
    score_width = canvas.bbox(score_label)[2] - canvas.bbox(score_label)[0]
    canvas.coords(lives_label, 20 + score_width + 20, 20)
    canvas.itemconfig(lives_label, text="Lives:{}".format(lives))
    
images_info = [(Image.open(filepath).size) for filepath in ["chef.png", "chicken.png", "alligator.png"]]
chef_width, chef_height, chicken_width, chicken_height, alligator_width, alligator_height = [info for info in sum(images_info, ())]
#as short as i could make it, takes information from images

window = Tk()
GAME_WIDTH = ((window.winfo_screenwidth()*(3/4))/50)*50 #keep with increment of 50 so spawning chickens looks nicer
GAME_HEIGHT = window.winfo_screenheight()*(3/4)
window.title("Eat the rotisserie")
window.resizable(False, False)

canvas = Canvas(window, bg=BACKGROUND_COLOR, height = GAME_HEIGHT, width = GAME_WIDTH, highlightthickness = 0) #highlightthickness gets rid of weird border
canvas.grid(row=1, column=0, columnspan=2)
score_label = canvas.create_text(20, 20, anchor=NW, text="Score:{}".format(score), font=('consolas', 20), fill="white")
lives_label = canvas.create_text(150, 20, anchor=NW, text="Lives:{}".format(lives), font=('consolas', 20), fill="white")

window.update()

window_width, window_height = window.winfo_width(), window.winfo_height() #centers the window
window.geometry(f"{window_width}x{window_height}+{(window.winfo_screenwidth()//2 - window_width//2)}+{(window.winfo_screenheight()//2 - window_height//2 - 48)}")

window.config(cursor = "none") #you are the alligator

alligator = Alligator(canvas, 0, int((GAME_HEIGHT/2) - (alligator_height/2)))
chef = Chef(canvas, GAME_WIDTH - chef_width, int((GAME_HEIGHT/2) - (chef_height/2))) #creates chef on the farthest right possible
chickens = []  # array of chickens 
first_move = True # first move so that the first chicken doesnt move instantly
create_chicken() #chef is cooking
move_chickens() #rolling chickens

window.mainloop()
