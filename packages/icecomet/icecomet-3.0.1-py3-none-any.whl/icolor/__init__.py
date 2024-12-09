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
        self.ijset = '\033[92m'
        self.jiset = '\033[93m'
    def show(self):
        print(f"{self.gray}gray {self.red}red {self.green}green {self.yello}yello {self.blue}blue {self.magenta}magenta {self.sky}sky {self.white}white {self.set}")
        print(f"{self.grayk}gray {self.redk}red {self.greenk}green {self.yellok}yello {self.bluek}blue {self.magentak}magenta {self.skyk}sky {self.whitek}white {self.set}")

##############################################################################################
# HEX
import matplotlib.pyplot as plt
class color_HEX_subMain:
    def __init__(self) -> None:
        self.red = '#FF0000'        # สีแดง
        self.green = '#00FF00'      # สีเขียว
        self.blue = '#0000FF'       # สีน้ำเงิน
        self.black = '#000000'      # สีดำ
        self.white = '#FFFFFF'      # สีขาว
        self.yellow = '#FFFF00'     # สีเหลือง
        self.cyan = '#00FFFF'       # สีฟ้า (Cyan)
        self.magenta = '#FF00FF'    # สีม่วงแดง (Magenta)
    def show_colors(self):
        colors = [self.red, self.green, self.blue, self.black, self.white, self.yellow, self.cyan, self.magenta]
        color_names = ['red', 'green', 'blue', 'black', 'white', 'yellow', 'cyan', 'magenta']
        self._plot_colors(colors, color_names)

    def _plot_colors(self, colors, color_names):
        plt.figure(figsize=(8, 2))
        plt.barh(range(len(colors)), [1] * len(colors), color=colors, edgecolor='black')
        plt.yticks(range(len(colors)), color_names)
        plt.xlim(0, 1)
        plt.gca().invert_yaxis()
        plt.show()

class color_HEX_sub1:
    def __init__(self) -> None:
        self.light_gray = '#D3D3D3' # สีเทาอ่อน
        self.dark_gray = '#A9A9A9'  # สีเทาเข้ม
        self.silver = '#C0C0C0'     # สีเงิน
        self.gray = '#808080'       # สีเทา
        self.brown = '#A52A2A'      # สีน้ำตาล
        self.gold = '#FFD700'       # สีทอง
        self.orange = '#FFA500'     # สีส้ม
        self.pink = '#FFC0CB'       # สีชมพู
        self.purple = '#800080'     # สีม่วง
        self.light_blue = '#ADD8E6' # สีฟ้าอ่อน
        self.light_green = '#90EE90' # สีเขียวอ่อน
    def show_colors(self):
        colors = [self.light_gray, self.dark_gray, self.silver, self.gray, self.brown, self.gold, self.orange, self.pink, self.purple, self.light_blue, self.light_green]
        color_names = ['light_gray', 'dark_gray', 'silver', 'gray', 'brown', 'gold', 'orange', 'pink', 'purple', 'light_blue', 'light_green']
        self._plot_colors(colors, color_names)
    
    def _plot_colors(self, colors, color_names):
        plt.figure(figsize=(8, 2))
        plt.barh(range(len(colors)), [1] * len(colors), color=colors, edgecolor='black')
        plt.yticks(range(len(colors)), color_names)
        plt.xlim(0, 1)
        plt.gca().invert_yaxis()
        plt.show()


class color_HEX_sub2:
    def __init__(self) -> None:
        self.dark_red = '#8B0000'   # สีแดงเข้ม
        self.dark_green = '#006400' # สีเขียวเข้ม
        self.dark_blue = '#00008B'  # สีน้ำเงินเข้ม
        self.dark_orange = '#FF8C00' # สีส้มเข้ม
        self.olive = '#808000'      # สีเขียวมะกอก
        self.teal = '#008080'       # สีฟ้าน้ำทะเล (Teal)
        self.navy = '#000080'       # สีกรมท่า
    def show_colors(self):
        colors = [self.dark_red, self.dark_green, self.dark_blue, self.dark_orange, self.olive, self.teal, self.navy]
        color_names = ['dark_red', 'dark_green', 'dark_blue', 'dark_orange', 'olive', 'teal', 'navy']
        self._plot_colors(colors, color_names)

    def _plot_colors(self, colors, color_names):
        plt.figure(figsize=(8, 2))
        plt.barh(range(len(colors)), [1] * len(colors), color=colors, edgecolor='black')
        plt.yticks(range(len(colors)), color_names)
        plt.xlim(0, 1)
        plt.gca().invert_yaxis()
        plt.show()

class color_HEX_other:
    def __init__(self):
        self.coral = '#FF99CC'      # สีส้มอ่อน
        self.cream = '#FFF599'      # สีครีม


class color_HEX:
    def __init__(self) -> None:
        self.main = color_HEX_subMain()
        self.create = color_HEX_sub1()
        self.UxUi = color_HEX_subMain()
        self.other = color_HEX_other()
    def RGB_toHEX(self, red=0, green=0, blue=0):
        r = hex(red)[2:]  # แปลงค่า red เป็นเลขฐาน 16 และตัด '0x' ออก
        g = hex(green)[2:]  # แปลงค่า green เป็นเลขฐาน 16 และตัด '0x' ออก
        b = hex(blue)[2:]  # แปลงค่า blue เป็นเลขฐาน 16 และตัด '0x' ออก
        
        # ตรวจสอบว่าค่าที่ได้มี 2 หลักหรือไม่ ถ้าไม่ให้เติม 0 ข้างหน้า
        r = r.zfill(2)
        g = g.zfill(2)
        b = b.zfill(2)

        return f'#{r}{g}{b}'



ct = color_text()
cH = color_HEX()
