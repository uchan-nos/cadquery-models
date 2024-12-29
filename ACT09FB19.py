'''
Copyright (c) 2024 Kota UCHIDA

AC-T09FB19: AC Outlet (EDK)
'''

import cadquery as cq
from lib import obj

TOP_W = 23
TOP_D = 16
TOP_H = 3
HOLE_W = 2.6
HOLE_L_LONG = 8.7
HOLE_L = 7.2
BODY_W = 20.0
BODY_D = 12.4
BODY_THIN_D = 8.8
BODY_H = 21.0

PIN_W = 0.6
PIN_D = 4.75
PIN_H = 8.2
PINHOLE_LARGE_D = 2.8
PINHOLE_SMALL_D = 1.6
PIN_DIST = 10.0

STOPPER_LEN = 18
STOPPER_GAP = 1.8

def make_top_hole(length):
    return (
        cq.Workplane()
        .box(HOLE_W, length, TOP_H, centered=(True, True, False))
        .faces('>Z')
        .workplane()
        .rect(HOLE_W + 1.8, length + 1.8)
        .extrude(-1, taper=45)
    )

def new():
    top_plate = (
        cq.Workplane()
        .box(TOP_W, TOP_D, TOP_H, centered=(True, True, False))
        .edges('|Z')
        .fillet(0.8)
        .cut(
            make_top_hole(HOLE_L)
            .translate((PIN_DIST/2, 0, 0))
        )
        .cut(
            make_top_hole(HOLE_L_LONG)
            .translate((-PIN_DIST/2, 0, 0))
        )
    )

    stopper = (
        cq.Workplane('ZY')
        .lineTo(STOPPER_LEN - 13.5, 2)
        .hLine(3)
        .lineTo(STOPPER_LEN - 5.2, 3.2)
        .lineTo(STOPPER_LEN - 1.8, 5)
        .lineTo(STOPPER_LEN, 3)
        .lineTo(STOPPER_LEN - 11, 0.7)
        .close()
        .extrude(6/2, both=True)
        .translate((0, 0, -STOPPER_LEN - STOPPER_GAP))
    )
    stopper1 = stopper.translate((0, BODY_THIN_D/2, 0))
    stopper2 = stopper1.mirror('XZ')

    body = (
        cq.Workplane()
        .box(6.2, BODY_D, BODY_H)
        .translate(((6.2 - BODY_W)/2, 0, -BODY_H/2))
        .edges('|Z')
        .fillet(0.8)
        .union(
            cq.Workplane()
            .box(BODY_W - 6.2, BODY_THIN_D, BODY_H)
            .translate(((BODY_D - 6.2)/2, 0, -BODY_H/2))
        )
        .union(stopper1)
        .union(stopper2)
        .union(
            cq.Workplane()
            .box(9.5, 12.3, 7.3)
            .translate((9.5/2 - 3, 0, -BODY_H + 7.3/2))
        )
    )

    pin_root = (
        cq.Workplane()
        .box(PIN_W, 9.7, 1.9)
        .translate((0, 0, -BODY_H - 1.9/2))
        .edges('|X and <Z')
        .chamfer(1.8)
    )

    pin = (
        cq.Workplane()
        .box(PIN_W, PIN_D, PIN_H)
        .faces('<X')
        .workplane()
        .hole(PINHOLE_LARGE_D)
        .center(0, -1.1)
        .hole(PINHOLE_SMALL_D)
        .translate((0, 0, -BODY_H - PIN_H/2))
        .edges('|X and <Z')
        .chamfer(0.9)
        .edges('<Z and <X')
        .chamfer(0.5, 0.1)
        .edges('<Z and >X')
        .chamfer(0.1, 0.5)
        .union(pin_root)
    )
    pin1 = pin.translate((-PIN_DIST/2, 0, 0))
    pin2 = pin.translate((PIN_DIST/2, 0, 0))

    color = cq.Color('gray20')
    pincolor = cq.Color('gray90')

    assy = (
        cq.Assembly(name='all')
        .add(top_plate, color=color)
        .add(body, color=color)
        .add(pin1, color=pincolor)
        .add(pin2, color=pincolor)
    )
    return assy

def main():
    obj = new()
    show_object(obj)
    obj.save('step_files/AC-T09FB19.step')

if __name__ == '__cq_main__':
    main()
