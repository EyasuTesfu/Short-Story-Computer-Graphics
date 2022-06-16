import pygame as pg
from OpenGL.GL import *
import numpy as np
import _ctypes
import pyrr
from OpenGL.GL.shaders import compileProgram, compileShader


class App:

    def __init__(self) -> None:
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,
                                    pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode((640, 480), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        # initialise opengl
        glClearColor(0.1, 0.2, 0.2, 1)
        self.shader = self.createShader(
            "shaders/vertex.txt", "shaders/fragment.txt")
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)
        glEnable(GL_DEPTH_TEST)

        self.wood_texture = Material("Dog/dog.jpg")
        self.cube_mesh = Object("Dog/dog.obj")

        self.cube = Cube(
            position=[0, 0, -3],
            eulers=[0, 0, 0]
        )

        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=640/480,
            near=0.1, far=10, dtype=np.float32
        )
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, "projection"),
            1, GL_FALSE, projection_transform
        )
        self.modelMatrixLocation = glGetUniformLocation(
            self.shader, "model")
        self.mainLoop()

    def createShader(self, vertexFilepath, fragmentFilepath):

        with open(vertexFilepath, 'r') as f:
            vertex_src = f.readlines()

        with open(fragmentFilepath, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))

        return shader

    def mainLoop(self):
        while(True):
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    return

            # update screen
           # refresh screen
            glClear(GL_COLOR_BUFFER_BIT)

            glUseProgram(self.shader)
            self.wood_texture.use()
            glBindVertexArray(self.triangle.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.triangle.vertex_count)

            pg.display.flip()

            # timing
            self.clock.tick(60)
        self.quit()

    def quit(self):
        pg.quit()


# class Mesh:
#     def __init__(self) -> None:
#         self.verticies = self.loadMesh()
# class Student:
# class Home:
# class School:
# class Mother:
# class Road:
# class Environment:


class Material:

    def __init__(self, filepath):
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        image = pg.image.load(filepath).convert()
        image_width, image_height = image.get_rect().size
        img_data = pg.image.tostring(image, 'RGBA')
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width,
                     image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)

    def use(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def destroy(self):
        glDeleteTextures(1, (self.texture,))


class Object:
    def __init__(self, filename) -> None:
        # x, y, z, s, t, nx, ny, nz
        self.verticies = self.loadObject("Dog/dog.obj")

        self.vertex_count = len(self.verticies) // 8

        self.verticies = np.array(self.verticies, dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.verticies.nbytes,
                     self.verticies, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                              32, ctypes.c_void_p(12))

    def loadObject(self, filepath):
        verticies = []
        # unassembled data of dog
        v = []
        vt = []
        vn = []
        with open(filepath, "r") as f:
            line = f.readline()
            while line:
                firstspace = line.find(" ")
                tag = line[:firstspace]
                if tag == "v":
                    line = line.replace("v  ", "")
                    # print(line)
                    # (x,y,z)
                    line = line.split(" ")
                    #print(line, "next")
                    lst = [float(x) for x in line]
                    v.append(lst)
                elif tag == "vt":
                    line = line.replace("vt ", "")
                    # (s,t)
                    line = line.split(" ")
                    lst = [float(x) for x in line]
                    vt.append(lst)
                elif tag == "vn":
                    line = line.replace("vn ", "")
                    # (nx, ny, nz)
                    line = line.split(" ")
                    lst = [float(x) for x in line]
                    vn.append(lst)
                elif tag == "f":
                    # face, v/vt/vn
                    line = line.replace("f ", "")
                    line = line.replace("\n", "")
                    # (../../.., ../../.., ../../..)
                    line = line.split(" ")
                    for vertex in line:
                        if vertex == '':
                            v

                    faceVerticies = []
                    faceTextures = []
                    faceNormals = []
                    print(line)
                    for vertex in line:
                        # vertex = v/vt/vt
                        l = vertex.split("/")
                        print(l)
                        position = int(l[0])-1
                        faceVerticies.append(v[position])
                        texture = int(l[1])-1
                        faceTextures.append(vt[texture])
                        normal = int(l[2])-1
                        faceNormals.append(vn[normal])
                    # [0,1,2,3] -> [0,1,2,0,2,3]
                    triangles_in_face = len(line)
                    vertex_order = []
                    for i in range(triangles_in_face):
                        vertex_order.append(0)
                        vertex_order.append(i+1)
                        vertex_order.append(i+2)
                    for i in vertex_order:
                        for x in faceVerticies[i]:
                            verticies.append(x)
                        for x in faceTextures[i]:
                            verticies.append(x)
                        for x in faceNormals[i]:
                            verticies.append(x)
                    v.append(lst)
                line = f.readline()

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))


if __name__ == "__main__":
    newapp = App()
