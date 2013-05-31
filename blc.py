"""
Binary Lambda Calculus

e : 00 e   (Lam)
  | 01 e e (App)
  | [1] 0  (Var)

Var encodes DeBruijn indices with

0 = 10
1 = 110
2 = 1110
3 = 11110
...

Closure : TE Term Env
        | IDX Int

Env : [Closure]

[[e]] = Return Closure | Apply Term Term Env

"""

#------------------------------------------------------------------------
# Structures
#------------------------------------------------------------------------

class App(object):
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2

    def __str__(self):
        return '%s(%s)' % (self.e1, self.e2)

class Lam(object):
    def __init__(self, e):
        self.e = e
    def __str__(self):
        return '\%s' % self.e

class Var(object):
    def __init__(self, i):
        self.i = i
    def __str__(self):
        return '%s' % self.i

class Return(object):
    def __init__(self, cls):
        self.cls = cls

class Apply(object):
    def __init__(self, e1, e2, env):
        self.e1 = e1
        self.e2 = e2
        self.env = env

class Idx(object):
    def __init__(self, i):
        self.i = i

class TE(object):
    def __init__(self, term, env):
        self.term = term
        self.env = env

#------------------------------------------------------------------------
# Normalization
#------------------------------------------------------------------------

def span(p, xs):
    for i, x in enumerate(xs):
        if not p(x):
            return (xs[0:i], xs[i:])
    return ([],xs)

def parse(xs):
    if xs[0] == '0' and xs[1] == '0':
        t, xs = parse(xs[2:])
        return Lam(t), xs
    elif xs[0] == '0' and xs[1] == '1':
        l, xs = parse(xs[2:])
        r, xss = parse(xs)
        return App(l, r), xss
    elif xs[0] == '1':
        os, xs = span(lambda x: x=='1', xs)
        return Var(len(os)), ('0' + xs)
    else:
        raise Exception("Invalid expression")

def whnf(e, env):
    if isinstance(e, Var):
        term = env[e.i-1]
        if isinstance(term, Idx):
            return Return(term)
        elif isinstance(term, TE):
            return whnf(term.term, term.env)
    elif isinstance(e, Lam):
        return Return(TE(e, env))
    elif isinstance(e, App):
        l = e.e1
        r = e.e2

        wl = whnf(l, env)
        if isinstance(wl, Return) and \
            isinstance(wl.cls, TE) and \
            isinstance(wl.cls.term, Lam):
            le = wl.cls.term.e
            env_ = wl.cls.env
            return whnf(le, [TE(r, env)] + env_)
        else:
            return Apply(wl, r, env)
    else:
        assert 0


def _nf(d, t):
    if isinstance(t, Apply):
        return App(_nf(d, t.e1), nf(d, t.e2, t.env))
    elif isinstance(t, Return):
        if isinstance(t.cls, TE) and isinstance(t.cls.term, Lam):
            return Lam(nf((d+1), t.cls.term.e, [Idx(d)] + t.cls.env))
        elif isinstance(t.cls, TE):
            return t.cls.term
        elif isinstance(t.cls, Idx):
            return Var(d - t.cls.i - 1)
        else:
            assert 0
    else:
        assert 0

def nf(d, t, env):
    return _nf(d, whnf(t, env))

prg1 = '0010'
prg2 = "0000000101101110110"
prg3 = "00010001100110010100011010000000010110000010010001010111110111101001000110100001110011010000000000101101110011100111111101111000000001111100110111000000101100000110110"

p1 = parse(prg1)[0]
p2 = parse(prg2)[0]
p3 = parse(prg3)[0]

print nf(0, p1, [])
print nf(0, p2, [])
print nf(0, p3, [])
