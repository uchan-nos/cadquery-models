'''
Copyright (c) 2024 Kota UCHIDA

MJ-074N: Stereo Mini Jack (Marushin electric)
'''

import cadquery as cq
from lib.cq_gears import cq_gears

NUT_M = 6
NUT_BODY_GAP = 0.7
SCREW_L = 4.5
BODY_L = 11.7
BODY_METAL_L = 5.5
BODY_D = 8
SIGPIN_L = 3
GNDPIN_L = 6.1
PIN_T = 0.3
PIN_W = 2

def new(plate_t=1):
    centering_xy = (True, True, False)

    body_metal = (
        cq.Workplane()
        .cylinder(BODY_METAL_L, BODY_D/2, centered=centering_xy)
        .translate((0, 0, -BODY_METAL_L))
        .faces('>Z')
        .workplane()
        .cylinder(NUT_BODY_GAP, NUT_M/2 - 0.5, centered=centering_xy)
        .faces('>Z')
        .workplane()
        .cylinder(SCREW_L - NUT_BODY_GAP, NUT_M/2, centered=centering_xy)
        .faces('>Z')
        .hole(3.6)
    )
    body_pla = (
        cq.Workplane()
        .cylinder(BODY_L - BODY_METAL_L, BODY_D/2, centered=centering_xy)
        .translate((0, 0, -BODY_L))
    )

    fixing_nut_w = 2
    fixing_nut = (
        cq.Workplane()
        .gear(
            cq_gears.SpurGear(
                module=(BODY_D - 0.2)/30,
                teeth_number=30,
                width=fixing_nut_w,
                pressure_angle=45,
                addendum_coeff=0.5,
                dedendum_coeff=0.5,
                bore_d=NUT_M,
                chamfer=0.2
            )
        )
        .translate((0, 0, plate_t))
    )

    sigpin_r = (
        cq.Workplane()
        .box(PIN_T, PIN_W, SIGPIN_L, centered=centering_xy)
        .edges('|X and <Z')
        .fillet(0.4)
        .faces('>X')
        .workplane(origin=(0, 0, 0.8))
        .hole(0.8)
        .translate((2.54, 0, -SIGPIN_L - BODY_L))
    )
    sigpin_l = sigpin_r.mirror('YZ')

    gndpin = (
        cq.Workplane()
        .box(PIN_W, PIN_T, GNDPIN_L, centered=centering_xy)
        .faces('>Y')
        .workplane(origin=(0, 0, 1))
        .hole(0.8)
        .translate((0, 2.8, -GNDPIN_L - BODY_L))
    )

    pla_color = cq.Color('gray20')
    metal_color = cq.Color('gray90')
    pin_color = cq.Color('lightgoldenrod1')
    assy = (
            cq.Assembly()
            .add(body_metal, color=metal_color)
            .add(body_pla, color=pla_color)
            .add(sigpin_r, color=pin_color)
            .add(sigpin_l, color=pin_color)
            .add(gndpin, color=metal_color)
            .add(fixing_nut, color=metal_color)
            )
    return assy

def main():
    obj = new()
    show_object(obj)
    obj.save('step_files/MJ-074N.step')

if __name__ == '__cq_main__':
    main()
