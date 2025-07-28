'''
Copyright (c) 2025 Kota UCHIDA

Generic Screw
'''

import bisect
import cadquery as cq
from collections import namedtuple
import math

Prop = namedtuple('Prop', ['M', 'pitch', 'dk', 'k'])
PROPS = [
    Prop(2.0, 0.4,  4.5,  1.2),
    Prop(2.3, 0.4,  5.2,  1.4),
    Prop(2.5, 0.4,  5.2,  1.5),
    Prop(2.6, 0.45, 5.7,  1.6),
    Prop(3.0, 0.5,  6.9,  1.9),
]

def interpolate(p0, p1, key, m):
    '''与えられた2点を結ぶ直線で線形補間を行う'''
    a = (getattr(p1, key) - getattr(p0, key)) / (p1.M - p0.M)
    b = getattr(p0, key) - a * p0.M
    return a * m + b

def get_prop(m_dia):
    i = bisect.bisect(PROPS, m_dia, key=lambda p: p.M)
    if i < len(PROPS) and (m_dia - 0.01 < PROPS[i].M < m_dia + 0.01):
        return PROPS[i]
    if i >= 1 and (m_dia - 0.01 < PROPS[i-1].M < m_dia + 0.01):
        return PROPS[i-1]

    # 線形補間
    if i == 0 or len(PROPS):
        p0 = PROPS[0]
        p1 = PROPS[-1]
    else:
        p0 = PROPS[i - 1]
        p1 = PROPS[i]

    pitch = interpolate(p0, p1, 'pitch', m_dia)
    dk = interpolate(p0, p1, 'dk', m_dia)
    k = interpolate(p0, p1, 'k', m_dia)
    print(f'pitch, dk, k are interpolated: dk={dk} k={k}')
    return Prop(m_dia, pitch, dk, k)

def new_truss(m_dia, length):
    '''
    トラスねじのモデルを作る

    m_dia:       ねじの呼び径
    len:         ねじの長さ（ねじ頭の底面からねじ端までの長さ）
    '''

    p = get_prop(m_dia)

    '''
    dk: ねじ頭の直径
    k: ねじ頭の高さ

       _--_     -
    _-'    '-_  | k
    ----------  -
    <-- dk -->
    '''
    x = math.pi - 2*math.atan2(p.dk/2, p.k)
    radius = p.dk/2/math.sin(x)
    head = (
        cq.Workplane('XY')
        .sphere(radius, (0, 0, 1), (math.pi/2 - x)*180/math.pi, 90)
        .translate((0, 0, p.k - radius))
    )

    body = (
        cq.Workplane()
        .cylinder(length, m_dia/2 * 0.95)
        .translate((0, 0, -length/2))
        .edges('<Z')
        .chamfer(p.M/10)
    )

    return head.add(body).combine()

def main():
    obj = new_truss(2.6, 5)
    show_object(obj)

if __name__ == '__cq_main__':
    main()
