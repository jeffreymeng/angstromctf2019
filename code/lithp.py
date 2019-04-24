import math

str = '19 4 14 3 10 17 24 22 8 2 5 11 7 26 0 25 18 6 21 23 9 13 16 1 12 15 27 20'
reorder = list(map(int, str.split()))

str2 = '8930 15006 8930 10302 11772 13806 13340 11556 12432 13340 10712 10100 11556 12432 9312 10712 10100 10100 8930 10920 8930 5256 9312 9702 8930 10712 15500 9312'
encrypted = list(map(int, str2.split()))

finallist = [0 for i in range(28)]
counter = 0

for i in reorder:
    x = encrypted[counter] * -1
    finallist[i] = int((1 + math.sqrt(1 - 4 * x)) / 2)
    counter += 1

flag = ''
for n in finallist:
    flag += chr(n)
print(flag)
