import cadquery as cq
import pin_header

PLATE_L = 58.34
PLATE_W = 21.29
PLATE_THICKNESS = 1.6
PIN_WIDTH = 17.78
HOLE_R = 0.6
SWITCH_HEIGHT = 2

def new():
    pin_offset_x = -PLATE_L/2 + 2.54

    plate_face = cq.Workplane().rect(PLATE_L, PLATE_W)
    plate_face = plate_face.pushPoints(
            [(20 * 2.54 + pin_offset_x, y)
                for y in (-PIN_WIDTH/2 + 2.54, PIN_WIDTH/2 - 2.54)] +
            [(xi * 2.54 + pin_offset_x, y)
                for y in (-PIN_WIDTH/2, PIN_WIDTH/2)
                for xi in range(0, 21)])
    plate_face = plate_face.circle(HOLE_R)
    plate = plate_face.extrude(PLATE_THICKNESS).edges('|Z').fillet(1)

    pin = pin_header.new()
    pad = cq.Workplane().cylinder(0.03, 0.8).faces('>Z').hole(HOLE_R*2)

    tn = cq.Assembly().add(plate, color=cq.Color('gray60'))
    for yi in range(2):
        y = (yi - 0.5) * PIN_WIDTH
        for xi in range(0, 21):
            x = xi * 2.54 + pin_offset_x
            loc_pin = cq.Location((x, y, 0), (1, 0, 0), 180)
            loc_pad = cq.Location((x, y, PLATE_THICKNESS))
            tn.add(pin, name=f'pin{yi}.{xi}', loc=loc_pin)
            tn.add(pad, name=f'pad{yi}.{xi}', loc=loc_pad, color=cq.Color('gold'))

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
    show_object(new())

if __name__ == '__cq_main__':
    main()
