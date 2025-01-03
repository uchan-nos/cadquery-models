'''
Copyright (c) 2025 Kota UCHIDA

FH-P20H: Fuse holder (ELPA)
'''

import cadquery as cq

from lib import obj
import hexnut

NUT_M = 13
NUT_SIZE = 16
NUT_T = 5.1
NUT_SEAT_D = 18.5
NUT_SEAT_T = 1.3

WASHER_D = 16.6
WASHER_T = 1.5

BODY_L = 20
BODY_FACE_D = 15.1
BODY_FACE_T = 3
BODY_BOTTOM_D = 9
BODY_BOTTOM_L = 10

PIN_T = 0.8
PIN1_W = 3.9
PIN1_L = 5.4
PIN2_W = 4
PIN2_L = 6.3

def new(plate_t=1):
    center_xy = (True, True, False)

    fixing_nut = (
        hexnut.new_with_seat(NUT_M, NUT_SIZE, NUT_T, NUT_SEAT_D, NUT_SEAT_T, fillet_side='top')
        .rotate((0, 0, 0), (1, 0, 0), 180)
        .translate((0, 0, -plate_t - WASHER_T))
    )

    washer = (
        cq.Workplane()
        .cylinder(WASHER_T, WASHER_D/2)
        .cut(
            cq.Workplane()
            .cylinder(WASHER_T, NUT_M/2)
        )
        .translate((0, 0, -WASHER_T/2 - plate_t))
    )

    body = (
        cq.Workplane()
        .cylinder(BODY_FACE_T, BODY_FACE_D/2, centered=center_xy)
        .faces('>Z')
        .workplane()
        .hole(11)
        .faces('<Z')
        .workplane()
        .cylinder(BODY_L - BODY_BOTTOM_L, NUT_M/2, centered=center_xy)
        .faces('<Z')
        .workplane()
        .cylinder(BODY_BOTTOM_L, BODY_BOTTOM_D/2, centered=center_xy)
        .faces('>Z')
        .workplane()
        .hole(7.5, 19)
    )

    cap = (
        cq.Workplane()
        .cylinder(1.2, BODY_FACE_D/2, centered=center_xy)
        .union(
            cq.Solid.makeCone(13.9/2, 12.2/2, 5)
        )
        .translate((0, 0, BODY_FACE_T))
    )

    pin1 = (
        cq.Workplane()
        .box(PIN1_W, PIN_T, PIN1_L, centered=center_xy)
        .edges('|Y and <Z')
        .fillet(PIN1_W/2 - 0.01)
        .faces('<Y')
        .workplane(origin=(0, 0, 2))
        .hole(2)
        .translate((0, 0, -PIN1_L - BODY_L))
    )

    pin2 = (
        obj.bended_plate_2d(
            cq.Workplane('YZ'),
            [
                (0, 0),
                (2.2, 0),
                (PIN2_L, 2.2)
            ],
            PIN_T
        )
        .extrude(PIN2_W/2, both=True)
        .edges('>>Y[-2]')
        .fillet(PIN2_W/2 - 0.01)
        .rotate((0, 0, 0), (1, 0, 0), -90)
        .translate((0, BODY_BOTTOM_D/2, -(BODY_L - BODY_BOTTOM_L)))
    )

    assy = (
        cq.Assembly(name='FH-P20H')
        .add(fixing_nut, name='fixing_nut', color=cq.Color('gray10'))
        .add(washer, name='washer', color=cq.Color('white'))
        .add(body, name='body', color=cq.Color('gray10'))
        .add(cap, name='cap', color=cq.Color('gray10'))
        .add(pin1, name='pin1', color=cq.Color('gray90'))
        .add(pin2, name='pin2', color=cq.Color('gray90'))
    )

    return assy

def main():
    obj = new()
    show_object(obj)
    obj.save('step_files/FH-P20H.step')

if __name__ == '__cq_main__':
    main()
