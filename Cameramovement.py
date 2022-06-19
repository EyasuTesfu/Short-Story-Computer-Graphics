'''
Joshua Tesfaye UGR/0359/12 Section 2
Dagim Fikru UGR/4328/12 Section 2
Short Story
date of submission: Sunday, June 19, 2022
'''

from camera import Camera
from ObjectLoader import ObjLoader
from TextureLoader import load_texture_pygame
import pyrr
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL import *
import pygame
import os
import time
from playsound import playsound
os.environ['SDL_VIDEO_WINDOW_POS'] = '400,200'


class Story:
    def mouse_look(self, xpos, ypos):
        global first_mouse, lastX, lastY

        if self.first_mouse:
            lastX = xpos
            lastY = ypos
            self.first_mouse = False

        xoffset = xpos - lastX
        yoffset = lastY - ypos

        lastX = xpos
        lastY = ypos

        self.cam.process_mouse_movement(xoffset, yoffset)

    def __init__(self) -> None:

        vertexPath = "shaders/vertex.txt"
        fragmentPath = "shaders/fragment.txt"

        with open(vertexPath, 'r') as f:
            vertex_src = f.readlines()

        with open(fragmentPath, 'r') as f:
            fragment_src = f.readlines()

        # CAMERA settings
        self.cam = Camera()
        self.WIDTH, self.HEIGHT = 1280, 720
        lastX, lastY = self.WIDTH / 2, self.HEIGHT / 2
        self.first_mouse = True
        pygame.init()
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.OPENGL |
                                              pygame.DOUBLEBUF | pygame.RESIZABLE)  # |pygame.FULLSCREEN
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        # load here the 3d meshes

        self.building_indicies, self.building_buffer = ObjLoader.load_model(
            "meshes/building.obj", False)
        self.woman_indicies, self.woman_buffer = ObjLoader.load_model(
            "meshes/3dwoman.obj")
        self.man_indicies, self.man_buffer = ObjLoader.load_model(
            "meshes/3dman.obj")
        self.floor_indicies, self.floor_buffer = ObjLoader.load_model(
            "meshes/floor.obj")

        shader = compileProgram(compileShader(
            vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

        # self.VAO and self.VBO
        self.VAO = glGenVertexArrays(4)
        self.VBO = glGenBuffers(4)
        self.EBO = glGenBuffers(1)

        # building self.VAO
        glBindVertexArray(self.VAO[0])
        # building Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[0])
        glBufferData(GL_ARRAY_BUFFER, self.building_buffer.nbytes,
                     self.building_buffer, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.building_indicies.nbytes,
                     self.building_indicies, GL_STATIC_DRAW)

        # building vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                              self.building_buffer.itemsize * 8, ctypes.c_void_p(0))
        # building textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                              self.building_buffer.itemsize * 8, ctypes.c_void_p(12))
        # building normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                              self.building_buffer.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        # woman self.VAO
        glBindVertexArray(self.VAO[1])
        # woman Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[1])
        glBufferData(GL_ARRAY_BUFFER, self.woman_buffer.nbytes,
                     self.woman_buffer, GL_STATIC_DRAW)

        # woman vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                              self.woman_buffer.itemsize * 8, ctypes.c_void_p(0))
        # woman textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                              self.woman_buffer.itemsize * 8, ctypes.c_void_p(12))
        # woman normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                              self.woman_buffer.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        # man self.VAO
        glBindVertexArray(self.VAO[2])
        # man Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[2])
        glBufferData(GL_ARRAY_BUFFER, self.man_buffer.nbytes,
                     self.man_buffer, GL_STATIC_DRAW)

        # man vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                              self.man_buffer.itemsize * 8, ctypes.c_void_p(0))
        # man textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                              self.man_buffer.itemsize * 8, ctypes.c_void_p(12))
        # man normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                              self.man_buffer.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        # floor self.VAO
        glBindVertexArray(self.VAO[3])
        # floor Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[3])
        glBufferData(GL_ARRAY_BUFFER, self.floor_buffer.nbytes,
                     self.floor_buffer, GL_STATIC_DRAW)

        # floor vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                              self.floor_buffer.itemsize * 8, ctypes.c_void_p(0))
        # floor textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                              self.floor_buffer.itemsize * 8, ctypes.c_void_p(12))
        # floor normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                              self.floor_buffer.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        self.textures = glGenTextures(4)
        load_texture_pygame("textures/brick.jpg", self.textures[0])
        load_texture_pygame(
            "textures/womantexture.jpg", self.textures[1])
        load_texture_pygame("textures/dennis.jpg", self.textures[2])
        load_texture_pygame("meshes/floor.jpg", self.textures[3])

        glUseProgram(shader)
        glClearColor(0, 0.1, 0.1, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        projection = pyrr.matrix44.create_perspective_projection_matrix(
            45, 1280 / 720, 0.1, 100)
        self.building_position = pyrr.matrix44.create_from_translation(
            pyrr.Vector3([10, 15, -20]))
        self.woman_position = pyrr.matrix44.create_from_translation(
            pyrr.Vector3([-4, 1, 16]))
        self.man_position = pyrr.matrix44.create_from_translation(
            pyrr.Vector3([8, 1, 15]))
        self.floor_position = pyrr.matrix44.create_from_translation(
            pyrr.Vector3([0, 0, 0]))

        self.model_location = glGetUniformLocation(shader, "model")
        self.project_location = glGetUniformLocation(shader, "projection")
        self.view_location = glGetUniformLocation(shader, "view")

        glUniformMatrix4fv(self.project_location, 1, GL_FALSE, projection)
        font = pygame.font.SysFont("None", 30)
        self.text1 = font.render("Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia, molestiae quas vel sint commodi repudiandae consequuntur voluptatum laborumnumquam blanditiis harum quisquam eius sed odit fugiat iusto fuga praesentium optio, eaque rerum! Provident similique accusantium nemo autem. Veritatis obcaecati tenetur iure eius earum ut molestias architecto voluptate aliquam  nihil, eveniet aliquid culpa officia aut! Impedit sit sunt quaerat, odit,", True, (255, 255, 255))
        self.runonce = True

    def main(self):
        # font = pygame.font.SysFont("Times New Roman, Arial", 30)
        # text = font.render("Abebe beso bela",True)
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

                if event.type == pygame.VIDEORESIZE:
                    glViewport(0, 0, event.w, event.h)
                    projection = pyrr.matrix44.create_perspective_projection_matrix(
                        45, event.w / event.h, 0.1, 100)
                    glUniformMatrix4fv(self.project_location,
                                       1, GL_FALSE, projection)

            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_a]:
                self.cam.process_keyboard("LEFT", 0.08)
            if keys_pressed[pygame.K_d]:
                self.cam.process_keyboard("RIGHT", 0.08)
            if keys_pressed[pygame.K_w]:
                self.cam.process_keyboard("FORWARD", 0.08)
            if keys_pressed[pygame.K_s]:
                self.cam.process_keyboard("BACKWARD", 0.08)

            mouse_position = pygame.mouse.get_pos()
            self.mouse_look(mouse_position[0], mouse_position[1])

            # to been able to look around 360 degrees, still not perfect
            if mouse_position[0] <= 0:
                pygame.mouse.set_pos((1279, mouse_position[1]))
            elif mouse_position[0] >= 1279:
                pygame.mouse.set_pos((0, mouse_position[1]))

            ct = pygame.time.get_ticks() / 1000

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            view = self.cam.get_view_matrix()
            glUniformMatrix4fv(self.view_location, 1, GL_FALSE, view)

            self.window.fill(0)
            # text = font.render('Angle: %d°' % angle, True, (255, 255, 255))
            # w, h = self.text1.get_size()
            # self.window.blit(
            #     self.text1, (self.WIDTH//2 - w//2, self.HEIGHT//2 - h//2))
            # rot_y = pyrr.Matrix44.from_y_rotation(0.8 * ct)
            # model = pyrr.matrix44.multiply(rot_y, building_pos)

            # # writing the text
            # self.window.blit(self.text1, pyrr.matrix44.create_from_translation(
            #     pyrr.Vector3([0, 20, 0])))
            # draw the building
            glBindVertexArray(self.VAO[0])
            glBindTexture(GL_TEXTURE_2D, self.textures[0])
            glUniformMatrix4fv(self.model_location, 1,
                               GL_FALSE, self.building_position)
            glDrawElements(GL_TRIANGLES, len(
                self.building_indicies), GL_UNSIGNED_INT, None)

            # draw the woman
            glBindVertexArray(self.VAO[1])
            glBindTexture(GL_TEXTURE_2D, self.textures[1])
            glUniformMatrix4fv(self.model_location, 1,
                               GL_FALSE, self.woman_position)
            glDrawArrays(GL_TRIANGLES, 0, len(self.woman_indicies))

            # draw the man
            glBindVertexArray(self.VAO[2])
            glBindTexture(GL_TEXTURE_2D, self.textures[2])
            glUniformMatrix4fv(self.model_location, 1,
                               GL_FALSE, self.man_position)
            glDrawArrays(GL_TRIANGLES, 0, len(self.man_indicies))

            # draw the floor
            glBindVertexArray(self.VAO[3])
            glBindTexture(GL_TEXTURE_2D, self.textures[3])
            glUniformMatrix4fv(self.model_location, 1,
                               GL_FALSE, self.floor_position)
            glDrawArrays(GL_TRIANGLES, 0, len(self.floor_indicies))

            pygame.display.flip()
            while(self.runonce == True):
                playsound('audio/1.mp3')
                playsound('audio/2.mp3')
                playsound('audio/3.mp3')
                playsound('audio/4.mp3')
                playsound('audio/5.mp3')
                playsound('audio/6.mp3')
                self.runonce = False

        pygame.quit()


ourStory = Story()
ourStory.main()
