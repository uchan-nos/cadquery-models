'''
Copyright (c) 2024 Kota UCHIDA

Twin-motor Gearbox: Tamiya 楽しい工作シリーズ No.97 (Tamiya)
'''

import cadquery as cq
from common import *
from lib import obj

import fa130

def new_gearbox():
    m1_height = 22.8
    thickness = 2.0
    t_cylinder = (m1_height - 20.1)/2

    def make_filled_cover(length, t_plate, t_cylinder):
        return (
            cq.Workplane('XZ')
            .cylinder(length, 20.1/2 + t_cylinder)
            .cut(
                cq.Workplane('XZ')
                .box(10, 30, length, centered=(F, T, T))
                .translate((15.1/2 + t_plate, 0, 0))
            )
            .cut(
                cq.Workplane('XZ')
                .box(20, 30, length, centered=(F, T, T))
                .translate((-20, 0, 0))
            )
            .translate((15.1/2, length/2, 0))
        )

    to_cut_inner = make_filled_cover(8.8, 0, 0)

    def make_cbore_hole(wp, dir):
        return (
            wp
            .faces('>X')
            .workplane(origin=(0, -4.6, dir*(m1_height/2 - 6/2)))
            .cboreHole(SCREW_HOLE_INNER_D, 6, 1)
            .faces('>X')
            .workplane(origin=(0, -4.6, dir*(m1_height/2)))
            .rect(6, 6)
            .extrude(-1, combine='s')
        )

    m1_motor_screw_box = (
        cq.Workplane()
        .box(15.1/2 + thickness, 9.8, 20.1 + t_cylinder*2, centered=(F, T, T))
        .cut(
            cq.Workplane()
            .box(15.1/2, 9.8, m1_height - thickness*2, centered=(F, T, T))
        )
        .faces('<X[1]')
        .workplane(origin=(0, 0, 20.1/2 + t_cylinder - 6/2))
        .cylinder(15.1/2, 6/2, centered=(T, T, F))
        .faces('<X[1]')
        .workplane(origin=(0, 0, -(20.1/2 + t_cylinder - 6/2)))
        .cylinder(15.1/2, 6/2, centered=(T, T, F))
        .faces('>Y')
        .workplane(origin=(15.1/2, 0, 0), invert=T)
        .box(15.1/2, 10, thickness, centered=(F, T, F))
        .faces('>Y')
        .workplane(origin=(0, 0, 0))
        .hole(7)
        .translate((15.1/2, -9.8/2, 0))
    )

    m1_screw_tab = (
        cq.Workplane()
        .sketch()
        .segment((0, -13/2), (0, 13/2))
        .arc((5, 0), 3, 0, 360)
        .hull()
        .finalize()
        .extrude(thickness)
        .faces('>Z')
        .workplane(origin=(4.7, 0, 0))
        .hole(3.2)
        .translate((15.1/2 + 14.6 - thickness, -23.5, -m1_height/2))
    )

    m1_gearbox = (
        obj.bended_plate_2d(
            cq.Workplane('XY'),
            [
                (0, 0),
                (5, 8.2 - 11.3),
                (5, 11.3 - 47.5)
            ],
            thickness,
            fillet=0.1
        )
        .extrude(22.8/2, both=T)
        .translate((-thickness/2, 0, 0))
        .faces('<X[1]')
        .tag('plate_inner_face')
        .workplane(origin=(0, 0, m1_height/2 - thickness + 1/2), offset=7)
        .rect(13.5, 1, centered=(F, T))
        .extrude('next')
        .faces(tag='plate_inner_face')
        .workplane(origin=(0, -13.5, m1_height/2 - thickness + 1/2))
        .box(17, 1, 5, centered=(F, T, F))
        .translate((15.1 + thickness, -9.8 + thickness/2, 0))
        .faces('>X')
        .workplane(origin=(0, -41.5, 20 - m1_height/2), invert=T)
        .cylinder(9.5, 6/2, centered=(T, T, F))
        .faces('>X')
        .workplane(origin=(0, -41.5, 20 - m1_height/2))
        .hole(3.2)
        .faces('>X')
        .workplane(origin=(0, 0, 0), offset=-thickness)
        .pushPoints([(-41.5, -m1_height/2 + 4, 0), (-43.7, 0, 0)])
        .cylinder(7.5, 6/2)
        .faces('>X')
        .workplane(origin=(0, 0, 0))
        .pushPoints([(-41.5, -m1_height/2 + 4, 0), (-43.7, 0, 0)])
        .hole(3.5)
        .faces('>X[-2]')
        .workplane(origin=(0, -30, 0))
        .cylinder(4, 6/2)
        .faces('>X')
        .workplane(origin=(0, -30, 0))
        .hole(3.5)
    )

    cover_l = (
        make_filled_cover(8.8, thickness, t_cylinder)
        .cut(to_cut_inner)
        .add(m1_motor_screw_box)
    )
    cover_l = make_cbore_hole(cover_l, 1)
    cover_l = make_cbore_hole(cover_l, -1)

    cover_l = (
        cover_l
        .add(m1_gearbox)
        .add(m1_screw_tab)
    )

    gearbox_l = (
        cq.Workplane(origin=(15.1 + thickness - 3, 25.2, 0))
        .box(5, 2.4, 7.2, centered=(F, F, T))
        .edges('|Z and >Y and <X')
        .chamfer(1.5)
        .workplane(origin=(15.1 + thickness, 25.2 - (10.4 - thickness), 0))
        .box(thickness, 10.4, 7.2, centered=(F, F, T))
        .workplane(origin=(15.1, 0, 0))
        .box(thickness, 19.2, 11.8, centered=(F, F, T))
        .add(cover_l)
        .combine()
    )
    gearbox_r = gearbox_l.mirror('YZ')
    gearbox = (
        cq.Assembly()
        .add(gearbox_l, color=cq.Color('gray50'))
        .add(gearbox_r, color=cq.Color('gray50'))
    )
    return gearbox

def new():
    gearbox = new_gearbox()
    shaft = new_hex_shaft(50)

    motor_l = fa130.new()
    motor_r = fa130.new()
    motor_l_loc = cq.Location((15.1/2, 0, 0), ey, 90)
    motor_r_loc = cq.Location((-15.1/2, 0, 0), ey, -90)
    shaft_l_loc = cq.Location((1, -30, 0), ey, 90)
    shaft_r_loc = cq.Location((-1, -30, 0), ey, -90)
    assy = (
        cq.Assembly()
        .add(gearbox, color=cq.Color('gray50'))
        .add(motor_l, loc=motor_l_loc)
        .add(motor_r, loc=motor_r_loc)
        .add(shaft, loc=shaft_l_loc, color=cq.Color('lightgoldenrod3'))
        .add(shaft, loc=shaft_r_loc, color=cq.Color('lightgoldenrod3'))
    )
    return assy

def main():
    show_object(new())

if __name__ == '__cq_main__':
    main()
