# tutorial
# https://www.programiz.com/python-programming/generator
# https://realpython.com/introduction-to-python-generators/


# simple generator
def my_gen():
    n = 1
    print("first print")
    yield n

    n += 1
    print("second print")
    yield n

    n += 1
    print("third print")
    yield n

tmp = my_gen()  # return iterator object without any execution
type(tmp)

next(tmp)


# combine generator and for loop
for item in my_gen():
    print(item)


# for loop embeded in generator
def my_gen2(n):
    for i in range(n):
        yield i

tmp = my_gen2(10)

next(tmp)


# generator expression
a = list(range(10))

b = [x**2 for x in a]
print(b)

c = (x**2 for x in a)
print(c)

for item in c:
    print(item)


import time

s = list(range(100000000))

t0 = time.time()
tmp = [x for x in s if x % 2 == 0]
print(sum(tmp))
t1 = time.time()
print("time: %.2f seconds" % (t1 - t0))

t0 = time.time()
tmp = (x for x in s if x % 2 == 0)
print(sum(tmp))
t1 = time.time()
print("time: %.2f seconds" % (t1 - t0))

