'''
Copyright (c) 2025 Kota UCHIDA

FH-P20H: Fuse holder (ELPA)
'''

import cadquery as cq

BODY_L = 22
BODY_W = 8.8
BODY_H = 5.6

PIN_T = 0.4
PIN_L = 9.1
PIN_W = 3.8
PIN_H = 4.2

HOLDER_W = 4.6
HOLDER_H = 10

def new():
    center_xy = (True, True, False)

    body = (
        cq.Workplane()
        .box(BODY_L, BODY_W, BODY_H, centered=center_xy)
        .faces('>Z')
        .hole(3.2)
        .cut(
            cq.Workplane()
            .box(7.6, 7.4, 4.2)
            .translate((0, 0, BODY_H - 4.2/2))
        )
    )

    holder_l1 = (
        cq.Workplane()
        .box(HOLDER_W, PIN_T, HOLDER_H)
        .translate((HOLDER_W/2 - BODY_L/2, 5.5/2, HOLDER_H/2 + PIN_H))
    )
    holder_l2 = holder_l1.mirror('XZ')
    pin_l = (
        cq.Workplane()
        .box(PIN_L + HOLDER_W, PIN_W, PIN_T)
        .edges('|Z and <X')
        .fillet(PIN_W/2 - 0.01)
        .faces('>Z')
        .workplane(origin=(2 - PIN_L/2 - HOLDER_W/2, 0, 0))
        .hole(2.5)
        .translate((HOLDER_W/2 - BODY_L/2 - PIN_L/2, 0, PIN_H))
        .union(holder_l1)
        .union(holder_l2)
    )
    pin_r = pin_l.mirror('YZ')

    assy = (
        cq.Assembly(name='FH-P20H')
        .add(body, name='body', color=cq.Color('peachpuff2'))
        .add(pin_l, name='pin_l', color=cq.Color('gray90'))
        .add(pin_r, name='pin_r', color=cq.Color('gray90'))
    )

    return assy

def main():
    obj = new()
    show_object(obj)
    obj.save('step_files/FH-K20H.step')

if __name__ == '__cq_main__':
    main()
