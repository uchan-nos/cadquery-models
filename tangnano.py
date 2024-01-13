import cadquery as cq
import pin_header

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

    plate_face = cq.Workplane().rect(PLATE_L, PLATE_W)
    plate_face = plate_face.pushPoints(pin_pos + pad_pos).circle(PAD_OUTER_R)
    plate = plate_face.extrude(PLATE_THICKNESS).edges('|Z').fillet(1)

    pin = pin_header.new()
    pad = (
            cq.Workplane()
            .cylinder(PLATE_THICKNESS + 0.1, 0.8)
            .faces('>Z').hole(PAD_INNER_R*2)
            )

    tn = cq.Assembly().add(plate, color=cq.Color('gray60'))
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

    return tn

def main():
    obj = new()
    show_object(obj)
    obj.save('step_files/TangNano.step')

if __name__ == '__cq_main__':
    main()
