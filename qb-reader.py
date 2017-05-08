"""
Script for reading and writing .qb files
"""

import numpy as np
import struct

class QbMatrix(object):

    def __init__(self, name, data, pos):
        self.name = name
        self.pos = pos
        self.data = data

class Qb(object):

    def __init__(self):
        self.version = 0x0101
        self.colorFormat = 0
        self.zAxisOrientation = 0
        self.compressed = 0
        self.visibilityMaskEncoded = 0
        self.matrixList = []

    def load(self, file):
        self.version = struct.unpack("I", file.read(4))[0]
        self.colorFormat = struct.unpack("I", file.read(4))[0]
        self.zAxisOrientation = struct.unpack("I", file.read(4))[0]
        self.compressed = struct.unpack("I", file.read(4))[0]
        self.visibilityMaskEncoded = struct.unpack("I", file.read(4))[0]
        numMatrices = struct.unpack("I", file.read(4))[0]
        self.matrixList = []

        for i in range(numMatrices):
            self.matrixList.append(self.loadMatrix(file))

    def loadMatrix(self, file):
        nameLength = struct.unpack("B", file.read(1))[0]
        name = struct.unpack(str(nameLength)+"s", file.read(nameLength))[0]
    
        size = struct.unpack("III", file.read(12))
        
        pos = struct.unpack("iii", file.read(12))
        
        matrix = np.ndarray(shape=size)
     
        if self.compressed == 0:
            sizeLength = size[0]*size[1]*size[2]
            matrix = np.ndarray(shape=size, dtype=int, buffer=file.read(sizeLength * 4))
        else:
            CODEFLAG = 2
            NEXTSLICEFLAG = 6

            z = 0
            while (z < size[2]):
                z += 1
                index = 0
       
                while True:
                    data = struct.unpack("I", file.read(4))[0]
                    
                    if data == NEXTSLICEFLAG:
                        break
                    elif data == CODEFLAG:
                        count = struct.unpack("I", file.read(4))[0]
                        data = struct.unpack("I", file.read(4))[0]
                   
                        for j in range(count): 
                            x = index % size[0] + 1
                            y = index // size[0] + 1
                            index += 1
                            matrix[x + y*size[0] + z*size[0]*size[1]] = data
                    else: 
                        x = index % sizex + 1
                        y = index // sizex + 1
                        index += 1
                        matrix[x + y*size[0] + z*size[0]*size[1]] = data

        return QbMatrix(name, matrix, pos)

    def save(self, file):
        self.compressed = 0 #Compression saving not supported

        file.write(struct.pack("I", self.version))
        file.write(struct.pack("I", self.colorFormat))
        file.write(struct.pack("I", self.zAxisOrientation))
        file.write(struct.pack("I", self.compressed))
        file.write(struct.pack("I", self.visibilityMaskEncoded))
        file.write(struct.pack("I", len(self.matrixList)))

        for matrix in self.matrixList:
            self.saveMatrix(file, matrix)

    def saveMatrix(self, file, matrix):
        file.write(struct.pack("B", len(matrix.name)))
        file.write(struct.pack(str(len(matrix.name.encode('ascii')))+"s", matrix.name.encode('ascii')))
        file.write(struct.pack("III", matrix.data.shape[0], matrix.data.shape[1], matrix.data.shape[2]))
        file.write(struct.pack("iii", matrix.pos[0], matrix.pos[1], matrix.pos[2]))
        for z in range(matrix.data.shape[2]):
            for y in range(matrix.data.shape[1]):
                for x in range(matrix.data.shape[0]):
                    file.write(struct.pack("I", matrix.data[x, y, z]))