# 12.17
import math
class MyCube:
    def __init__(self,length):
        self.side = length

    def volume(self):
        v = pow(self.side,3)
        return round(v,2)
# round四舍五入函数
    def surface_area(self):
        s = pow(self.side,2)*6
        return round(s,2)

if __name__ == "__main__":
    side = float(input("请输入立方体的边长："))
    cube = MyCube(float(side))
    print(f"体积：{cube.volume()}")
    print(f"表面积：{cube.surface_area()}")

class Calculator:
    def __init__(self):
        self.result = 0.0
    def add(self, a,b):
        return round(a+b,2)
    def subtract(self,a,b):
        return round(a-b,2)
    def multipy(self,a,b):
        return round(a*b,2)
    def divide(self,a,b):
        return round(a/b,2)

if __name__ == "__main__":
    a = int(input("请输入第一个数:"))
    b = int(input("请输入第二个数:"))
    c = input("请输入运算符:")
    calc = Calculator()

    if c == '+':
        result = calc.add(a, b)
    elif c == '-':
        result = calc.subtract(a, b)
    elif c == '*':
        result = calc.multipy(a, b)
    elif c == '/':
        result = calc.divide(a, b)
    else:
        result = "错误: 无效的运算符"
    round(result,2)
    print(f"结果：{result}")
