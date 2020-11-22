import pygame
from pygame.locals import *

from OpenGL.GL import *
import numpy

from obj import *

def main():
        pygame.init()
        cw = 800
        ch = 600
        display = (cw,ch)
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

        print (glGetString(GL_VERSION))

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0, 0, cw, ch)
        glFrustum(-1, 1, -1, 1, 1, 1000)

        angle = 0

        color = (255,128,60)
        plano = glGenLists(1)
        glNewList(plano, GL_COMPILE)
        glBegin(GL_TRIANGLES)
        glColor3ubv(color)
        glVertex3f(-1, 1, 0)
        glVertex3f( 1, 1, 0)
        glVertex3f(1, -1, 0)


        glColor3ub(255,0,255)
        glVertex3f(-1, -1, 0)
        glVertex3f( 1, -1, 0)
        glVertex3f(-1, 1, 0)
        glEnd()
        glEndList()

        model = Obj("knight")
        path = "./knight_stand_0.obj"
        model.parse(path)

        verts = [-0.500000, -0.500000, -0.500000,
                  0.500000, -0.500000, -0.500000,
                  0.500000, -0.500000,  0.500000,
                 -0.500000, -0.500000,  0.500000,
                 -0.500000,  0.500000,  0.500000,
                  0.500000,  0.500000,  0.500000,
                  0.500000,  0.500000, -0.500000,
                 -0.500000,  0.500000, -0.500000]

        verts = numpy.array(verts)

        indexs = [2, 6, 5,
                  6, 2, 1,
                  0, 4, 7,
                  4, 0, 3,
                  0, 6, 1,
                  6, 0, 7,
                  4, 2, 5,
                  2, 4, 3,
                  6, 4, 5,
                  4, 6, 7,
                  0, 2, 3,
                  2, 0, 1 ]

        colors = [255,0,0,
                  0,255,0,
                  0,0,255,
                  255,255,0,
                  0,255,255,
                  255,0,255,
                  128,255,0,
                  0,128,255]

        colors = numpy.array(colors)

        wire = False
        zBuffer = False
        bfc = False
        bfcCW = False

        while True:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                        pygame.quit()
                                        quit()
                                elif event.key == pygame.K_m:
                                        if not wire:
                                                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                                        else:
                                                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                                        wire = not wire
                                elif event.key == pygame.K_z:
                                        zBuffer = not zBuffer
                                        if(zBuffer):
                                                glEnable(GL_DEPTH_TEST)
                                        else:
                                                glDisable(GL_DEPTH_TEST)
                                elif event.key == pygame.K_b:
                                        bfc = not bfc
                                        if(bfc):
                                                glEnable(GL_CULL_FACE)
                                        else:
                                                glDisable(GL_CULL_FACE)
                                elif event.key == pygame.K_c:
                                        bfcCW = not bfcCW
                                        if(bfcCW):
                                                glFrontFace(GL_CW)
                                        else:
                                                glFrontFace(GL_CCW)

                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()

                #glTranslatef(10,0,0)
                glRotatef(angle, 0,1,0)
                glRotatef(angle, 1,0,0)
                glRotatef(angle, 0,0,1)
                #glScalef(0.5,0.5,0.5)

                angle += 1

                glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

                glEnableClientState(GL_VERTEX_ARRAY)
                glVertexPointer(3, GL_FLOAT, 0, model.v)

                #glEnableClientState(GL_COLOR_ARRAY)
                #glColorPointer(3, GL_UNSIGNED_BYTE, 0, colors)

                #glDrawArrays(GL_TRIANGLES, 0, 6)
                #glDrawArrays(GL_TRIANGLES, 0, 634)
                glDrawElements(GL_TRIANGLES, 633, GL_UNSIGNED_INT, model.faces)

                glDisableClientState(GL_VERTEX_ARRAY)
                glDisableClientState(GL_COLOR_ARRAY)

                pygame.display.flip()

main()