import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
from obj import * #parser

#Uso esta funcion para compilar de forma individual el codigo de cada componente del shader (vertex y fragment)
#Le paso el path al archivo y el tipo de shader (GL_VERTEX_SHADER o GL_FRAGMENT_SHADER)
def compileProgram(path, type):
    #Leo el codigo fuente desde el archivo
    sourceFile = open(path, "r")
    source = sourceFile.read()
    #Creo un shader vacio en memoria de video, del tipo indicado
    #En la variable shader queda almacenado un indice que nos va a permitir identificar este shader de ahora en mas
    shader = glCreateShader(type)
    #Le adjunto el codigo fuente leido desde el archivo
    glShaderSource(shader, source)
    #Intento compilarlo
    glCompileShader(shader)
    
    #Con la funcion glGelShaderiv puedo obtener el estado del compilador de shaders
    #En este caso le pido el stado de la ultima compilacion ejecutada
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        #Si la compilacion falla, muestro el error y retorno 0 (shader nulo)
        #print path + ': ' + glGetShaderInfoLog(shader)
        #Me aseguro de liberar los recursos que reserve en memoria de vide, ya que no los voy a usar
        glDeleteShader(shader)
        return 0
    else:
        return shader

#Esta funcion me permite crear un programa de shading completo, basado en un vertex y un fragment shader
#Le paso el path a ambos codigos fuentes
def createShader(vSource, fSource):
    #Creo y compilo el vertex shader
    vProgram = compileProgram(vSource, GL_VERTEX_SHADER)
    #Creo y compilo el fragment shader
    fProgram = compileProgram(fSource, GL_FRAGMENT_SHADER)
    #Creo un programa de shading vacio en memoria de video
    shader = glCreateProgram()
    #Le adjunto el codigo objeto del vertex shader compilado
    glAttachShader(shader, vProgram)
    #Le adjunto el codigo objeto del fragment shader compilado
    glAttachShader(shader, fProgram)
    #Intento linkear el programa para generar un ejecutable en memoria de video
    glLinkProgram(shader)
    #Chequeo si la ejecucion del linkeo del programa fue exitosa
    if glGetProgramiv(shader, GL_LINK_STATUS) != GL_TRUE:
        #Si falla, imprimo el mensaje de error y libero los recursos
        #print glGetProgramInfoLog(shader)
        glDeleteProgram(shader)
        return 0
    #Una vez que el programa fue linkeado, haya sido exitoso o no, ya no necesito los shaders
    #individuales compilados, asi que libero sus recursos
    glDeleteShader(vProgram)
    glDeleteShader(fProgram)

    return shader

def main():
    pygame.init()
    display = (900,900)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    #print glGetString(GL_SHADING_LANGUAGE_VERSION)
    model = Obj("static model")
    path = "./knight_stand_0.obj"
    model.parse(path)

"""    modelAnimation = []

    model1 = Obj("static model")
    path = "./knight_animado/knight_stand_0.obj"
    model1.parse(path)
    model2 = Obj("static model")
    path = "./knight_animado/knight_stand_1.obj"
    model2.parse(path)
    model3 = Obj("static model")
    path = "./knight_animado/knight_stand_2.obj"
    model3.parse(path)
    model4 = Obj("static model")
    path = "./knight_animado/knight_stand_3.obj"
    model4.parse(path)
    model5 = Obj("static model")
    path = "./knight_animado/knight_stand_4.obj"
    model5.parse(path)

    modelAnimation.append(model1)
    modelAnimation.append(model2)
    modelAnimation.append(model3)
    modelAnimation.append(model4)
    modelAnimation.append(model5) """


#    for i in range(5):
#        modelAn = Obj("model ani #" + str(i))
#        pathAn = "./knight_animado/knight_stand_"+str(i)+".obj"
#        modelAn.parse(pathAn)
#        modelAnimation.append(modelAn)

    #Creo un programa de shading y guardo la referencia en la variable gouraud
