# Lithp
slopey112 - 4/24/2019

We are given a program and asked to decrypt the flag.
```lisp
;LITHP

(defparameter *encrypted* '(8930 15006 8930 10302 11772 13806 13340 11556 12432 13340 10712 10100 11556 12432 9312 10712 10100 10100 8930 10920 8930 5256 9312 9702 8930 10712 15500 9312))
(defparameter *flag* '(redacted))
(defparameter *reorder* '(19 4 14 3 10 17 24 22 8 2 5 11 7 26 0 25 18 6 21 23 9 13 16 1 12 15 27 20))

(defun enc (plain)
    (setf uwuth (multh plain))
    (setf uwuth (owo uwuth))
    (setf out nil)
    (dotimes (ind (length plain) out)
        (setq out (append out (list (/ (nth ind uwuth) -1))))))

(defun multh (plain)
    (cond
        ((null plain) nil)
        (t (cons (whats-this (- 1 (car plain)) (car plain)) (multh (cdr plain))))))

(defun owo (inpth)
    (setf out nil)
    (do ((redth *reorder* (cdr redth)))
        ((null redth) out)
        (setq out (append out (list (nth (car redth) inpth))))))

(defun whats-this (x y)
    (cond
        ((equal y 0) 0)
        (t (+ (whats-this x (- y 1)) x))))

;flag was encrypted with (enc *flag*) to give *encrypted*
```
The code is written in lisp, and it's very title is a reference to that; lithp is a parody language based off of lisp wherein all s's are replaced with th.

There's not much to say here if you don't know the language, but I'll first walk through the functions, starting from the bottom.

`whats-this` is much simpler than it seems. All it does is multiply its parameters, but is written recursively.

`owo` reorders its input such that the ith element in its parameter is moved to the jth, where j is the jth element in `*reorder*`such that the jth element is equal to i.

`multh` takes a list as its argument also. If we define the ith element as a, a becomes (1 - a) * a.

`enc` takes list and first calls `multh` on the input, and then calls `owo` on the input list. For each item in the newly defined list, it redefines it as the absolute value of itself.

All there is to do is to compute these operations in reverse. I've simplified these functions significantly in my [solution](code/Lithp.py) (written in python), but I hope it can still be readable.
```python
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

print(finallist)
```
And we get the result in a list.
```
slopey112@slopey112:/tmp$ python3 lithp.py
[97, 99, 116, 102, 123, 104, 101, 108, 112, 95, 109, 101, 95, 73, 95, 104, 97, 118, 101, 95, 97, 95, 108, 105, 116, 104, 112, 125]
```
Right off the bat, my instinct told me that the numbers were ASCII. So I added a few lines to my solution:
```python
flag = ''
for n in finallist:
    flag += chr(n)
print(flag)
```
And we get our flag.
```
slopey112@slopey112:/tmp$ python3 lithp.py
actf{help_me_I_have_a_lithp}
```
