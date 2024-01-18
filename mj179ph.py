'''
Copyright (c) 2024 Kota UCHIDA

MJ179PH: DC Barrel Jack 2.1mm (Marushin electric)
'''

import cadquery as cq
from lib import obj

def new():
    hole = (
            cq.Workplane('XZ', origin=((0, 10/2, 6.5)))
            .cylinder(10, 6/2)
            )

    inner_dome = (
            cq.Workplane('XZ', origin=((0, 13.5 - 1.5, 0)))
            .moveTo(3, 1)
            .lineTo(3, 6.5)
            .threePointArc((0, 9.5), (-3, 6.5))
            .lineTo(-3, 1)
            .close()
            .extrude(13.5 - 1.5*2)
            )

    front = (
            cq.Workplane('XY')
            .box(9, 3.5, 11)
            .translate((0, 3.5/2, 11/2))
            .cut(hole)
            .cut(inner_dome)
            )

    back = (
            cq.Workplane('XY', origin=(0, 13.5, 2))
            .rarray(6, 1, 2, 1)
            .box(3, 2, 4)
            )

    back_cut = (
            cq.Workplane(origin=(0, 14.5 - 2.5/2, 0))
            .rarray(9, 1, 2, 1)
            .box(0.6, 2.5, 20)
            )

    pin_plus_t = 0.4
    pin_plus_wp = cq.Workplane('XZ', origin=(0, 13.5 + pin_plus_t/2, 6.5))
    pin_plus_hlen = 9/2 - 0.5
    pin_plus = (
            pin_plus_wp
            .cylinder(pin_plus_t, 2)
            .cylinder(pin_plus_t + 0.2, 1)
            .pushPoints([(0, -10/2, 0)])
            .box(3, 10, pin_plus_t)
            )
    pin_plus = obj.bended_board_2d(pin_plus.transformed((90, 0, 0), (0, 2.5/2, 0)), [
            (0, 0),
            (pin_plus_hlen, 0),
            (pin_plus_hlen, 1.7)
        ], pin_plus_t).extrude(2.5)

    dome = (
            cq.Workplane('XZ', origin=((0, 13.5, 0)))
            .moveTo(4.5, 0)
            .lineTo(4.5, 6.5)
            .threePointArc((0, 10.5), (-4.5, 6.5))
            .lineTo(-4.5, 0)
            .close()
            .extrude(13.5 - 3.5)
            .union(back)
            .cut(inner_dome)
            .cut(back_cut)
            .cut(pin_plus)
            )

    cn_plus = (
            cq.Workplane('XZ', origin=((0, 14, 6.5)))
            .circle(1.95/2)
            .extrude(14 - 1.2)
            .faces('<Y').fillet(1.95/2)
            )

    cn_t = 0.25
    cn_gnd = obj.bended_board_2d(cq.Workplane('YZ', origin=(-4/2, 0, 0)),
            [
                (7.5 + cn_t/2, 1 + cn_t/2),
                (1.2 + cn_t/2, 1 + cn_t/2),
                (1.2 + cn_t/2, 2.5),
                (4, 4.5),
                (9.2, 3.5),
                (10.5, 3.8)
            ], cn_t).extrude(4)

    pin_gnd = (
            cq.Workplane('XY', origin=(0, 7.5 + cn_t/2, (1 - 3.5)/2))
            .box(2.5, cn_t, 3.5 + 1)
            )

    cn_fix = obj.bended_board_2d(cq.Workplane('XZ', origin=(0, 9.5, 0)),
            [
                (-2, 3.8 + (pin_plus_t + cn_t)/2),
                (4.7 + pin_plus_t/2, 3.8 + (pin_plus_t + cn_t)/2),
                (4.7 + pin_plus_t/2, -3.5)
            ], pin_plus_t).extrude(-2.5)

    body_color = cq.Color('gray20')
    metal_color = cq.Color('lightgoldenrod1')
    result = (
            cq.Assembly()
            .add(front, color=body_color)
            .add(dome, color=body_color)
            .add(cn_plus, color=metal_color)
            .add(pin_plus, color=metal_color)
            .add(cn_gnd, color=metal_color)
            .add(pin_gnd, color=metal_color)
            .add(cn_fix, color=metal_color)
            )
    return result

def main():
    obj = new()
    show_object(obj)
    obj.save('step_files/MJ-179PH.step')

if __name__ == '__cq_main__':
    main()
