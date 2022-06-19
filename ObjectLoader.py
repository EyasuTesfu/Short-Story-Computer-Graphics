import numpy as np


class ObjLoader:
    buffer = []

    @staticmethod
    def search_data(data_values, coordinates, skip, data_type):
        for d in data_values:
            if d == skip:
                continue
            if data_type == 'float':
                coordinates.append(float(d))
            elif data_type == 'int':
                coordinates.append(int(d)-1)

    @staticmethod
    def create_sorted_vertex_buffer(indices_data, vertices, textures, normals):
        for i, ind in enumerate(indices_data):
            if i % 3 == 0:
                start = ind * 3
                end = start + 3
                ObjLoader.buffer.extend(vertices[start:end])
            elif i % 3 == 1:
                start = ind * 2
                end = start + 2
                ObjLoader.buffer.extend(textures[start:end])
            elif i % 3 == 2:
                start = ind * 3
                end = start + 3
                ObjLoader.buffer.extend(normals[start:end])

    @staticmethod
    def create_unsorted_vertex_buffer(indices_data, vertices, textures, normals):
        num_verts = len(vertices) // 3

        for i1 in range(num_verts):
            start = i1 * 3
            end = start + 3
            ObjLoader.buffer.extend(vertices[start:end])

            for i2, data in enumerate(indices_data):
                if i2 % 3 == 0 and data == i1:
                    start = indices_data[i2 + 1] * 2
                    end = start + 2
                    ObjLoader.buffer.extend(textures[start:end])

                    start = indices_data[i2 + 2] * 3
                    end = start + 3
                    ObjLoader.buffer.extend(normals[start:end])

                    break

    @staticmethod
    def show_buffer_data(buffer):
        for i in range(len(buffer)//8):
            start = i * 8
            end = start + 8
            print(buffer[start:end])

    @staticmethod
    def load_model(file, sorted=True):
        vert_coords = []
        tex_coords = []
        norm_coords = []

        all_indices = []
        indices = []
        x = 0
        with open(file, 'r') as f:
            line = f.readline()
            # line = line.replace("\n", "")
            while line and x < 8:
                values = line.split()
                # print(values)
                if line.strip():
                    if values[0] == 'v':
                        ObjLoader.search_data(
                            values, vert_coords, 'v', 'float')
                    elif values[0] == 'vt':
                        ObjLoader.search_data(
                            values, tex_coords, 'vt', 'float')
                    elif values[0] == 'vn':
                        ObjLoader.search_data(
                            values, norm_coords, 'vn', 'float')
                    elif values[0] == 'f':
                        for value in values[1:]:
                            val = value.split('/')
                            ObjLoader.search_data(val, all_indices, 'f', 'int')
                            indices.append(int(val[0])-1)

                line = f.readline()

        if sorted:
            ObjLoader.create_sorted_vertex_buffer(
                all_indices, vert_coords, tex_coords, norm_coords)
        else:
            ObjLoader.create_unsorted_vertex_buffer(
                all_indices, vert_coords, tex_coords, norm_coords)

        buffer = ObjLoader.buffer.copy()
        ObjLoader.buffer = []

        return np.array(indices, dtype='uint32'), np.array(buffer, dtype='float32')
