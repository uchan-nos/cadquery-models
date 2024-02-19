import cadquery as cq
from lib import obj

def new_pin_smd(t, h, l, w):
    '''
    Create a pin

         |------ l -------|        |- w -|
                          |
          -------.        |         -----
    ---- |        `       |        |     |
      |   -----    \               |     |
     h|        \    `-----  ----   |-----|
      |         \         |  |t    |     |
    -----------  `--------  ----    -----
    '''

    tilt_v = h/10.0
    tilt_h = l/30.0
    l2 = l/2
    t2 = t/2
    return obj.bended_board_2d(cq.Workplane('XZ'), [
        (0, h),
        (l2 - tilt_v, h),
        (l2 + tilt_v, t2 + tilt_h),
        (l, t2)
    ], t).extrude(w).translate((0, w/2, 0))

def new_tssop(num_pins):
    body_t = 1.0
    body_w = 4.4
    body_l = 6.5

    body = (
            cq.Workplane()
            .box(body_w, body_l, 0.2)
            .faces('<Z')
            .rect(body_w, body_l)
            .workplane(offset=(body_t - 0.2)/2)
            .rect(body_w - 0.2, body_l - 0.2)
            .loft()
            .faces('>Z')
            .rect(body_w, body_l)
            .workplane(offset=(body_t - 0.2)/2)
            .rect(body_w - 0.2, body_l - 0.2)
            .loft()
            .translate((0, 0, body_t/2 + 0.1))
            )
    body = body.faces('>Z').workplane().center(-body_w/2 + 1, body_l/2 - 1).hole(0.8, 0.1)

    body_center_z = body_t/2 + 0.1
    pin_t = 0.15
    pin = new_pin_smd(pin_t, body_center_z, 1, 0.25)

    result = (
            cq.Assembly()
            .add(body, color=cq.Color('gray10'))
            )

    for i in range(int(num_pins/2)):
        loc_pin = cq.Location((body_w/2, body_l/2 - 0.65*i - 0.65/2, 0))
        loc_pin_mirror = cq.Location((-body_w/2, body_l/2 - 0.65*i - 0.65/2, 0), (0, 0, 1), 180)
        result.add(pin, loc=loc_pin, color=cq.Color('gray'))
        result.add(pin, loc=loc_pin_mirror, color=cq.Color('gray'))

    return result

def new_qfn(num_pins, width, pitch, mark1='hole'):
    num_pins_4 = int(num_pins/4)
    t = 0.7
    pin_t = 0.2
    pin_w = pitch/2
    pin_l = pitch/1.25
    pins = (
            cq.Workplane()
            .rarray(pitch, width - pin_l, num_pins_4, 2)
            .box(pin_w, pin_l, pin_t)
            .rarray(width - pin_l, pitch, 2, num_pins_4)
            .box(pin_l, pin_w, pin_t)
            .translate((0, 0, pin_t/2))
            )
    gnd = (
            cq.Workplane()
            .box(width - pin_l*4, width - pin_l*4, pin_t)
            .edges('>(-1, 1, 0)').chamfer(pin_l)
            .translate((0, 0, pin_t/2))
            )
    body = (
            cq.Workplane()
            .box(width, width, t)
            .translate((0, 0, t/2))
            .cut(pins).cut(gnd)
            )

    result = (
            cq.Assembly()
            .add(pins, color=cq.Color('gray'))
            .add(gnd, color=cq.Color('gray'))
            )

    mark1_pos = width/2 - width/8
    mark1_plane = body.faces('>Z').workplane().center(-mark1_pos, mark1_pos)
    if mark1 == 'white':
        mark1_obj = mark1_plane.cylinder(0.1, width/30, combine=False)
        body = body.cut(mark1_obj)
        result.add(mark1_obj, color=cq.Color('white'))
    elif mark1 == 'hole':
        body = mark1_plane.hole(width/10, 0.1)
    result.add(body, color=cq.Color('gray10'))

    return result
