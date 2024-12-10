# lumpur
learn to use methods for processing unclear response


## features
+ `Drag`, `Electric`, `Gravitational`, `Magnetic`, `Normal`, `Spring` classes in `forces` module.
+ `Rectangle`, `Triangle` classes in `shapes` module.
+ `Color2` class in `utils` module.
+ `Vect3` class in `vectors` module.
+ `binary()`function in `datasets.clasdata` module.
+ `plot_binary()` function in `datasets.dataviz` module.
+ `abbr()` function in `misc.info` module.


## illustrations
Some motions for single particle.

<img src="https://raw.githubusercontent.com/dudung/lumpur/refs/heads/main/docs/images/transient_drag_euler.png" width="300" /><img src="https://raw.githubusercontent.com/dudung/lumpur/refs/heads/main/docs/images/parabolic_gravitational_euler.png" width="300" />

<img src="https://raw.githubusercontent.com/dudung/lumpur/refs/heads/main/docs/images/harmonic_spring_euler.png" width="300" /><img src="https://raw.githubusercontent.com/dudung/lumpur/refs/heads/main/docs/images/circular_magnetic_euler.png" width="300" />

The motions are for particle moving in flowing viscous medium and performing some motions (parabolic, harmonic, circular).


## examples
Following are some examples of lumpur.

### vectors addition
$$
\begin{array}{rcl}
c_x & = & a_x + b_x, \newline
c_y & = & a_y + b_y, \newline
c_z & = & a_z + b_z.
\end{array}
$$
```py
from lumpur.vectors.vect3 import Vect3

a = Vect3(1, 2, 3)
b = Vect3(1, 1, 1)
c = a + b

print('    a =', a)
print('    b =', b)
print('a + b =', c)
```
```
    a = { "x": 1, "y": 2, "z": 3 }
    b = { "x": 1, "y": 1, "z": 1 }
a + b = { "x": 2, "y": 3, "z": 4 }
```

### vectors cross product
$$
\begin{array}{rcl}
c_x & = & a_y \ b_z - a_z \ b_y, \newline
c_y & = & a_z \ b_x - a_x \ b_z, \newline
c_z & = & a_x \ b_y - a_y \ b_x.
\end{array}
$$
```py
from lumpur.vectors.vect3 import Vect3

a = Vect3(1, 7, 3)
b = Vect3(3, 2, 4)
d = a * b

print('    a =', a)
print('    b =', b)
print('a x b =', d)
```
```
    a = { "x": 1, "y": 7, "z": 3 }
    b = { "x": 3, "y": 2, "z": 4 }
a x b = { "x": 22, "y": 5, "z": -19 }
```

### circular decision boundary
$$
0.41 - 0.8x - 1.2y + x^2 + y^2 = 0
$$
```py
import lumpur.datasets.clasdata as ldc
import lumpur.datasets.dataviz as ldv

coeffs = [[0.41], [-0.8, -1.2], [1, 0, 1]]
r1 = [0, 1.05, 0.05]
r2 = [0, 1.05, 0.05]
df = ldc.binary(coeffs, r1=r1, r2=r2)
ldv.plot_binary(df)
```
<img src="https://raw.githubusercontent.com/dudung/lumpur/refs/heads/main/docs/images/dataviz_circular.png" width="300" />

### linier decision boundary
$$
-x + y = 0
$$
```py
import lumpur.datasets.clasdata as ldc
import lumpur.datasets.dataviz as ldv

coeffs = [[0], [-1, 1]]
df = ldc.binary(coeffs)
ldv.plot_binary(df)
```
<img src="https://raw.githubusercontent.com/dudung/lumpur/refs/heads/main/docs/images/dataviz_linear.png" width="300" />

### abbreviation
```py
import lumpur.misc.info as info

print(info.abbrv())
```

```
learn to use methods for processing unclear response
```
