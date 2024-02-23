'''
Copyright (c) 2024 Kota UCHIDA

OS102011MA1QN1: Slide switch (C&K)
'''

import cadquery as cq
from lib import obj

def new():
    plate_t = 0.4
    right_plate = (
        cq.Workplane('YZ')
        .moveTo(-2.2, 0)
        .vLine(4.0)
        .hLine(4.4)
        .vLine(-4.0)
        .lineTo(1.2, 0)
        .threePointArc((0.8, 0.4), (0.4, 0))
        .lineTo(0.6, -1.4)
        .lineTo(0.4, -2.5)
        .threePointArc((0, -2.8), (-0.4, -2.5))
        .lineTo(-0.6, -1.4)
        .lineTo(-0.4, 0)
        .threePointArc((-0.8, 0.4), (-1.2, 0))
        .close()
        .extrude(-plate_t)
        .translate((8.6/2, 0, 0))
    )
    right_angle = (
        obj.bended_plate_2d(cq.Workplane('XZ'), [
            (0, 4.0),
            (0, 4.7 - plate_t/2),
            (plate_t/2 - 0.6, 4.7 - plate_t/2),
        ], plate_t, fillet=0.1)
        .extrude(4.4 - 2*0.5)
        .translate((8.6/2 - plate_t/2, (4.4 - 2*0.5)/2, 0))
    )

    left_plate = right_plate.mirror(mirrorPlane='YZ')
    left_angle = right_angle.mirror(mirrorPlane='YZ')

    main_plate_slit = (
        cq.Workplane()
        .box(4.2, 4, 3.8)
        .translate((0, -4.4/2, 3.6/2))
        .union(
            cq.Workplane()
            .box(5.2, 4.4, 1.6)
            .translate((0, 0, 1.6/2))
        )
    )

    main_plate_width = 8.6 - 0.6*2
    main_plate = (
        obj.bended_plate_2d(cq.Workplane('YZ'), [
            (-3.0/2, 0.3),
            (-4.4/2 + plate_t/2, 0.7),
            (-4.4/2 + plate_t/2, 4.7 - plate_t/2),
            (4.4/2 - plate_t/2, 4.7 - plate_t/2),
            (4.4/2 - plate_t/2, 0.7),
            (3.0/2, 0.3),
        ], plate_t, fillet=0.1)
        .extrude(main_plate_width)
        .translate((-main_plate_width/2, 0, 0))
        .cut(main_plate_slit)
        .union(right_angle)
        .union(right_plate)
        .union(left_angle)
        .union(left_plate)
    )

    knob_slit = (
        cq.Workplane()
        .box(0.9, 0.9, 2)
        .rotateAboutCenter((0, 0, 1), 45)
        .translate((0, -(4 + 1)/2, 0))
    )
    knob = (
        cq.Workplane()
        .box(2, 4 + 1, 2)
        .cut(knob_slit)
        .translate((1, (4 + 1)/2 - 4.4/2 - 4.0, 2.6))
        .faces('>Y').workplane(origin=(1, 0, 2.6 + 0.1))
        .box(1.8*2 + 2, 2.2, 1)
    )

    inner_pcb = (
        cq.Workplane()
        .box(8, 3.4, 0.9)
        .box(5, 4.4, 0.9)
        .translate((0, 0, 1.6 - 0.9/2))
    )

    pin = (
        cq.Workplane()
        .box(0.5, 0.3, 5)
        .translate((0, 0, 5/2 - 2.8))
    )
    pin1_loc = cq.Location((-2, 0, 0))
    pin3_loc = cq.Location((2, 0, 0))

    plate_color = cq.Color('lightgray')
    assy = (
        cq.Assembly('OS102011MA1QN1')
        .add(main_plate, color=plate_color)
        .add(knob, color=cq.Color('gray10'))
        .add(inner_pcb, color=cq.Color('tan3'))
        .add(pin, name='pin1', loc=pin1_loc, color=plate_color)
        .add(pin, name='pin2', color=plate_color)
        .add(pin, name='pin3', loc=pin3_loc, color=plate_color)
    )
    return assy

def main():
    obj = new()
    show_object(obj)
    obj.save('step_files/OS102011MA1QN1.step')

if __name__ == '__cq_main__':
    main()
