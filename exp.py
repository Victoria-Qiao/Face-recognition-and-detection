import numpy as np

a = np.array([1,2,3])
print(a)
print("type of a: ")
print(type(a))
b = np.array([2,3,4])
v = []
v.append(a)
v.append(b)
print(v)
print("type of v: ")
print(type(v))

u = np.array(v)
print(u)
print("type of u: ")
print(type(u))