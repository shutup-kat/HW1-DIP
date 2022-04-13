class interpolation:

    def linear_interpolation(self, image, p0, p1, p2, y3, i1, i2):
        """Computes the linear interpolation value at some iD location x between two 1D points (Pt1 and Pt2).
        
        There are no arguments defined in the function definition on purpose. It is left up to the student to define any requierd arguments.
        Please change the signature of the function and add the arguments based on your implementation.
        
        The function ideally takes two 1D points Pt1 and Pt2, and their intensitites I(Pt1), I(Pt2).
        return the interpolated intensity value (I(x)) at location x """

        # Write your code for linear interpolation here
       # print(p0, p1, p2)
        if not y3:
            myint = (image[p1[0]][p1[1]] * ((p2[0] - p0[0]) / (p2[0] - p1[0]) ) ) + (image[p2[0]][p2[1]] * (p0[0] - p1[0]) / (p2[0] - p1[0]) )
        else:
            myint = (i1 * ((p2[1] - p0[1]) / (p2[1] - p1[1]) ) ) + (i2 * (p0[1] - p1[1]) / (p2[1] - p1[1]) )
        return myint

    def bilinear_interpolation(self, image, p0, p1, p2, p3, p4):

        """Computes the bi linear interpolation value at some 2D location x between four 2D points (Pt1, Pt2, Pt3, and Pt4).
        
        There are no arguments defined in the function definition on purpose. It is left upto the student to define any requierd arguments.
        Please change the signature of the function and add the arguments based on your implementation.
        
        The function ideally takes four 2D points Pt1, Pt2, Pt3, and Pt4, and their intensitites I(Pt1), I(Pt2), I(Pt3), and I(Pt4).
        return the interpolated intensity value (I(x)) at location x """

        # Write your code for bilinear interpolation here
        # Recall that bilinear interpolation performs linear interpolation three times
        # Please reuse or call linear interpolation method three times by passing the appropriate parameters to compute this task
        # intensity = image[p1][p2]
       # print(p0, p1, p2)
        flag = False
        i1, i2 = 0, 0
        i1 = self.linear_interpolation(image, p0, p1, p3, flag, i1, i2) #intensity one
        i2 = self.linear_interpolation(image, p0, p2, p4, flag, i1, i2) #intensity two
        flag = True
        point1 = (p0[0], p1[1])
        point2 = (p0[0], p2[1])
        final = self.linear_interpolation(image, p0, point1, point2, flag, i1, i2)

        return final

