import cadquery as cq
import pin_header
import gw1n_qn48
from lib import ic

PLATE_L = 58.34
PLATE_W = 21.29
PLATE_THICKNESS = 1.6
PIN_WIDTH = 17.78
PAD_INNER_R = 0.6
PAD_OUTER_R = 0.8
SWITCH_HEIGHT = 2

def new():
    pin_offset_x = -PLATE_L/2 + 2.54

    pin_pos = [(xi * 2.54 + pin_offset_x, sign * PIN_WIDTH/2)
            for sign in (-1, 1) for xi in range(0, 20)]
    pad_pos = [(20 * 2.54 + pin_offset_x, sign * (PIN_WIDTH/2 - off))
            for sign in (-1, 1) for off in (0, 2.54)]

    plate2d = (
            cq.Workplane().sketch()
            .rect(PLATE_L, PLATE_W).vertices().fillet(1)
            .push(pin_pos + pad_pos).circle(PAD_OUTER_R, mode='s')
            .finalize()
            )
    plate = plate2d.extrude(PLATE_THICKNESS)
    surface_back = plate2d.extrude(-0.01)
    surface_front = surface_back.mirror('XY', (0, 0, PLATE_THICKNESS/2))

    name_text = (
            surface_front.faces('>Z').workplane()
            .text('Tang Nano', 2.5, 0.01, cut=False, font='Eras Bold ITC')
            .translate((18.3 - PLATE_L/2, PLATE_W/2 - 9, 0))
            )

    tn = (
            cq.Assembly()
            .add(plate, color=cq.Color('gray80'))
            .add(surface_front, color=cq.Color('gray20'))
            .add(surface_back, color=cq.Color('gray20'))
            .add(name_text, color=cq.Color('white'))
            )

    pin = pin_header.new()
    pad = (
            cq.Workplane()
            .cylinder(PLATE_THICKNESS + 0.1, 0.8)
            .faces('>Z').hole(PAD_INNER_R*2)
            )

    for pos in pin_pos:
        loc_pin = cq.Location((pos[0], pos[1], 0), (1, 0, 0), 180)
        tn.add(pin, name=f'pin{pos}', loc=loc_pin)
    for pos in pin_pos + pad_pos:
        loc_pad = cq.Location((pos[0], pos[1], PLATE_THICKNESS/2))
        tn.add(pad, name=f'pad{pos}', loc=loc_pad, color=cq.Color('gold'))

    btn = (
            cq.Workplane()
            .moveTo(1, 0.5)
            .threePointArc((0, 1.5), (-1, 0.5))
            .vLine(-1)
            .threePointArc((0, -1.5), (1, -0.5))
            .close()
            .extrude(0.5)
            )
    switch_body = (
            cq.Workplane()
            .box(3, 4, SWITCH_HEIGHT)
            )
    switch = (
            cq.Assembly()
            .add(btn, loc=cq.Location((0, 0, 2/2)), color=cq.Color('white'))
            .add(switch_body, color=cq.Color('gray'))
            )

    switch_z = PLATE_THICKNESS + SWITCH_HEIGHT/2
    loc_a = cq.Location((PLATE_L/2 - 2, PIN_WIDTH/2 - 1, switch_z))
    loc_b = cq.Location((PLATE_L/2 - 2, 1 - PIN_WIDTH/2, switch_z))
    tn.add(switch, name='sw-a', loc=loc_a)
    tn.add(switch, name='sw-b', loc=loc_b)

    ch552t = ic.new_tssop(20)
    loc_ch552t = cq.Location((17.5, 0, PLATE_THICKNESS), (0, 0, 1), 90)
    tn.add(ch552t, loc=loc_ch552t)

    gw1n = gw1n_qn48.new()
    loc_gw1n = cq.Location((3, -0.5, PLATE_THICKNESS), (0, 0, 1), 90)
    tn.add(gw1n, loc=loc_gw1n)

    return tn

def main():
    obj = new()
    show_object(obj)
    obj.save('step_files/TangNano.step')

if __name__ == '__cq_main__':
    main()
