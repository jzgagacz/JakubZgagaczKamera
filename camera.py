import pygame
import numpy as np
import math

pygame.init()
winw = 1600
winh = 900
window = pygame.display.set_mode((winw, winh))
pygame.display.set_caption("Wirtualna Kamera")
clock=pygame.time.Clock()

run = True

boxcolor = (0,200,255)
d=700
deltad=0.1
angle = math.radians(0.08)
movement = 0.4
def perspectiveMatrix(d):
    return np.array(           [[1,0,0,0],
                                [0,1,0,0],
                                [0,0,1,0],
                                [0,0,1/d,0]] )
def rotationMatrixX(angle):
    return np.array(           [[1,0,0,0],
                                [0,math.cos(angle),-1*math.sin(angle),0],
                                [0,math.sin(angle),math.cos(angle),0],
                                [0,0,0,1]] )
def rotationMatrixY(angle):
    return np.array(           [[math.cos(angle),0,math.sin(angle),0],
                                [0,1,0,0],
                                [-1*math.sin(angle),0,math.cos(angle),0],
                                [0,0,0,1]] )
def rotationMatrixZ(angle):
    return np.array(           [[math.cos(angle),-1*math.sin(angle),0,0],
                                [math.sin(angle),math.cos(angle),0,0],
                                [0,0,1,0],
                                [0,0,0,1]] )

def translationMatrix(x,y,z):
    return np.array(           [[1,0,0,x],
                                [0,1,0,y],
                                [0,0,1,z],
                                [0,0,0,1]] )
def makeBox(x,y,z,w,h,d):
    box = []
    point = np.array([x,y,z,1]).T
    box.append(point)
    point = np.array([x+w,y,z,1]).T
    box.append(point)
    point = np.array([x+w,y,z+d,1]).T
    box.append(point)
    point = np.array([x,y,z+d,1]).T
    box.append(point)
    point = np.array([x,y+h,z,1]).T
    box.append(point)
    point = np.array([x+w,y+h,z,1]).T
    box.append(point)
    point = np.array([x+w,y+h,z+d,1]).T
    box.append(point)
    point = np.array([x,y+h,z+d,1]).T
    box.append(point)
    return box

def rotate(box, rotMatrix):
    rotBox = []
    for i in range(0, len(box)):
        point = box[i]
        point=np.matmul(rotMatrix, point)
        rotBox.append(point)
    return rotBox

def translate(box, transMatrix):
    rotBox = []
    for i in range(0, len(box)):
        point = box[i]
        point=np.matmul(transMatrix, point)
        rotBox.append(point)
    print(rotBox, flush=True)
    return rotBox

def drawBox(box):
    perBox = []
    for i in range(0, len(box)):
        point = box[i]
        if point[2] < 0:
            return
        point=np.matmul(perspectiveMatrix(d), point)
        point[0] = (point[0]/point[3])
        point[1] = (point[1]/point[3])
        perBox.append(point)
    for i in range(0, 4):
        pygame.draw.line(window, boxcolor, (perBox[i][0]+winw/2, perBox[i][1]+winh/2), (perBox[(i+1)%4][0]+winw/2, perBox[(i+1)%4][1]+winh/2), 1)
        pygame.draw.line(window, boxcolor, (perBox[i+4][0]+winw/2, perBox[i+4][1]+winh/2), (perBox[(i+1)%4+4][0]+winw/2, perBox[(i+1)%4+4][1]+winh/2), 1)
        pygame.draw.line(window, boxcolor, (perBox[i+4][0]+winw/2, perBox[i+4][1]+winh/2), (perBox[(i+1)%4+4][0]+winw/2, perBox[(i+1)%4+4][1]+winh/2), 1)
        pygame.draw.line(window, boxcolor, (perBox[i][0]+winw/2, perBox[i][1]+winh/2), (perBox[i+4][0]+winw/2, perBox[i+4][1]+winh/2), 1)

sceneObjects = []

box1 = makeBox(-125,50,400,100,100,100)
box2 = makeBox(25,50,400,200,200,100)
box3 = makeBox(-325,50,550,300,100,200)
box4 = makeBox(25,-50,550,100,200,100)
sceneObjects.append(box1)
sceneObjects.append(box2)
sceneObjects.append(box3)
sceneObjects.append(box4)

def rotateScene(rotMatrix):
    for i in range(0, len(sceneObjects)):
        sceneObjects[i] = rotate(sceneObjects[i], rotMatrix)

def translateScene(transMatrix):
    for i in range(0, len(sceneObjects)):
        sceneObjects[i] = rotate(sceneObjects[i], transMatrix)

def drawScene():
    for obj in sceneObjects:
        drawBox(obj)

while True:
    dt = clock.tick(75)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_j]:
        rotateScene(rotationMatrixY(angle*dt))
    if keys_pressed[pygame.K_l]:
        rotateScene(rotationMatrixY(-angle*dt))
    if keys_pressed[pygame.K_i]:
        rotateScene(rotationMatrixX(-angle*dt))
    if keys_pressed[pygame.K_k]:
        rotateScene(rotationMatrixX(angle*dt))
    if keys_pressed[pygame.K_u]:
        rotateScene(rotationMatrixZ(angle*dt))
    if keys_pressed[pygame.K_o]:
        rotateScene(rotationMatrixZ(-angle*dt))
    if keys_pressed[pygame.K_a]:
        translateScene(translationMatrix(movement*dt,0,0))
    if keys_pressed[pygame.K_d]:
        translateScene(translationMatrix(-movement*dt,0,0))
    if keys_pressed[pygame.K_w]:
        translateScene(translationMatrix(0,0,-movement*dt))
    if keys_pressed[pygame.K_s]:
        translateScene(translationMatrix(0,0,movement*dt))
    if keys_pressed[pygame.K_q]:
        translateScene(translationMatrix(0,-movement*dt,0))
    if keys_pressed[pygame.K_e]:
        translateScene(translationMatrix(0,movement*dt,0))
    if keys_pressed[pygame.K_r]:
            d+=deltad*dt
    if keys_pressed[pygame.K_f]:
        d-=deltad*dt
        if (d<1):
            d=1
    window.fill((0,0,0))
    drawScene()
    pygame.display.update()