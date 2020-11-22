import numpy
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from obj import *


def loadTexture(path):
    surf = pygame.image.load(path)
    image = pygame.image.tostring(surf, 'RGBA', 0)
    ix, iy = surf.get_rect().size
    texid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texid)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, ix, iy,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, image)

    glBindTexture(GL_TEXTURE_2D, 0)
    return texid


def main():
    pygame.init()
    display = (1200, 1200)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    modelAnimation = []
    
    animations = []
    animations_title = ["run", "stand", "crouch_stand", "fallback", "jump", "wave", "point"]
    animations_frames = [6,40,19,17,6,11,12]

    for i in range(7):
        animation = []
        for j in range(animations_frames[i]):
            model_animation = Obj("model " + animations_title[i] + " # " + str(j))
            path = "./knight_animado/knight_"+animations_title[i]+"_"+str(j)+".obj"
            model_animation.parse(path)
            animation.append(model_animation)
        animations.append(animation)
        animations.clear

    animation_index = 0

    smallIndex = 0
    index = 0

    glEnable(GL_TEXTURE_2D)
    glActiveTexture(GL_TEXTURE0)
    text = loadTexture("./knight_good.png")
    textB = loadTexture("./knight.png")
    texts = [text, textB]
    text_index = 0

    glShadeModel(GL_SMOOTH)

    glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, [1, 1, 1, 1])
    glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT, [0, 0, 0, 1])
    glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, [1, 1, 1, 1])
    glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, 16)

    glEnable(GL_LIGHT0)

    glLight(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
    glLight(GL_LIGHT0, GL_AMBIENT, [0, 0, 0, 3])
    glLight(GL_LIGHT0, GL_POSITION, [0, 0, 0, 1])
    glLight(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])

    glLight(GL_LIGHT1, GL_DIFFUSE, [1, 1, 1, 1])
    glLight(GL_LIGHT1, GL_AMBIENT, [1, 1, 1, 1])
    glLight(GL_LIGHT1, GL_POSITION, [0, 0, 0, 1])
    glLight(GL_LIGHT1, GL_SPECULAR, [1, 1, 1, 1])

    glEnable ( GL_COLOR_MATERIAL ) ;
    glPointSize(10)

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, display[0], display[1])
    glFrustum(-1, 1, -1, 1, 1, 1000)

    glRotatef(270, 0, 1, 0)
    glRotatef(0, 0, 0, 1)
    glRotatef(270, 1, 0, 0)

    ground_vertices = ((-250, -250, -25), (250, -250, -25),
                       (-250, 250, -25), (250, 250, -25))
    ground_surfaces = (0, 1, 2, 3)
    ground_vt = ((0, 0), (0, 40), (40, 40), (40, 0))
    ground_texture = loadTexture("./ground.jpg")

    ang = 0.0
    mode = GL_FILL
    zBuffer = True
    bfc = False
    bfcCW = True
    end = False
    flat = False
    l0 = True

    x = -50
    y = 0
    rz = 0
    ry = 0
    movingX = movingY = rotatingY = rotatingZ = False
    tx = ty = az = ay = 0

    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    end = True
                if event.key == pygame.K_m:
                    if mode == GL_LINE:
                        mode = GL_FILL
                    else:
                        mode = GL_LINE
                    glPolygonMode(GL_FRONT_AND_BACK, mode)
                if event.key == pygame.K_z:
                    zBuffer = not zBuffer
                    if(zBuffer):
                        glEnable(GL_DEPTH_TEST)
                    else:
                        glDisable(GL_DEPTH_TEST)
                if event.key == pygame.K_b:
                    bfc = not bfc
                    if(bfc):
                        glEnable(GL_CULL_FACE)
                    else:
                        glDisable(GL_CULL_FACE)
                if event.key == pygame.K_c:
                    bfcCW = not bfcCW
                    if(bfcCW):
                        glFrontFace(GL_CW)
                    else:
                        glFrontFace(GL_CCW)
                if event.key == pygame.K_l:
                    l0 = not l0
                    if(l0):
                        glEnable(GL_LIGHT0)
                        glDisable(GL_LIGHT1)
                    else:
                        glDisable(GL_LIGHT0)
                        glEnable(GL_LIGHT1)
                if event.key == pygame.K_f:
                    flat = not flat
                    if(flat):
                        glShadeModel(GL_FLAT)
                    else:
                        glShadeModel(GL_SMOOTH)
                if event.key == pygame.K_t:
                    text_index = (text_index + 1) % 2

                if event.key == pygame.K_w:
                    movingX = False
                if event.key == pygame.K_s:
                    movingX = False
                if event.key == pygame.K_d:
                    movingY = False
                if event.key == pygame.K_a:
                    movingY = False
                if event.key == pygame.K_UP:
                    rotatingY = False
                if event.key == pygame.K_DOWN:
                    rotatingY = False
                if event.key == pygame.K_RIGHT:
                    rotatingZ = False
                if event.key == pygame.K_LEFT:
                    rotatingZ = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    movingX = True
                    tx = 1
                if event.key == pygame.K_s:
                    movingX = True
                    tx = -1
                if event.key == pygame.K_d:
                    movingY = True
                    ty = 1
                if event.key == pygame.K_a:
                    movingY = True
                    ty = -1
                if event.key == pygame.K_UP:
                    rotatingY = True
                    ay = 1
                if event.key == pygame.K_DOWN:
                    rotatingY = True
                    ay = -1
                if event.key == pygame.K_RIGHT:
                    rotatingZ = True
                    az = 1
                if event.key == pygame.K_LEFT:
                    rotatingZ = True
                    az = -1
                if event.key == pygame.K_0:
                    animation_index = 0
                if event.key == pygame.K_1:
                    animation_index = 1
                if event.key == pygame.K_2:
                    animation_index = 2
                if event.key == pygame.K_3:
                    animation_index = 3
                if event.key == pygame.K_4:
                    animation_index = 4
                if event.key == pygame.K_5:
                    animation_index = 5
                if event.key == pygame.K_6:
                    animation_index = 6

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(x, y, 0)
        glRotatef(rz, 0, 0, 1)
        glRotatef(ry, 0, 1, 0)

        if movingX:
            x = x + tx * .6
            glTranslatef(tx * .6, 0, 0)
        if movingY:
            y = y + ty * .6
            glTranslatef(0, ty * .6, 0)
        if rotatingZ:
            rz = rz + az * 2
            glRotatef(az * 2, 0, 0, 1)
        if rotatingY:
            ry = ry + ay * 2
            glRotatef(ay * 2, 0, 1, 0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        smallIndex += 1
        if(smallIndex >= 6):
            index += 1
            smallIndex = 0

        if(index >= animations_frames[animation_index]):
            index = 0

#        index = 4

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)

        glVertexPointer(3, GL_FLOAT, 0, ground_vertices)
        glTexCoordPointer(2, GL_FLOAT, 0, ground_vt)
        glBindTexture(GL_TEXTURE_2D, ground_texture)
        glDrawElements(GL_TRIANGLE_STRIP, 4, GL_UNSIGNED_INT, ground_surfaces)

        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)

        glVertexPointer(3, GL_FLOAT, 0, animations[animation_index][index].drawV)
        glNormalPointer(GL_FLOAT, 0, animations[animation_index][index].drawN)
        glTexCoordPointer(2, GL_FLOAT, 0, animations[animation_index][index].drawT)
        glBindTexture(GL_TEXTURE_2D, texts[text_index])
        glDrawArrays(GL_TRIANGLES, 0, len(animations[animation_index][index].faces))
        glBindTexture(GL_TEXTURE_2D, 0)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)

        glPushMatrix()
        ang += 1.0
        glRotatef(ang, 0,0,1)
        glTranslatef(0,30,0)
        #Dibujo un punto para mostrar donde está la fuente de luz
        glDisable(GL_LIGHTING)
        glBegin(GL_POINTS)
        glVertex3fv([0,30,0])
        glEnd()
        glEnable(GL_LIGHTING)
        #Al setear la posción de la luz, esta se multiplica por el contenido de la matrix MODELVIEW, haciendo que la fuente de luz se mueva
        glLightfv(GL_LIGHT0, GL_POSITION, [0,0,0,1])
        #Vuelvo al estado anterior de la matriz, para dibujar el modelo
        glPopMatrix()

        pygame.display.flip()

    glDeleteTextures([texts[text_index]])
    pygame.quit()
    quit()

main()
