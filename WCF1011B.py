'''
Copyright (c) 2024 Kota UCHIDA

WCF1011B: AC outlet (Panasonic)
'''

import cadquery as cq
from lib import obj

CAP_W = 27
CAP_D = 21.5
CAP_H = 3.5
BODY_W = 23
BODY_D = 12
BODY_H = 20.3
PIN_L = 5.2
PIN_T = 0.8
PIN_W = 3.5
PIN_HOLE_L = 3
PIN_HOLE_W = 2

def new():
    cap = (
        cq.Workplane()
        .box(CAP_W, CAP_D, CAP_H, centered=(True, True, False))
        .edges('|Z')
        .fillet(2)
        .edges('>Z')
        .chamfer(1, 2)
    )
    cap_cut = (
        cap.faces('>Z').workplane()
        .box(9, 15, 0.2, combine=False)
        .edges('|Z and >X')
        .fillet(3)
        .edges('|Z and <X')
        .fillet(1.5)
        .translate((6, 0, 0))
    )
    cap = cap.cut(cap_cut)
    cap = cap.cut(cap_cut.mirror((1, 0, 0)))

    body = (
        cq.Workplane()
        .box(BODY_W, BODY_D, BODY_H)
        .edges('not >Z')
        .fillet(1)
        .translate((0, 0, -BODY_H/2))
        .add(cap)
    )

    plug_hole = (
        cq.Workplane()
        .box(2.2, 8.7, 18)
        .edges('|Z')
        .fillet(0.5)
        .translate((6.35, 0, 0))
    )

    body = body.cut(plug_hole)
    body = body.cut(plug_hole.mirror((1, 0, 0)))

    claw = (
        cq.Workplane('YZ')
        .vLine(-9)
        .lineTo(1, -10)
        .hLine(1)
        .lineTo(CAP_D/2 - BODY_D/2, -2)
        .lineTo(18.5/2 - BODY_D/2, 0)
        .lineTo(1.5, -8)
        .hLine(-0.5)
        .vLine(8)
        .close()
        .extrude(4)
        .translate((25/2 - 4, BODY_D/2, 0))
    )
    claw.add(claw.mirror((1, 0, 0)))
    claw.add(claw.mirror((0, 1, 0)))

    body.add(claw)

    pin_hole_l = PIN_HOLE_L - PIN_HOLE_W
    pin_hole = (
        cq.Workplane('YZ')
        .moveTo(-PIN_HOLE_W/2, 0)
        .threePointArc((0, PIN_HOLE_W/2), (PIN_HOLE_W/2, 0))
        .vLine(-pin_hole_l)
        .threePointArc((0, -pin_hole_l - PIN_HOLE_W/2), (-PIN_HOLE_W/2, -pin_hole_l))
        .close()
        .extrude(2, both=True)
        .translate((0, 0, -2.5))
    )

    pin_2d = obj.bended_plate_2d(
        cq.Workplane('XZ'),
        [
            (0, 10),
            (0, -1.5),
            (0.5, -2.5),
            (0.5, -3.5),
            (0, -4.5),
            (0, -PIN_L)
        ],
        PIN_T,
        fillet=1
    )
    pin = (
        pin_2d
        .extrude(PIN_W/2, both=True)
        .edges('|X and <Z')
        .fillet(PIN_W/2 - 0.01)
        .cut(pin_hole)
        .translate((18.8/2 - 0.5 - PIN_T/2, 0, -BODY_H))
    )
    pin.add(pin.mirror((1, 0, 0)))

    assy = (
        cq.Assembly()
        .add(body, color=cq.Color('gray10'))
        .add(pin, color=cq.Color('lightgray'))
    )

    return assy

def main():
    obj = new()
    show_object(obj)
    obj.save('step_files/WCF1011B.step', mode='fused')

if __name__ == '__cq_main__':
    main()
