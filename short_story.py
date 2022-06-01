__author__ = "Joshua Tesfaye, Dagim Fikru"
__copyright__ = "Copyright 2022, Short Story-CG project"
__instructor__ = "Absalat Dawit"
__license__ = ""
__version__ = "1.0.0"
__maintainer__ = ""
__email__ = "jt272525@gmail.com"
__status__ = "Production"
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

edges = ((0, 1), (0, 3), (0, 4),
        (2, 1), (2, 3), (2, 7),
        (6, 3), (6, 4),
        (6, 7), (5, 1),
        (5, 4), (5, 7))


vertices = ((1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
            (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1))


def Cube():
    glBegin(GL_TRIANGLE_STRIP)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def Sphere():
    sphere = gluNewQuadric() 
    glMatrixMode(GL_PROJECTION)

    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
    viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    glLoadIdentity()
    gluSphere(sphere, 1.0, 32,26)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    a, b, c = 0, 0, 0
    while True:
        for event in pygame.event.get():
            a += 1
            b += 1
            c += 1
            glColor3f(a + 1, b + 1.5, c)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(a, b, c)
        # Cube()
        Sphere()
        pygame.display.flip()
        a += 1
        b += 1
        c += 1
        # pygame.time.wait(10)


main()
