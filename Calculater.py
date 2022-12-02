import sys
from PyQt5.QtWidgets import *

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        #각 위젯을 배치할 레이아웃을 미리 만들어 둠
        #크게 입력 창과 숫자, 기호 버튼을 main_layout에 배열하려 함
        layout_number_operator = QGridLayout()
        layout_equation_solution = QFormLayout()

        #수식 입력과 답 출력을 위한 LineEdit 위젯을 하나의 창으로 생성
        #값을 저장하기 위한 LineEdit 위젯 생성 -> equation_memory
        self.equation = QLineEdit("")
        self.equation_memory = QLineEdit("")

        #layout_equation_solution 레이아웃에 수식, 답 위젯을 추가
        layout_equation_solution.addRow(self.equation)

        #사칙연산 버튼 생성
        button_plus = QPushButton("+")
        button_minus = QPushButton("-")
        button_product = QPushButton("x")
        button_division = QPushButton("/")
        button_share = QPushButton("%")
        button_root = QPushButton("x^(1/2)")
        button_square = QPushButton("x^2")
        button_reciprocal = QPushButton("1/x")

        #사칙연산 버튼을 클릭했을 때, 각 사칙연산 부호가 수식창에 추가될 수 있도록 시그널 설정
        button_plus.clicked.connect(lambda state, operation = "+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation = "-": self.button_operation_clicked(operation))
        button_product.clicked.connect(lambda state, operation = "*": self.button_operation_clicked(operation))
        button_division.clicked.connect(lambda state, operation = "/": self.button_operation_clicked(operation))
        button_share.clicked.connect(lambda state, operation = "%": self.button_operation_clicked(operation))
        button_root.clicked.connect(lambda state, operation = "root": self.button_operation_clicked(operation))
        button_square.clicked.connect(lambda state, operation = "^2": self.button_operation_clicked(operation))
        button_reciprocal.clicked.connect(lambda state, operation = "1/x": self.button_operation_clicked(operation))

        #사칙연산 버튼을 layout_operation 레이아웃에 추가
        layout_number_operator.addWidget(button_plus, 4, 3)
        layout_number_operator.addWidget(button_minus, 3, 3)
        layout_number_operator.addWidget(button_product, 2, 3)
        layout_number_operator.addWidget(button_division, 1, 3)
        layout_number_operator.addWidget(button_share, 0, 0)
        layout_number_operator.addWidget(button_root, 1, 2)
        layout_number_operator.addWidget(button_square, 1, 1)
        layout_number_operator.addWidget(button_reciprocal, 1, 0)


        #'=', 'C', 'CE', 'Backspace' 버튼 생성
        button_equal = QPushButton("=")
        button_clear1 = QPushButton("C")
        button_clear2 = QPushButton("CE")
        button_backspace = QPushButton("Backspace")

        #'=', 'C', 'CE', 'Backspace' 버튼 클릭 시 시그널 설정
        button_equal.clicked.connect(self.button_equal_clicked)
        button_clear1.clicked.connect(self.button_clear_clicked)
        button_clear2.clicked.connect(self.button_clear_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)

        #'=', 'C', 'CE', 'Backspace' 버튼을 layout_number_operator 레이아웃에 추가
        layout_number_operator.addWidget(button_clear1, 0, 2)
        layout_number_operator.addWidget(button_clear2, 0, 1)
        layout_number_operator.addWidget(button_backspace, 0, 3)
        layout_number_operator.addWidget(button_equal, 5, 3)

        #숫자 버튼 생성하고, layout_number_operator 레이아웃에 추가
        #각 숫자 버튼을 클릭했을 때, 숫자가 수식창에 입력 될 수 있도록 시그널 설정
        number_button_dict = {}
        x = 4
        for number in range(0, 10):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].clicked.connect(lambda state, num = number:
                                                       self.number_button_clicked(num))

            #숫자 버튼을 기존의 코드 형식을 유지하면서도 윈도우 표준 계산기의 배열과 동일하게 하기 위해 아래와 같이 구성
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

        #소숫점 버튼과 '+/-' 버튼을 입력하고 시그널 설정
        button_dot = QPushButton(".")
        button_dot.clicked.connect(lambda state, num = ".": self.number_button_clicked(num))
        layout_number_operator.addWidget(button_dot, 5, 2)

        button_plus_minus = QPushButton("+/-")
        button_plus_minus.clicked.connect(lambda state, operation = "+/-": self.button_operation_clicked(operation))
        layout_number_operator.addWidget(button_plus_minus, 5, 0)

        #각 레이아웃을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_equation_solution)
        main_layout.addLayout(layout_number_operator)

        self.setLayout(main_layout)
        self.show()

    ###########
    #functions#
    ###########

    #숫자 버튼 클릭 시 화면에 숫자 보여주고 equation 문자열에 숫자 추가
    def number_button_clicked(self, num):
        equation = self.equation.text()
        equation += str(num)
        self.equation_memory.insert(str(num))
        self.equation.setText(equation)

    #연산자 버튼 클릭 시 화면 지우고 equation_memory 문자열에 연산자 추가
    def button_operation_clicked(self, operation):
        self.equation_memory.insert(operation)
        self.equation.setText('')

    #'='버튼 누르면 스택을 이용해 후위표기법으로 변환 후 계산해 결과 보여줌
    def button_equal_clicked(self):
        #나중에 계산 시 리스트로 equation을 만들어야 하는데 연산자의 문자열 길이가 1보다 크면 하나의 연산자를 지칭해도
        #하나의 연산자로 생각하는데 문제가 생길 수 있으므로 아래와 같이 문자열 길이가 1보다 큰 연산자를 다른 문자열로 바꿔줌
        #'root' -> 'r', '^2'(제곱) -> '^', '1/x' -> 'v', '+/-' -> 'm'
        equation = self.equation_memory.text()
        equation = equation.replace("root", "r")
        equation = equation.replace("^2", "^")
        equation = equation.replace("1/x", "v")
        equation = equation.replace("+/-", "m")

        #연산자 기준으로 나눠서 리스트 만듦
        list_tokens = list(equation)
        lst = []    #후위표기법으로 나타낸 식 저장할 리스트
        stack = []  #스택 생성
        prior = {'r':4, '^':4, 'v':4, 'm':4, '*':3,'/':3,'+':2,'-':2,'(':1} #우선 순위 결정
        for n in range(len(list_tokens)):   #토큰 길이만큼 반복
            if list_tokens[n].isdecimal():  #token이 숫자이면 리스트에 추가
                lst.append(list_tokens[n])
            elif list_tokens[n] == '(': #'('이면 stack에 추가
                    stack.append(list_tokens[n])
            elif list_tokens[n] == ')':  #')'가 나오면 stack에서 (가 나올때까지 pop처리 및 lst에 추가. 
                while stack[-1] != '(':
                    lst.append(stack.pop())
                stack.pop() #'('가 나타나면 pop처리
            else:   #tokens[n]이 stack[-1]의 우선순위와 같거나 보다 작으면 tokens[n]의 우선순위가 더 커질때까지 pop
                while stack and prior[list_tokens[n]] <= prior[stack[-1]]:
                    lst.append(stack.pop()) #pop한 것들 lst에 추가 시켜줌   
                stack.append(list_tokens[n]) #위의 조건이 완료 되면 stack에 추가
        while len(stack) != 0:  #stack에 남아있는 연산자들 lst에 추가
            lst.append(stack.pop())

        #후위표기법으로 표현된 식 계산
        def Calculate(tokens):
            stack = []  #스택 생성
            for token in tokens:
                if token == '+':
                    stack.append(stack.pop()+stack.pop())
                elif token == '-':
                    stack.append(-(stack.pop()-stack.pop()))
                elif token == '*':
                    stack.append(stack.pop()*stack.pop())
                elif token == '/':
                    rv = stack.pop()
                    stack.append(stack.pop()/rv)
                elif token == 'r':
                    stack.append(stack.pop()**(1/2))
                elif token == 'v':
                    stack.append(1/stack.pop())
                elif token == '^':
                    stack.append(stack.pop()**2)
                elif token == 'm':
                    stack.append(-stack.pop())
                else:
                    stack.append(int(token))
            return stack.pop()
        solution = str(Calculate(lst))
        self.equation.setText(solution) #계산 결과 입력창에 보여줌

    #'C', 'CE' button 클릭 시 화면 지워줌
    #'C', 'CE' button 클릭 시 저장된 내용 지움
    def button_clear_clicked(self):
        self.equation.setText("")
        self.equation_memory.setText("")

    #backspace 버튼 클릭 시 문자열 하나씩 지움
    def button_backspace_clicked(self):
        equation = self.equation.text()
        equation = equation[:-1]
        self.equation.setText(equation)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())