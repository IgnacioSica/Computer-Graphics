import pygame
import numpy
from OpenGL.GL import *
from pygame.locals import *
from obj import *

def main():
    pygame.init()
    cw = 800
    ch = 600
    display = (cw,ch)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    print (glGetString(GL_VERSION))

    model = Obj("knight")
    path = "./knight_stand_0.obj"
    model.parse(path)

    print(model.faces)

main()