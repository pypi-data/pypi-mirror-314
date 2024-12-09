import math
from decimal import Decimal

# things I would like to have
def println(str):
    print(str + '\n')

def power(num, power):
    return pow(num, pow)

class Area2d:
    def circle(self, radius, piDigits, part):

        if piDigits < 0 or piDigits > 27:
            return None
        
        area = power(radius, 2) * pi(piDigits)
        return area * part

    def rectangle(self, length, width, part):
        area = length * width
        return area * part

    def triangle(self, base, height, part):
        area = base * height / 2
        return area * part
    
class SurfaceArea3d:
    def sphere(self, piDigits, radius):

        if piDigits < 0 or piDigits > 27:
            return None
        
        SA = 4 * pi(piDigits) * power(radius, 2)
        return SA

    def rectPrism(self, length, width, height):
        SA = (length * width + length * height + width * height) * 2
        return SA
    
    def trianglularPrism(self, base1, base2, base3, baseHeight, height):
        SA = 0
        if baseHeight != None:
            SA = Area2d.triangle(base1, baseHeight, 1) * 2 + (base1 + base2 + base3) * height
        else:
            s = (base1 + base2 + base3) / 2
            Ab = s * (s - base1) * (s - base2) * (s - base3)
            SA = 2 * Ab + (base1 + base2 + base3) * height

        return SA

def pi(digits):

    if digits < 0 or digits > 27:
        return None
    
    pi = "141592653589793238462643383"
    neededPi = "3."
    for i in range(digits):
        neededPi += pi[i]

    return Decimal(neededPi)

