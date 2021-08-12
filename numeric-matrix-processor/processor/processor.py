class Matrix:
    def __init__(self, shape, numbers=None):
        self.shape = shape
        if numbers is None:
            self.num = [[0.0 for j in range(self.shape[1])] for i in range(self.shape[0])]
        else:
            self.num = [[numbers[i][j] for j in range(self.shape[1])] for i in range(self.shape[0])]

    def matrix_add(self, matrix):
        return Matrix(self.shape,
                      [[self.num[i][j] + matrix.num[i][j] for j in range(self.shape[1])] for i in range(self.shape[0])])

    def matrix_multiply_const(self, constant):
        return Matrix(self.shape,
                      [[constant * self.num[i][j] for j in range(self.shape[1])] for i in range(self.shape[0])])

    def matrix_multiply(self, matrix):
        multiply_ans = []
        for i in range(self.shape[0]):
            multiply_ans.append([sum([self.num[i][j] * matrix.num[j][k] for j in range(self.shape[1])])
                                 for k in range(matrix.shape[1])])
        return Matrix((self.shape[0], matrix.shape[1]), multiply_ans)

    def matrix_transpose(self, option):
        matrix = None
        if option == "1":
            matrix = Matrix((self.shape[1], self.shape[0]))
            for i in range(0, matrix.shape[0]):
                for j in range(0, matrix.shape[1]):
                    matrix.num[i][j] = self.num[j][i]
        elif option == "2":
            matrix = Matrix((self.shape[1], self.shape[0]))
            for i in range(0, matrix.shape[0]):
                for j in range(0, matrix.shape[1]):
                    matrix.num[i][j] = self.num[self.shape[1] - j - 1][self.shape[0] - i - 1]
        elif option == "3":
            matrix = Matrix(self.shape, [self.num[i][::-1] for i in range(self.shape[0])])
        elif option == "4":
            matrix = Matrix(self.shape, self.num[::-1])
        return matrix

    def determinant(self):
        if self.shape == (1, 1):
            return self.num[0][0]
        else:
            det = 0.0
            for i in range(0, self.shape[0]):
                numbers = [[self.num[j][k] for k in range(1, self.shape[1])] for j in range(self.shape[0]) if j != i]
                det += (-1) ** i * self.num[i][0] \
                       * Matrix((self.shape[0] - 1, self.shape[1] - 1), numbers).determinant()
            return det

    def inverse(self):
        det = self.determinant()
        if det == 0.0:
            return None
        adjugate_numbers = []
        for i in range(self.shape[0]):
            adjugate_row = []
            for j in range(self.shape[1]):
                cofactor_numbers = []
                for k in range(self.shape[0]):
                    if k == i:
                        continue
                    cofactor_row = []
                    for l in range(self.shape[1]):
                        if l != j:
                            cofactor_row.append(self.num[k][l])
                    cofactor_numbers.append(cofactor_row)
                adjugate_row.append((-1) ** (i + j)
                                    * Matrix((self.shape[0] - 1, self.shape[1] - 1), cofactor_numbers).determinant())
            adjugate_numbers.append(adjugate_row)
        adjugate_matrix = Matrix((self.shape[1], self.shape[0]), adjugate_numbers).matrix_transpose("1")
        return adjugate_matrix.matrix_multiply_const(1 / det)

    def print_matrix(self):
        print("The result is: ")
        for i in range(self.shape[0]):
            print(" ".join(str(number) for number in self.num[i]))


def get_matrix(n, m):
    numbers = [[float(x) for x in input().split()] for i in range(n)]
    return Matrix((n, m), numbers)


def binary_core(option):
    n, m = list(map(int, input("Enter size of first matrix: ").split()))
    print("Enter first matrix: ")
    A = get_matrix(n, m)
    n, m = list(map(int, input("Enter size of second matrix: ").split()))
    print("Enter second matrix: ")
    B = get_matrix(n, m)
    if option == "1":
        if A.shape == B.shape:
            A.matrix_add(B).print_matrix()
            return
    elif option == "3":
        if A.shape[1] == B.shape[0]:
            A.matrix_multiply(B).print_matrix()
            return
    print("The operation cannot be performed.")


def unary_core(option):
    transpose_option = None
    if option == "4":
        print("""
1. Main diagonal
2. Side diagonal
3. Vertical line
4. Horizontal line""")
        transpose_option = input("Your choice: ")

    n, m = list(map(int, input("Enter size of matrix: ").split()))
    print("Enter matrix: ")
    A = get_matrix(n, m)
    if option == "2":
        constant = int(input("Enter constant: "))
        A.matrix_multiply_const(constant).print_matrix()
    elif option == "4":
        A.matrix_transpose(transpose_option).print_matrix()
    elif option == "5":
        print("The result is: ")
        print(A.determinant())
    elif option == "6":
        inverse_matrix = A.inverse()
        if inverse_matrix is None:
            print("This matrix doesn't have an inverse.")
        else:
            inverse_matrix.print_matrix()


while True:
    print("""
1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrix
5. Calculate a determinant
6. Inverse matrix
0. Exit""")

    action = input("Your choice: ")
    if action == "1" or action == "3":
        binary_core(action)
    elif action == "2" or action == "4" or action == "5" or action == "6":
        unary_core(action)
    elif action == "0":
        break
