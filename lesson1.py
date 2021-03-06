import pygame
import sys
import math

pygame.init()

def rotate2d(pos, rad):
    x,y = pos
    s,c = math.sin(rad), math.cos(rad)
    return x*c-y*s, y*c+x*s

class Cam:
    def __init__(self,  pos = (0,0,0), rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot)

    def events(self, event):
        if event.type == pygame.MOUSEMOTION:
            x,y = event.rel
            x/= 200
            y/=200
            self.rot[0] += y
            self.rot[1] += x


    def update(self,dt, key):
        s = dt * 10

        if key[pygame.K_q]: self.pos[1] += s
        if key[pygame.K_e]: self.pos[1] -= s

        x,y = s * math.sin(self.rot[1]), s * math.cos(self.rot[1])

        if key[pygame.K_w]: self.pos[0] += x; self.pos[2] += y;
        if key[pygame.K_s]: self.pos[0] -= x; self.pos[2] -= y;
        if key[pygame.K_a]: self.pos[0] -= y; self.pos[2] += x;
        if key[pygame.K_d]: self.pos[0] += y; self.pos[2] -= x;



w,h = 400,400
cx,cy = w//2, h//2

screen = pygame.display.set_mode((w,h))

clock = pygame.time.Clock()

verts = (-1,-1,-1), (1,-1,-1), (1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)
edges = (0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4), (0,4), (1,5), (2,6), (3,7)
faces = (0,1,2,3), (4,5,6,7), (0,1,5,4), (2,3,7,6),(0,3,7,4), (1,2,6,5)
colours = (255,0,0), (255,128,0), (255,255,0), (255,255,255), (0,0,255), (0,128,0)

cam = Cam((0,0,-5))

pygame.event.get()
pygame.mouse.get_rel()
pygame.mouse.set_visible(0)
pygame.event.set_grab(1)


while True:
    dt = clock.tick()/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  pygame.quit();  sys.exit()
        cam.events(event)

    screen.fill((0,0,0))

    vert_list = []
    screen_coords = []

    for x,y,z in verts:
        x -= cam.pos[0]
        y -= cam.pos[1]
        z -= cam.pos[2]

        x,z = rotate2d((x,z), cam.rot[1])
        y,z = rotate2d((y,z), cam.rot[0])

        vert_list += [(x,y,z)]

        f = 200 / z
        x, y = x * f, y * f
        screen_coords += [(cx+int(x), cy+int(y))]


    face_list = []
    face_colour = []
    depth = []

    for f in range(len(faces)):
        face = faces[f]

        on_screen = False
        for i in face:
            if vert_list[i][2] > 0:
                on_screen = True
                break

        if on_screen == True:
            coords = [screen_coords[i] for i in face]
            face_list += [coords]
            face_colour += [colours[f]]
            depth += [sum(sum(vert_list[j][i] for j in face) **2 for i in range(3))]

    order = sorted(range(len(face_list)), key=lambda i:depth[i], reverse=1)

    for i in order:
        pygame.draw.polygon(screen, face_colour[i], face_list[i])

    pygame.display.flip()

    key = pygame.key.get_pressed()
    cam.update(dt, key)

