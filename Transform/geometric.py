import Transform.interpolation
from .interpolation import interpolation
import math
import cv2
import numpy as np


class Geometric:
    def __init__(self):
        pass

    def matrix_m(self, a, b, theta):
        transformation_matrix = np.array([[math.cos(theta), -math.sin(theta)],
                                          [math.sin(theta), math.cos(theta)]])
        result_a = (a * transformation_matrix[0][0]) + (b * transformation_matrix[0][1])
        result_b = (a * transformation_matrix[1][0]) + (b * transformation_matrix[1][1])

        return result_a, result_b

    def matrix_shift(self, a, b, theta):
        transformation_matrix = np.array([[math.cos(theta), math.sin(theta)],
                                          [-math.sin(theta), math.cos(theta)]])
        result_a = (a * transformation_matrix[0][0]) + (b * transformation_matrix[0][1])
        result_b = (a * transformation_matrix[1][0]) + (b * transformation_matrix[1][1])

        return result_a, result_b

    def forward_rotate(self, image, theta):
        """Computes the forward rotated image by an angle theta
                image: input image
                theta: angle to rotate the image by (in radians)
                return the rotated image"""

        corners = {"tl": np.array([0, 0]),
                   "tr": np.array([0, image.shape[1]]),
                   "bl": np.array([image.shape[0], 0]),
                   "br": np.array([image.shape[0], image.shape[1]])}

        newcorners = {"tl": np.array([0, 0]),
                      "tr": np.array([0, image.shape[1]]),
                      "bl": np.array([image.shape[0], 0]),
                      "br": np.array([image.shape[0], image.shape[1]])}
        numcol, numrow, mincol, maxcol, minrow, maxrow= 0, 0, 0, 0, 0, 0

        for i in corners:
            my_x = corners[i][0]
            my_y = corners[i][1]
            real_x, real_y = self.matrix_m(my_x, my_y, theta)
            newcorners[i][0] = real_x
            newcorners[i][1] = real_y
            #print(newcorners[i])

        for i in newcorners:
            if newcorners[i][0] < minrow:
                minrow = newcorners[i][0]
            if newcorners[i][0] > maxrow:
                maxrow = newcorners[i][0]
            if newcorners[i][1] < mincol:
                mincol = newcorners[i][1]
            if newcorners[i][1] > maxcol:
                maxcol = newcorners[i][1]

        numrow = maxrow - minrow
        numcol = maxcol - mincol

        box = np.zeros((numrow, numcol), np.uint8)
        newshape = box.shape

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                lastrow, lastcol = self.matrix_m(i, j, theta)

                kat_x = int(lastrow - minrow)
                kat_y = int(lastcol - mincol)
                box[kat_x][kat_y] = image[i][j]

        return box

    def reverse_rotation(self, rotated_image, theta, origin, original_shape):
        """Computes the reverse rotated image by an angle theta
                rotated_image: the rotated image from previous step
                theta: angle to rotate the image by (in radians)
                Origin: origin of the original image with respect to the rotated image
                Original shape: shape of the orginal image
                return the original image"""
        box = np.zeros((original_shape), np.uint8)

        for i in range(rotated_image.shape[0]):
            for j in range(rotated_image.shape[1]):
                x_offset = int(i - origin[0])
                y_offset = int(j - origin[1])
                rows, cols = self.matrix_shift(x_offset, y_offset, theta)
                if rows >= 0 and rows <= 256 and cols >= 0 and cols <= 256:
                    box[int(rows)][int(cols)] = rotated_image[i][j]
        return box

    def rotate(self, image, theta, interpolation_type):
        """Computes the forward rotated image by an angle theta using interpolation
                image: the input image
                theta: angle to rotate the image by (in radians)
                interpolation_type: type of interpolation to use (nearest_neighbor, bilinear)
                return the original image"""

        corners = {"tl": np.array([0, 0]),
                   "tr": np.array([0, image.shape[1]]),
                   "bl": np.array([image.shape[0], 0]),
                   "br": np.array([image.shape[0], image.shape[1]])}

        newcorners = {"tl": np.array([0, 0]),
                      "tr": np.array([0, image.shape[1]]),
                      "bl": np.array([image.shape[0], 0]),
                      "br": np.array([image.shape[0], image.shape[1]])}
        numcol, numrow, mincol, maxcol, minrow, maxrow= 0, 0, 0, 0, 0, 0

        for i in corners:
            my_x = corners[i][0]
            my_y = corners[i][1]
            real_x, real_y = self.matrix_m(my_x, my_y, theta) #computed rot matrix
            newcorners[i][0] = real_x
            newcorners[i][1] = real_y

        for i in newcorners:
            if newcorners[i][0] < minrow:
                minrow = newcorners[i][0]
            if newcorners[i][0] > maxrow:
                maxrow = newcorners[i][0]
            if newcorners[i][1] < mincol:
                mincol = newcorners[i][1]
            if newcorners[i][1] > maxcol:
                maxcol = newcorners[i][1]


        numrow = maxrow - minrow
        numcol = maxcol - mincol
        myorigin = (-minrow, -mincol)
        box = np.zeros((numrow, numcol), np.uint8)


        for i in range(box.shape[0]):
            for j in range(box.shape[1]):
                x_offset = i - myorigin[0]
                y_offset = j - myorigin[1]
                rows, cols = self.matrix_shift(x_offset, y_offset, theta)
                #print(rows, cols)
                if interpolation_type == "nearest_neighbor":
                    if rows >= 0 and rows < 255 and cols >= 0 and cols < 255:
                        box[i][j] = image[round(rows)][round(cols)]

                elif interpolation_type == "bilinear":

                    if rows >= 0 and rows < 255 and cols >= 0 and cols < 255:
                        foundp = (rows, cols)

                        tl = (math.floor(rows), math.floor(cols))  # floor floor
                        tr = (math.floor(rows), math.ceil(cols))  # floor ceil

                        bl = (math.ceil(rows), math.floor(cols))  # ceil floor
                        br = (math.ceil(rows), math.ceil(cols))  # ceil ceil
                        box[i][j] = interpolation().bilinear_interpolation(image, foundp, tl, tr, bl, br)
        return box


