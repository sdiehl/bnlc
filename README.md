Binary Lambda Calculus in Python
--------------------------------

The binary lambda calculus is defined as the following sequence
of bytes:

```
e : 00 e   (Lam)
  | 01 e e (App)
  | [1] 0  (Var)
```

The var rule encodes DeBruijn indices with the following pattern:

```
0 = 10
1 = 110
2 = 1110
3 = 11110
```

For example the SKI calculus can be expressed in Python as the
following lambda expressions:

```python
I = lambda x: x
K = lambda x: lambda y: x
S = lambda x: lambda y: lambda z: x(z)(y(z))  # (x z)(y z)
```

Or in the binary lambda calculus as:

```
I = 0010
K = 000010110
S = 00000010110111001011011101101110
```

The smallest eval machine for the binary lambda caluclus is the
following program:


```
  01010001
   10100000
    00010101
     10000000
      00011110
       00010111
        11100111
         10000101
          11001111
          000000111
         10000101101
        1011100111110
       000111110000101
      11101001 11010010
     11001110   00011011
    00001011     11100001
   11110000       11100110
  11110111         11001111
 01110110           00011001
00011010             00011010
```

Source: http://www.ioccc.org/2012/tromp/hint.html
