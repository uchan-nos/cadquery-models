'''
Copyright (c) 2025 Kota UCHIDA

SSR21H: Common mode choke coil (Tokin)
'''

import cadquery as cq

BODY_W = 22
BODY_D = 22
BOBBIN_D = 14
PIN_L = 3.5
PIN_D = 0.8
PIN_PITCH_X = 10
PIN_PITCH_Y = 18.5

def new(color=cq.Color('lightgray')):
    center_xy = (True, True, False)

    base_h = 4.4
    leg_len = base_h - 2.7
    base_t = 3.5

    base = (
        cq.Workplane()
        .box(BODY_W, BODY_D, 2.7)
        .cut(
            cq.Workplane()
            .box(BODY_W - 2*base_t, BODY_D - 2*base_t, 2.7)
        )
        .translate((0, 0, 2.7/2 + leg_len))
        .faces('<Z')
        .workplane(offset=leg_len/2)
        .rect(BODY_W - 2.8, BODY_D - 3.5, forConstruction=True)
        .vertices()
        .box(2.8, 3.5, leg_len)
        .rarray(1, BODY_D - 3.5, 1, 2)
        .box(3.5, 3.5, leg_len)
    )

    core_h = 7.5
    core_depress_h = 5.7
    core_t = 2.5
    core_side_l = (
        cq.Workplane('YZ')
        .move(-BODY_D/2 + core_t, 0)
        .vLine(core_h)
        .lineTo(-BODY_D/2 + 9.5, core_depress_h)
        .lineTo(BODY_D/2 - 9.5, core_depress_h)
        .lineTo(BODY_D/2 - core_t, core_h)
        .vLine(-core_h)
        .close()
        .extrude(core_t)
        .translate((-BODY_W/2, 0, base_h))
    )
    core_side_r = core_side_l.mirror('YZ')
    core = (
        cq.Workplane()
        .rarray(1, BODY_D - core_t, 1, 2)
        .box(BODY_W, core_t, core_h)
        .translate((0, 0, base_h + core_h/2))
        .union(core_side_l)
        .union(core_side_r)
    )

    bobbin = (
        cq.Workplane('YZ')
        .cylinder(2, BOBBIN_D/2, centered=center_xy)
        .faces('>X')
        .workplane()
        .cylinder(4, 1, centered=center_xy)
        .faces('>X')
        .workplane()
        .cylinder(4, BOBBIN_D/2, centered=center_xy)
        .faces('>X')
        .workplane()
        .cylinder(4, 1, centered=center_xy)
        .faces('>X')
        .workplane()
        .cylinder(2, BOBBIN_D/2, centered=center_xy)
        .translate((-16/2, 0, BOBBIN_D/2))
    )

    coil = (
        cq.Workplane('YZ')
        .cylinder(4, BOBBIN_D/2 - 0.5)
        .translate((-4, 0, BOBBIN_D/2))
    )
    coil = coil.add(coil.mirror('YZ'))

    pin1 = (
        cq.Workplane()
        .cylinder(PIN_L + base_h, PIN_D/2, centered=center_xy)
        .translate((-PIN_PITCH_X/2, PIN_PITCH_Y/2, -PIN_L))
    )
    pin12 = pin1.union(pin1.mirror('XZ'))
    pins = pin12.union(pin12.mirror('YZ'))

    assy = (
        cq.Assembly(name='SSR21H')
        .add(base, name='base', color=cq.Color('gray10'))
        .add(core, name='core', color=cq.Color('gray30'))
        .add(bobbin, name='bobbin', color=cq.Color('gray10'))
        .add(coil, name='coil', color=cq.Color('orange2'))
        .add(pins, name='pins', color=cq.Color('gray90'))
    )

    return assy

def main():
    obj = new()
    show_object(obj)
    obj.save('step_files/SSR21H.step')

if __name__ == '__cq_main__':
    main()
