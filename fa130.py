'''
Copyright (c) 2024 Kota UCHIDA

FA-130: Small DC Motor (Mabuchi Motor)
https://www.mabuchi-motor.co.jp/motorize/branch/motor/pdf/fa_130ra.pdf
'''

import cadquery as cq

ey = cq.Vector(0, 1, 0)

def new_metal_body():
    body_cut = (
        cq.Workplane()
        .box(20, 20, 10, centered=(True, False, True))
    )
    d_cut = (
        cq.Workplane()
        .box(10, 5 + 2.3, 1, centered=(True, False, False))
        .translate((0, 20, -1 - 4))
    )
    body = (
        cq.Workplane('XZ')
        .transformed(offset=(0, 0, -20))
        .cylinder(20, 20.1/2, centered=(True, True, False))
        .edges('<Y')
        .fillet(2)
        .cut(body_cut.translate((0, 0, -5 - 15.1/2)))
        .cut(body_cut.translate((0, 0, 5 + 15.1/2)))
        .faces('<Y')
        .tag('front')
        .cylinder(1.7, 6.15/2, centered=(True, True, False))
        .faces('<Y')
        .circle(5/2)
        .extrude(-0.5, combine='s')
        .faces(tag='front')
        .cylinder(9.4, 2/2, centered=(True, True, False))
        .edges('<Y')
        .fillet(0.5)
        .faces('>Y')
        .workplane()
        .cylinder(5 + 2.3, 10/2, centered=(True, True, False))
        .cut(d_cut)
        .edges('>Y')
        .chamfer(0.5)
        .faces('>Y')
        .cylinder(1.3, 2/2, centered=(True, True, False))
        .edges('>Y')
        .chamfer(0.3)
    )
    return body

def new_pla_cap():
    body_cut = (
        cq.Workplane()
        .box(20, 25, 10, centered=(True, False, True))
    )
    cap = (
        cq.Workplane('XZ')
        .transformed(offset=(0, 0, -25))
        .cylinder(5, 20.1/2, centered=(True, True, False))
        .cut(body_cut.translate((0, 0, -5 - 15.1/2)))
        .cut(body_cut.translate((0, 0, 5 + 15.1/2)))
        .faces('>Z')
        .box(8.5, 1.4, 5, centered=(True, False, True))
        .edges('|Y and >Z')
        .fillet(1.3)
        .edges('>Y')
        .chamfer(1)
    )
    return cap

def new_pins():
    rot_point = cq.Vector(-4/2, 0, 0)
    pin_l = (
        cq.Workplane()
        .box(4, 2, 0.1)
        .cut(
            cq.Workplane()
            .box(2, 1, 0.1)
        )
        .rotate(rot_point, rot_point + ey, -20)
        .translate((8.5/2 + 2, 25 - 3.4, 15.1/2))
    )
    pin_r = pin_l.mirror('YZ')
    pins = (
        cq.Assembly()
        .add(pin_l, color=cq.Color('gold'))
        .add(pin_r, color=cq.Color('gold'))
    )
    return pins

def new():
    metal_body = new_metal_body()
    pla_cap = new_pla_cap()
    pins = new_pins()
    assy = (
        cq.Assembly()
        .add(metal_body, color=cq.Color('gray80'))
        .add(pla_cap, color=cq.Color('blue'))
        .add(pins)
    )
    return assy

def main():
    show_object(new())

if __name__ == '__cq_main__':
    main()
