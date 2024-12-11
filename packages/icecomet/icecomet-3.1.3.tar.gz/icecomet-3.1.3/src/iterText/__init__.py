import os

class color_text:
    def __init__(self) -> None:
        self.gray = '\033[90m'
        self.red = '\033[91m'
        self.green = '\033[92m'
        self.yello = '\033[93m'
        self.blue = '\033[94m'
        self.magenta = '\033[95m'
        self.sky = '\033[96m'
        self.white = '\033[97m'


        self.grayk = '\033[100m'
        self.redk = '\033[101m'
        self.greenk = '\033[102m'
        self.yellok = '\033[103m'
        self.bluek = '\033[104m'
        self.magentak = '\033[105m'
        self.skyk = '\033[106m'
        self.whitek = '\033[107m'

        self.set = '\033[0m'

    def iterText_show(self):
        print(f"{self.gray}gray {self.red}red {self.green}green {self.yello}yello {self.blue}blue {self.magenta}magenta {self.sky}sky {self.white}white {self.set}")
        print(f"{self.grayk}gray {self.redk}red {self.greenk}green {self.yellok}yello {self.bluek}blue {self.magentak}magenta {self.skyk}sky {self.whitek}white {self.set}")


class cursor_control:

    mode = 'return'

    def up(self,number=1):
        if self.mode != 'return':
            print(f'\033[{number}A')
        else :
            return f'\033[{number}A'

    def down(self,number=1):
        if self.mode != 'return':
            print(f'\033[{number}B')
        else :
            return f'\033[{number}B'

    def right(self,number=1):
        if self.mode != 'return':
            print(f'\033[{number}C')
        else :
            return f'\033[{number}C'

    def left(self,number=1):
        if self.mode != 'return':
            print(f'\033[{number}B')
        else :
            return f'\033[{number}B'


#-------------------------------------------
    def uppest(self,number=999):
        if self.mode != 'return':
            print(f'\033[{number}B')
        else :
            return f'\033[{number}B'

    def downest(self,number=999):
        if self.mode != 'return':
            print(f'\033[{number}B')
        else :
            return f'\033[{number}B'

    def rightest(self,number=999):
        if self.mode != 'return':
            print(f'\033[{number}C')
        else :
            return f'\033[{number}C'

    def leftest(self,number=999):
        if self.mode != 'return':
            print(f'\033[{number}D')
        else :
            return f'\033[{number}D'
#-------------------------------------------
    def goto(self,colum=1,row=1):
        if self.mode != 'return':
            print(f'\033[{colum};{row}H')
        else :
            return f'\033[{colum};{row}H'

    def clearAll(self):
        os.system('clear')

    def clearAtCursor(self):
        if self.mode != 'return':
            print('\033[P')
        else :
            return '\033[P'

    def clearCursor2end(self):
        if self.mode != 'return':
            print('\033[J')
        else :
            return '\033[J'
    
    def clearCursor2rightest(self):
        if self.mode != 'return':
            print('\033[K')
        else :
            return '\033[K'

    def clearLeft2cursor(self):
        if self.mode != 'return':
            print('\033[1K')
        else :
            return '\033[1K'

    def clearThisline(self):
        if self.mode != 'return':
            print('\033[2K')
        else :
            return '\033[2K'



ct = color_text()
cc = cursor_control()
