'''
Copyright (c) 2024 Kota UCHIDA

CW-SB21KKGF: Rocker Switch (NKK)
'''

import cadquery as cq
from lib import obj

TOP_W = 21.1
TOP_D = 15.1
TOP_H = 2
HOLE_W = 15.8
HOLE_D = 10.6
BODY_W = 17.4
BODY_D = 12.6
BODY_H = 14.2

PIN_W = 4.75
PIN_D = 0.8
PIN_H = 8.1
PINHOLE_LARGE_D = 2.3
PINHOLE_SMALL_D = 1.6

def new():
    top_plate = (
        cq.Workplane()
        .box(TOP_W, TOP_D, TOP_H, centered=(True, True, False))
        .edges('|Z')
        .fillet(0.8)
        .cut(
            cq.Workplane()
            .box(HOLE_W, HOLE_D, TOP_H, centered=(True, True, False))
        )
    )
    body = (
        cq.Workplane()
        .box(BODY_W, BODY_D, BODY_H, centered=(True, True, False))
        .translate((0, 0, -BODY_H))
        .faces('<Z').workplane(origin=(-5, 0, 0))
        .box(6, 1, 5.2, centered=(True, True, False))
    )

    button_concave_r = 20
    button_rot_orig = (0, 0, -1)
    button_rot_axis = (0, 1, -1)
    button_rot_deg = 15
    mark_rot_degdiff = 10

    button_cut = (
        cq.Workplane('XZ')
        .cylinder(HOLE_D - 0.2, button_concave_r)
        .translate((0, 0, button_concave_r + 3.4))
    )
    button_mark_cut = (
        button_cut
        .translate((0, 0, 0.02))
    )

    button = (
        cq.Workplane('XZ')
        .moveTo(-15.8/2, -2)
        .lineTo(-12.9/2, 4.5)
        #.threePointArc((0, 3.5), (12.9/2, 4.5))
        .lineTo(12.9/2, 4.5)
        .lineTo(15.8/2, -2)
        .close()
        .extrude(HOLE_D/2 - 0.1, both=True)
        .cut(button_cut)
        .rotate(button_rot_orig, button_rot_axis, button_rot_deg)
    )
    button_mark_on = (
        cq.Workplane()
        .box(0.5, 3.2, 1)
        .translate((6.0, 0, 3.3))
        .rotate(button_rot_orig, button_rot_axis, -mark_rot_degdiff)
        .cut(button_mark_cut)
        .rotate(button_rot_orig, button_rot_axis, button_rot_deg)
    )
    button_mark_off = (
        cq.Workplane()
        .cylinder(1, 3.2/2)
        .cut(
            cq.Workplane()
            .cylinder(1, 3.2/2 - 0.5)
        )
        .translate((-4.7, 0, 3.3))
        .rotate(button_rot_orig, button_rot_axis, mark_rot_degdiff)
        .cut(button_mark_cut)
        .rotate(button_rot_orig, button_rot_axis, button_rot_deg)
    )
    button_mark = (
        button_mark_on
        .add(button_mark_off)
    )

    pin = (
        cq.Workplane()
        .box(PIN_W, PIN_D, PIN_H)
        .faces('<Y')
        .workplane()
        .hole(PINHOLE_LARGE_D)
        .center(0, -0.7)
        .hole(PINHOLE_SMALL_D)
        .translate((0, 0, -BODY_H - PIN_H/2))
        .edges('|Y and <Z')
        .chamfer(0.9)
        .edges('|X and <Z')
        .chamfer(0.5, 0.15)
    )
    pin1 = pin.translate((4, 8/2, 0))
    pin2 = pin1.mirror('XZ')
    pin1a = pin.translate((-5, 5/2, 0))
    pin2a = pin1a.mirror('XZ')

    color = cq.Color('gray20')
    pincolor = cq.Color('gray90')

    assy = (
        cq.Assembly()
        .add(top_plate, color=color)
        .add(body, color=color)
        .add(button, color=color)
        .add(pin1, color=pincolor)
        .add(pin1a, color=pincolor)
        .add(pin2, color=pincolor)
        .add(pin2a, color=pincolor)
        .add(button_mark, color=cq.Color('white'))
    )
    return assy

def main():
    obj = new()
    show_object(obj)
    obj.save('step_files/CW-SB21KKGF.step')

if __name__ == '__cq_main__':
    main()
