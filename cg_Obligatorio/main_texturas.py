import numpy
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from obj import *

def Ground(ground_vertices):
    
    glBegin(GL_QUADS)

    x = 0
    for vertex in ground_vertices:
        x+=1
        glColor3fv((0,1,1))
        glVertex3fv(vertex)
        
    glEnd()

def loadTexture(path):
    surf = pygame.image.load(path)
    image = pygame.image.tostring(surf, 'RGBA', 0)
    ix, iy = surf.get_rect().size
    texid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texid)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)

    glBindTexture(GL_TEXTURE_2D, 0)
    return texid

def main():
    pygame.init()
    display = (1200,1200)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    #Creo un programa de shading y guardo la referencia en la variable gouraud
#    gouraud = createShader("./shaders/gouraud_vs.hlsl", "./shaders/gouraud_fs.hlsl")
    
    modelAnimation = []

    rangeAn = 40

    for i in range(rangeAn):
        modelAn = Obj("model ani #" + str(i))
        path = "./knight_animado/knight_stand_"+str(i)+".obj"
        print(path)
        modelAn.parse(path)
        modelAnimation.append(modelAn)

    smallIndex = 0
    index = 0

    #Activo el manejo de texturas
    glEnable(GL_TEXTURE_2D)
    #Activo la textura 0 (hay 8 disponibles)
    glActiveTexture(GL_TEXTURE0)
    #Llamo a la funcion que levanta la textura a memoria de video
    text = loadTexture("./knight_good.png")

    #Para el shader, me guardo una referencia a la variable que representa a la textura
#    unifTextura = glGetUniformLocation(gouraud, 'textura')

    glShadeModel(GL_SMOOTH)

#    glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, [1,0,0,1])
#    glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT, [1,0,0,1])
#    glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, [1,1,1,1])
#    glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, 16)

    glEnable(GL_LIGHT0)

    glLight(GL_LIGHT0, GL_DIFFUSE, [1,1,1,1])
    glLight(GL_LIGHT0, GL_AMBIENT, [0.1,0.1,0.1,1])
    glLight(GL_LIGHT0, GL_POSITION, [0,0,0,1])
    glLight(GL_LIGHT0, GL_SPECULAR, [1,1,1,1])

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glViewport(0,0,display[0],display[1])
    glFrustum(-1,1,-1,1,1,1000)

    glRotatef(270, 0, 1, 0)
    glRotatef(0, 0, 0, 1)
    glRotatef(270, 1, 0, 0)

    ground_surfaces = (0,1,2,3)

    ground_vertices = (
        (-250,-250,-25),
        (250,-250,-25),
        (-250,250,-25),
        (250,250,-25),
    )

    ang = 0.0
    mode = GL_FILL
    zBuffer = True
    bfc = False
    bfcCW = True
#    light = False
    end = False
    
    movingX = False
    movingY = False
    movingZ = False
    rotatingZ = False
    rotatingY = False

    x = -50
    y = 0
    rz = 0
    ry = 0

    tx = 0
    ty = 0
    tz = 0
    az = 0
    ay = 0

    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_m:
                    if mode == GL_LINE:
                        mode = GL_FILL
                    else:
                        mode = GL_LINE
                    glPolygonMode( GL_FRONT_AND_BACK, mode)
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
                elif event.key == pygame.K_ESCAPE:
                    end = True
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
                    tx =  1
                if event.key == pygame.K_s:
                    movingX = True
                    tx = -1
                if event.key == pygame.K_d:
                    movingY = True
                    ty =  1
                if event.key == pygame.K_a:
                    movingY = True
                    ty = -1
                if event.key == pygame.K_UP:
                    rotatingY = True
                    ay =  1
                if event.key == pygame.K_DOWN:
                    rotatingY = True
                    ay = -1
                if event.key == pygame.K_RIGHT:
                    rotatingZ = True
                    az =  1
                if event.key == pygame.K_LEFT:
                    rotatingZ = True
                    az = -1

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(x,y,0)
        glRotatef(rz, 0, 0, 1)
        glRotatef(ry, 0, 1, 0)

        if movingX:
            x = x + tx * .6
            glTranslatef(tx * .6,0,0)
        if movingY:
            y = y + ty * .6
            glTranslatef(0,ty * .6,0)
        if rotatingZ:
            rz = rz + az * 2
            glRotatef(az * 2, 0, 0, 1)
        if rotatingY:
            ry = ry + ay * 2
            glRotatef(ay * 2, 0, 1, 0)

        glPushMatrix()
        glRotatef(ang, 0,0,1)
        glTranslatef(0,30,0)
        glDisable(GL_LIGHTING)
        glBegin(GL_POINTS)
        glVertex3fv([5,0,0])
        glEnd()
        glEnable(GL_LIGHTING)
        glLightfv(GL_LIGHT1, GL_POSITION, [0,0,0,1])
        glPopMatrix()

        ang += 5

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        smallIndex += 1
        if(smallIndex >= 2):
            index += 1
            smallIndex = 0

        if(index >= rangeAn):
            index = 0

        index = 4
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, ground_vertices)
        glDrawElements(GL_TRIANGLE_STRIP, 4, GL_UNSIGNED_INT, ground_surfaces)
        glDisableClientState(GL_VERTEX_ARRAY)


        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)

        glVertexPointer(3, GL_FLOAT, 0, modelAnimation[index].drawV)
        glNormalPointer(GL_FLOAT, 0, modelAnimation[index].drawN)
        glTexCoordPointer(2, GL_FLOAT, 0, modelAnimation[index].drawT)

        glBindTexture(GL_TEXTURE_2D, text)

        glDrawArrays(GL_TRIANGLES, 0, len(modelAnimation[index].faces))

        glBindTexture(GL_TEXTURE_2D, 0)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)

        pygame.display.flip()
    
    #Cuando salgo del loop, antes de cerrar el programa libero todos los recursos creados
    glDeleteTextures([text])
    pygame.quit()
    quit()

main()