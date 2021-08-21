from kivy.clock import mainthread
from kivy.core.text import Text
from kivy.config import Config
# Prevent window resizing by users
# Config.set must be in top of the file
Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window


# To split a string with multiple delimiters (re for regex)
import re

# Calling the external kv file
Builder.load_file("Cal.kv")


class myLayout(Widget):

    # Sign virable lists signs
    sign = ["÷", "×", "+", "-", "."]

    # Display clear function
    def clear(self):
        inputField = self.ids.cal_display
        inputField.font_size = 65
        inputField.text = '0'
        

    # Ans digit manipulate virable for auto delete after answer
    ans = False


    # For Input text dynamic 
    def dynamicInput(self):
        # get the input field by ID
        inputfield = self.ids.cal_display
        # Get the input field text
        txt = self.ids.cal_display.text        
        instance = Text(text_size=(350, None), font_size=65, text=txt)
        width, height = instance.render()
        while height > 77:
            instance.options['font_size'] *= .95
            width, height = instance.render()
        inputfield.font_size = instance.options['font_size']
        self.reset_scroll(inputfield)

    @mainthread
    def reset_scroll(self, abc):
        abc.scroll_x = abc.scroll_y = 0
    
    # # For Input text dynamic 
    # def dynamicInput(self,num=False):
    #     if num == False:
    #         num = 350
    #     # get the input field by ID
    #     inputfield = self.ids.cal_display
    #     # Get the input field text
    #     txt = self.ids.cal_display.text
    #     # get the height and width
    #     Height = inputfield.height
    #     # Width = inputfield.width
    #     instance = Text(text_size=(None, Height), font_size=65, text=txt)
    #     width, height = instance.render()
    #     while width > num:
    #         instance.options['font_size'] *= .97
    #         width, height = instance.render()
    #     inputfield.font_size = instance.options['font_size']


    # Equetion History virable and function
    hist = ""
    histry = []
    def history(self, hist="", show=""):
        if show == 0:
            if len(self.histry) < 2:
                self.histry.append(hist)
            else:
                self.histry = self.histry[1:]
                self.histry.append(hist)
        else:
            if self.histry == []:
                self.ids.cal_display.text = "0"
            else:
                self.ids.cal_display.text = self.histry[0]
                self.dynamicInput()
        self.hist = ""

    #
    # BackSpace function
    def backSpace(self):
        disp = self.ids.cal_display.text
        if disp == "Error" or disp == '0' or disp == '':
            self.ids.cal_display.text = '0'
        else:
            if len(disp) > 1:
                self.ids.cal_display.text = disp[:-1]
            else:
                self.ids.cal_display.text = '0'
                self.ids.cal_display.font_size = 65

    # function for +/- sign
    def plus_minus(self):
        disp = self.ids.cal_display.text
        if disp == "Error":
            self.ids.cal_display.text = '0'
        else:
            if '-' in disp[0]:
                self.ids.cal_display.text = f'{disp.replace("-","",1)}'
            else:
                self.ids.cal_display.text = f'-{disp}'

    #
    #  Input numbers function
    def inputNum(self, n):
        disp = self.ids.cal_display.text
        if disp == '0' or disp == "Error" or self.ans == True:
            self.ids.cal_display.text = f'{n}'
            self.ans = False
        else:
            self.ids.cal_display.text = f'{disp}{n}'

    #
    # Input Operator function
    def add_optr(self, optr):
        disp = self.ids.cal_display.text
        if disp == "Error":
            self.ids.cal_display.text = '0'
        else:
            if self.ans == True:
                self.ans = False
            if optr == '+':
                self.ids.cal_display.text = self.add_optr_helper(disp, optr)
            elif optr == '-':
                self.ids.cal_display.text = self.add_optr_helper(disp, optr)
            elif optr == '÷':
                self.ids.cal_display.text = self.add_optr_helper(disp, optr)
            elif optr == '×':
                self.ids.cal_display.text = self.add_optr_helper(disp, optr)
            elif optr == '.':
                self.ids.cal_display.text = self.add_optr_helper(disp, optr)

    #
    # Function for add opretor on cal display
    def add_optr_helper(self, stri, optr):
        if optr == '.':
            if stri[-1] in self.sign:
                arry = re.split('\+|\-|÷|×', stri[:-1])
                if optr in arry[-1]:
                    return stri
                else:
                    stri = stri[:-1] + optr
                    return stri
            else:
                arry = re.split('\+|\-|÷|×', stri)
                if optr in arry[-1]:
                    return stri
                else:
                    return f'{stri}{optr}'
        else:
            if stri[-1] in self.sign:
                stri = stri[:-1] + optr
                return stri
            else:
                return f'{stri}{optr}'

    def clcu_demo(self):
        disp = self.ids.cal_display.text
        print(eval(disp))

    #
    # Suppoter fun for calculate function
    def cal_fun(self, arry, optr):
        optrIndx = arry.index(optr)
        ans = None
        if optr == '÷':
            ans = float(arry[optrIndx-1])/float(arry[optrIndx+1])
        elif optr == '×':
            ans = float(arry[optrIndx-1])*float(arry[optrIndx+1])
        elif optr == '+':
            ans = float(arry[optrIndx-1])+float(arry[optrIndx+1])
        elif optr == '-':
            ans = float(arry[optrIndx-1])-float(arry[optrIndx+1])
        arry[optrIndx] = str(ans)
        arry = [arry[x]
                for x in range(len(arry)) if x != optrIndx-1 and x != optrIndx+1]
        self.calculate(arry)

    #
    # Calculation Answer Funtion
    def calculate(self, arry=""):
        try:
            if arry == "":
                disp = self.ids.cal_display.text
                if disp[-1] in self.sign:
                    arry = re.split('(\+|\-|÷|×)', disp[:-1])
                else:
                    arry = re.split('(\+|\-|÷|×)', disp)
                if disp[0] == "-":
                    arry = arry[2:]
                    arry[0] = f'-{arry[0]}'
                self.hist = ''.join(arry)
                self.calculate(arry)
            else:
                if '÷' in arry:
                    self.cal_fun(arry, '÷')
                elif '×' in arry:
                    self.cal_fun(arry, '×')
                elif '+' in arry:
                    self.cal_fun(arry, '+')
                elif '-' in arry:
                    self.cal_fun(arry, '-')
                else:
                    if arry:
                        self.history(self.hist, 0)
                        self.ans = True  
                        ans = arry[0].split(".")
                        if ans[-1] == '0':
                            self.ids.cal_display.text = ans[0]
                            self.dynamicInput()
                        else:
                            self.ids.cal_display.text = f'{arry[0]}'
                            self.dynamicInput()
                        if arry[0] == "-0":
                            self.ids.cal_display.text = '0'
        except:
            self.ids.cal_display.text = "Error"


class cal(App):
    def build(self):
        self.icon = 'Calc.ico'
        self.title = 'Calculator'
        # Set the window size
        Window.size = (400, 600)
        return myLayout()


if __name__ == "__main__":
    cal().run()
