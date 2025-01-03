'''
Copyright (c) 2024 Kota UCHIDA

Generic Hex Nut
'''

import cadquery as cq
import math

def new(m_dia, size, t, fillet_side=None, fillet_rate=2, angle=0):
    '''
    六角ナットのモデルを作る

    m_dia:       ねじの呼び径
    size:        ナットの外径（辺と辺の距離）
    t:           ナットの厚み
    fillet_side: フィレット有無（None, 'top', 'bottom', 'both'）
    fillet_rate: フィレットのかかり具合（1 以上。1 が最も強いフィレット）
    angle:       開始角度
    '''
    e_radius = size / math.sqrt(3)

    raw_nut = (
        cq.Workplane()
        .sketch()
        .regularPolygon(e_radius, 6, angle)
        .finalize()
        .extrude(t)
        .faces('>Z')
        .hole(m_dia)
    )

    '''
    TODO: ねじ溝を作る
    '''

    if fillet_side is None:
        return raw_nut

    cutter_r = fillet_rate * e_radius
    cutter_h = cutter_r * math.cos(math.asin(size/2 / cutter_r))
    cutter = (
        cq.Workplane()
        .cylinder(t + 1, e_radius + 1, centered=(True, True, False))
        .cut(
            cq.Workplane()
            .sphere(cutter_r)
            .translate((0, 0, t - cutter_h))
        )
    )

    cutted = raw_nut
    if fillet_side in {'both', 'top'}:
        cutted = cutted.cut(cutter)
    if fillet_side in {'both', 'bottom'}:
        cb = (
            cutter
            .mirror('XY')
            .translate((0, 0, t))
        )
        cutted = cutted.cut(cb)

    return cutted

def new_with_seat(m_dia, size, total_t, seat_d, seat_t, fillet_side=None, fillet_rate=2, angle=0):
    if fillet_side not in {None, 'top'}:
        raise ValueError('fillet_side must be None or top')

    return (
        new(m_dia, size, total_t, fillet_side, fillet_rate, angle)
        .intersect(
            cq.Workplane()
            .cylinder(total_t, seat_d/2, centered=(True, True, False))
        )
        .union(
            cq.Workplane()
            .cylinder(seat_t, seat_d/2, centered=(True, True, False))
            .faces('>Z')
            .hole(m_dia)
        )
    )

def main():
    obj = new(12, 17, 5, fillet_side='both')
    show_object(obj)

if __name__ == '__cq_main__':
    main()
