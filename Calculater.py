import sys
from PyQt5.QtWidgets import *

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        ### 각 위젯을 배치할 레이아웃을 미리 만들어 둠
        ### 크게 입력 창과 숫자, 기호 버튼을 main_layout에 배열하려 함
        #layout_operation = QHBoxLayout()
        #layout_clear_equal = QHBoxLayout()
        layout_number_operator = QGridLayout()
        layout_equation_solution = QFormLayout()

        ### 수식 입력과 답 출력을 위한 LineEdit 위젯 생성
        label_equation = QLabel("Equation: ")
        label_solution = QLabel("Solution: ")
        self.equation = QLineEdit("")
        self.solution = QLineEdit("")

        ### layout_equation_solution 레이아웃에 수식, 답 위젯을 추가
        layout_equation_solution.addRow(label_equation, self.equation)
        layout_equation_solution.addRow(label_solution, self.solution)

        ### 사칙연산 버튼 생성
        button_plus = QPushButton("+")
        button_minus = QPushButton("-")
        button_product = QPushButton("x")
        button_division = QPushButton("/")
        button_share = QPushButton("%")
        button_root = QPushButton("x^(1/2)")
        button_square = QPushButton("x^2")
        button_reciprocal = QPushButton("1/x")

        ### 사칙연산 버튼을 클릭했을 때, 각 사칙연산 부호가 수식창에 추가될 수 있도록 시그널 설정
        button_plus.clicked.connect(lambda state, operation = "+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation = "-": self.button_operation_clicked(operation))
        button_product.clicked.connect(lambda state, operation = "*": self.button_operation_clicked(operation))
        button_division.clicked.connect(lambda state, operation = "/": self.button_operation_clicked(operation))
        button_share.clicked.connect(lambda state, operation = "%": self.button_operation_clicked(operation))
        button_root.clicked.connect(lambda state, operation = "%": self.button_operation_clicked(operation))
        button_square.clicked.connect(lambda state, operation = "%": self.button_operation_clicked(operation))
        button_reciprocal.clicked.connect(lambda state, operation = "%": self.button_operation_clicked(operation))

        ### 사칙연산 버튼을 layout_operation 레이아웃에 추가
        layout_number_operator.addWidget(button_plus, 4, 3)
        layout_number_operator.addWidget(button_minus, 3, 3)
        layout_number_operator.addWidget(button_product, 2, 3)
        layout_number_operator.addWidget(button_division, 1, 3)
        layout_number_operator.addWidget(button_share, 0, 0)
        layout_number_operator.addWidget(button_root, 1, 2)
        layout_number_operator.addWidget(button_square, 1, 1)
        layout_number_operator.addWidget(button_reciprocal, 1, 0)


        ### =, C, CE, backspace 버튼 생성
        button_equal = QPushButton("=")
        button_clear1 = QPushButton("C")
        button_clear2 = QPushButton("CE")
        button_backspace = QPushButton("Backspace")

        ### =, C, CE, backspace 버튼 클릭 시 시그널 설정
        button_equal.clicked.connect(self.button_equal_clicked)
        button_clear1.clicked.connect(self.button_clear_clicked)
        button_clear2.clicked.connect(self.button_clear_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)

        ### =, C, CE, backspace 버튼을 layout_clear_equal 레이아웃에 추가
        layout_number_operator.addWidget(button_clear1, 0, 2)
        layout_number_operator.addWidget(button_clear2, 0, 1)
        layout_number_operator.addWidget(button_backspace, 0, 3)
        layout_number_operator.addWidget(button_equal, 5, 3)

        ### 숫자 버튼 생성하고, layout_number 레이아웃에 추가
        ### 각 숫자 버튼을 클릭했을 때, 숫자가 수식창에 입력 될 수 있도록 시그널 설정
        number_button_dict = {}
        x = 4
        for number in range(0, 10):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].clicked.connect(lambda state, num = number:
                                                       self.number_button_clicked(num))
            if number >0:
                x,y = divmod(number-1, 3)
                if (x == 0):
                    x = 4
                elif (x == 1):
                    x = 3
                elif (x == 2):
                    x = 2
                layout_number_operator.addWidget(number_button_dict[number], x, y)
                
            elif number==0:
                layout_number_operator.addWidget(number_button_dict[number], 5, 1)

        ### 소숫점 버튼과 00 버튼을 입력하고 시그널 설정
        button_dot = QPushButton(".")
        button_dot.clicked.connect(lambda state, num = ".": self.number_button_clicked(num))
        layout_number_operator.addWidget(button_dot, 5, 2)

        button_double_zero = QPushButton("00")
        button_double_zero.clicked.connect(lambda state, num = "00": self.number_button_clicked(num))
        layout_number_operator.addWidget(button_double_zero, 5, 0)

        ### 각 레이아웃을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_equation_solution)
        main_layout.addLayout(layout_number_operator)

        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################
    def number_button_clicked(self, num):
        equation = self.equation.text()
        equation += str(num)
        self.equation.setText(equation)

    def button_operation_clicked(self, operation):
        equation = self.equation.text()
        equation += operation
        self.equation.setText(equation)

    def button_equal_clicked(self):
        equation = self.equation.text()
        solution = eval(equation)
        self.solution.setText(str(solution))

    def button_clear_clicked(self):
        self.equation.setText("")
        self.solution.setText("")

    def button_backspace_clicked(self):
        equation = self.equation.text()
        equation = equation[:-1]
        self.equation.setText(equation)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())