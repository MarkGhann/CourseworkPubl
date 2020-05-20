import math as m

f1 = open("SGA.txt", "r")
Wga = list(f1.readline().split(' '))
print(Wga[0], Wga[1])
Wga[0], Wga[1] = float(Wga[0]), float(Wga[1])
Tga = list(f1.readline().split(' '))
Tga[0], Tga[1] = float(Tga[0]), float(Tga[1])

f2 = open("SAI.txt", "r")
Wai = list(f2.readline().split(' '))
print(Wai)
Wai[0], Wai[1] = float(Wai[0]), float(Wai[1])
Tai = list(f2.readline().split(' '))
Tai[0], Tai[1] = float(Tai[0]), float(Tai[1])

Sw = (1/100) * Wga[0] + (1/100) * Wai[0]
St = (1/100) * Tga[0] + (1/100) * Tai[0]

Tw = (Wga[1] - Wai[1])/m.sqrt(Sw)
Tt = (Tga[1] - Tai[1])/m.sqrt(St)

fw = Sw / (((1/99) * ((Wga[0]/100)**2) + (Wai[0]/100)**2)**(-1))
ft = St / (((1/99) * ((Tga[0]/100)**2) + (Tai[0]/100)**2)**(-1))
print(fw, ft, Tw)

Talpha = float(input())
T1minalpha = float(input())

taW = Talpha
t1W = T1minalpha
thalfW = 1.9842169002535168

a = Tw > taW 
b = Tw < t1W

IW1 = [Wga[1] - m.sqrt(Sw)/10*thalfW, Wga[1] + m.sqrt(Sw)/10*thalfW]
IW2 = [Wai[1] - m.sqrt(Sw)/10*thalfW, Wai[1] + m.sqrt(Sw)/10*thalfW]

TW1 = [Tga[1] - m.sqrt(St)/10*thalfW, Tga[1] + m.sqrt(St)/10*thalfW]
TW2 = [Tai[1] - m.sqrt(St)/10*thalfW, Tai[1] + m.sqrt(St)/10*thalfW]

f = open("intervalsI.txt", "w")
f.write(str(IW1) + " " + str(IW2) + " " + str(1 if a else (2 if b else 0)))
f.write("\n" + str(TW1) + " " + str(TW2))
f1.close()
f2.close()

f.close()