#    gouraud = createShader("./shaders/gouraud_2020_vp.glsl",
#                           "./shaders/gouraud_2020_fp.glsl")

    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [1,1,1,1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.2,0.2,0.2,1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1,1,1,1])
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 128)

    glEnable(GL_LIGHT0)

    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0,0.0,0.0,1])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1,0.1,0.1,1])
    glLightfv(GL_LIGHT0, GL_POSITION, [0,100,-50,1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1,1,1,1])

    glEnable(GL_LIGHT1)

    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.0,0.0,1,1])
    glLightfv(GL_LIGHT1, GL_AMBIENT, [0.0,0.0,0.0,1])
    glLightfv(GL_LIGHT1, GL_POSITION, [0,0,0,1])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [0,0,1,1])

    glEnable(GL_LIGHT2)

    glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.0,1.0,0,1])
    glLightfv(GL_LIGHT2, GL_AMBIENT, [0.0,0.0,0.0,1])
    glLightfv(GL_LIGHT2, GL_POSITION, [0,0,0,1])
    glLightfv(GL_LIGHT2, GL_SPECULAR, [0,1,0,1])

    glMatrixMode(GL_PROJECTION)
    glViewport(0,0,display[0],display[1])
    glFrustum(-1,1,-1,1,1,1000)


    glClearColor(0,0,1,1)

    ang = 0.0
    mode = GL_FILL
    glEnable(GL_DEPTH_TEST)
    zBuffer = True
    bfc = False
    bfcCW = True
    shader = False
    light = False
    end = False
    flat = False
    l0 = True

    glPointSize(10)

    #Pido la shader la ubicación de la variable gloabl (uniform) 'especular'
#    uEspec = glGetUniformLocation(gouraud, 'especular')

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
                if event.key == pygame.K_l:
                    light = not light
                    if(light):
                        #Con la tecla L habilito y deshabilito la luz
                        glEnable(GL_LIGHTING)
                    else:
                        glDisable(GL_LIGHTING)
                if event.key == pygame.K_k:
                    flat = not flat
                    if(flat):
                        #Con la tecla K habilito y deshabilito flat shading
                        glShadeModel(GL_FLAT)
                    else:
                        glShadeModel(GL_SMOOTH)
                if event.key == pygame.K_s:
                    shader = not shader
                    if(shader):
                        #Con la tecla S habilito y deshabilito el shader
                        glUseProgram(gouraud)
                    else:
                        glUseProgram(0)
                if event.key == pygame.K_0:
                    l0 = not l0
                    if(l0):
                        glEnable(GL_LIGHT0)
                    else:
                        glDisable(GL_LIGHT0)

                elif event.key == pygame.K_ESCAPE:
                    end = True
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                    
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0,0.0, -50)
        glRotatef(-90, 1,0,0)
        #Hasta acá corresponde a la matriz modelo del knight
        #hago push matrix para salvar el estado, y luego ingreso las transfromaciones para mover la luz
        glPushMatrix()
        glRotatef(ang, 0,0,1)
        glTranslatef(0,30,0)

        #Dibujo un punto para mostrar donde está la fuente de luz
        glDisable(GL_LIGHTING)
        glBegin(GL_POINTS)
        glVertex3fv([0,0,0])
        glEnd()
        glEnable(GL_LIGHTING)

        #Al setear la posción de la luz, esta se multiplica por el contenido de la matrix MODELVIEW, haciendo que la fuente de luz se mueva
        glLightfv(GL_LIGHT2, GL_POSITION, [0,0,0,1])

        #Vuelvo al estado anterior de la matriz, para dibujar el modelo
        glPopMatrix()
        glRotatef(-ang, 0, 0, 1)

        ang += 0.5

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)

        #glVertexPointer(3, GL_FLOAT, 36, model.drawData)
        #glNormalPointer(GL_FLOAT, 36, model.drawData[3:])
        glVertexPointer(3, GL_FLOAT, 0, model.drawV)
        glNormalPointer(GL_FLOAT, 0, model.drawN)

        #Si el shader está activado, seteo el flag (uniform) que indica si calcular el componente de Phong en la ecuación de Lambert
        if(shader):
            glUniform1ui(uEspec, 1)

        glDrawArrays(GL_TRIANGLES, 0, len(model.faces))
        #glDrawElements(GL_TRIANGLES, 634, GL_UNSIGNED_INT, model.faces)
        #glDrawArrays(GL_TRIANGLES, 0, 366)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)

        pygame.display.flip()
    
    #Cuando salgo del loop, antes de cerrar el programa libero todos los recursos creados
#    glDeleteProgram(gouraud)
    pygame.quit()
    quit()

main()