# Half and Half
slopey112 - 4/24/2019

We are given a python script that generates a cipher.
```python
from secret import flag

def xor(x, y):
	o = ''
	for i in range(len(x)):
		o += chr(ord(x[i])^ord(y[i]))
	return o

assert len(flag) % 2 == 0

half = len(flag)//2
milk = flag[:half]
cream = flag[half:]

assert xor(milk, cream) == '\x15\x02\x07\x12\x1e\x100\x01\t\n\x01"'
```
The code is very simple. The program first splits the flag into half and half. Then, it iterates through each index in the arrays. It returns an ASCII character based on the XOR of the decimal value of two corresponding characters in the split arrays.

As we can see, the results of that cipher is given at the bottom. From this, we can deduce that the length of the flag must be 24 because there are 12 characters in the resulting cipher.

Next, we can also deduce the first five characters and the last character in the flag. We know the flag must begin with `actf{` and must end with `}`.

The first major observation is that we can deduce six characters already, because of XOR properties. First, the commutative property:
```
a = b ^ c
a = c ^ b
```
Next, XOR has another interesting property.
```
a = b ^ c
b = c ^ a
c = a ^ b
```
From this, we can already deduce a few of the characters. Below I've arranged the two halves of the flag on top of each other, with the result at the bottom. Unknown characters are `.`.
```
a   c   t   f   {   .   ..   . . .   .
.   .   .   .   .   .   ..   . . .   }
\x15\x02\x07\x12\x1e\x100\x01\t\n\x01"
```
Let's start from left to right and sweep across.
```
a ^ . = 0x15
. = chr(0x15 ^ ord(a))
. = 't'
```
Continuing along, we can deduce many of these characters as well.
```
a   c   t   f   {   .   ..   . . .   _
t   a   s   t   e   .   ..   . . .   }
\x15\x02\x07\x12\x1e\x100\x01\t\n\x01"
```
Now we're at a bit of a roadblock. How can we find the rest of the characters? We can start by making an assumption, that the flag is not obfuscated in any way. Given that, we can generate the possibilities for these characters with a quick [python script](/code/Half_and_Half.py).
```python
import string
import sys

search = string.ascii_lowercase + '_'

def decrypt(result):
    char = ord(result)
    for c in search:
        for c2 in search:
            if ord(c) ^ ord(c2) == char:
                print('{} {}'.format(c, c2))

decrypt(sys.argv[1])
```
Let's run this script on the first unknown character.
```
slopey112@slopey112:~/Documents/Code/payloads$ python3 decrypt.py $(python -c "print '\x10'")
a q
b r
c s
d t
e u
f v
g w
h x
i y
j z
q a
r b
s c
t d
u e
v f
w g
x h
y i
z j
```
By our first assumption that there is no obfuscation, the next letter following "taste" can only be "\_", "d", or "s" as only these can make spellable characters. As we can see our options are limited to "d" and "s", we'll take a guess and try "s". Now our cipher looks like this:
```
a   c   t   f   {   c   ..   . . .   _
t   a   s   t   e   s   ..   . . .   }
\x15\x02\x07\x12\x1e\x100\x01\t\n\x01"
```
Through deduction, the next character should be "\_" after "tastes", also by the same assumption as earlier. Running our script again, our guess is correct.
```
slopey112@slopey112:~/Documents/Code/payloads$ python3 decrypt.py 0
o _
_ o
```
Great.
```
a   c   t   f   {   c   o.   . . .   _
t   a   s   t   e   s   _.   . . .   }
\x15\x02\x07\x12\x1e\x100\x01\t\n\x01"
```
After some thinking, the "co" in the beginning reminds us of a particular drink that is generally associated with "half and half". I ran the script a few more times, and we found the pattern.
```
a   c   t   f   {   c   of   f e e   _
t   a   s   t   e   s   _g   o o d   }
\x15\x02\x07\x12\x1e\x100\x01\t\n\x01"
```
And we are left with our flag.
```
actf{coffee_tastes_good}
```
