from random import *
from tkinter import *
master = Tk()

w = Canvas(master, width=1000, height=1000)

class GameOfLife:
    map_height = 0
    map_width = 0
    map_population = []
    overpopulation_count = 4
    underpopulation_count = 2
    birth_count = 3
    rects = []


    def __init__(self, width, height):
        self.map_height = height
        self.map_width = width
        self.map_population = []
        #initialize population array with all 0 values
        for i in range(self.map_width):
            self.map_population.append([False] * self.map_height)


    def randomize_population(self, probability_life=0.05):
        individuals_alive = round(self.map_height * self.map_width * probability_life)
        print("initializing", individuals_alive, "alive individuals")
        for i in range(individuals_alive):
            #use randint from random package to select
            # random places for population
            x = randint(0, self.map_width-1)
            y = randint(0, self.map_height-1)
            self.map_population[x][y] = True

    def is_alive(self, x, y):
        return self.map_population[x][y]

    def get_alive_count(self, x, y):
        alive = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if (i < 0 or j < 0 or i >= self.map_width or j >= self.map_height or (x == i and y == j)):
                    continue
                if (self.is_alive(i, j)):
                    # there is someone alive here!
                    alive = alive + 1

        return alive

    def evolve(self):
        for i in range(self.map_width):
            for j in range(self.map_height):
                alive = self.get_alive_count(i, j)
                if alive >= self.overpopulation_count:
                    self.map_population[i][j] = False
                elif alive >= self.birth_count:
                    self.map_population[i][j] = True
                elif alive < self.underpopulation_count:
                    self.map_population[i][j] = False

    def draw(self, w):

        for rect in self.rects:
            w.delete(rect)

        width = 1000 / self.map_width
        height = 1000 / self.map_height
        for i in range(self.map_width):
            for j in range(self.map_height):
                color = "black"
                if self.map_population[i][j]:
                    color = "green"
                self.rects.append(w.create_rectangle(i*width, j*height, (i+1)*width, (j+1)*height, fill=color))

gol = GameOfLife(100, 100)

gol.randomize_population()

gol.draw(w)

w.pack()

generating = False

def generation():
    global w, master
    gol.evolve()
    gol.draw(w)
    master.update()

def update(event=None):
    global w, master, generating
    if (event != None):
        generating = not generating
        print("generating:", generating)
    if generating:
        generation()
        master.after(25, update)

master.bind( "<space>", update)
master.mainloop()
