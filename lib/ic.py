import cadquery as cq

def new_pin_smd(t, h, l, w):
    '''
    Create a pin

         |------ l -------|        |- w -|
                          |
          -------.p1      |         -----
    ---- |        `       |        |     |
      |   -----    \ p2            |     |
     h|      p4\    `-----  ----   |-----|
      |         \         |  |t    |     |
    ---------- p3`--------  ----    -----
    '''

    tilt_v = 0.05
    tilt_h = 0.05
    l2 = l/2
    t2 = t/2
    p1 = (l2 + t2 - tilt_v, h + t2)
    p2 = (l2 + t2 + tilt_v, t + tilt_h*(1 - t/(l2)))
    p3 = (l2 - t2 + tilt_v, tilt_h)
    p4 = (l2 - t2 - tilt_v, h - t2)
    pin = (
            cq.Workplane('XZ')
            .moveTo(0, h + t2)
            .lineTo(*p1)
            .lineTo(*p2)
            .lineTo(l, t)
            .lineTo(l - t*tilt_h/(l - p3[0]), 0)
            .lineTo(*p3)
            .lineTo(*p4)
            .lineTo(0, h - t2)
            .close()
            .extrude(w)
            .edges('|Y and >(1, 0, 2)')
            .fillet(t)
            .edges('|Y and <(1, 0, 2)')
            .fillet(t)
            .edges(cq.selectors.NearestToPointSelector((p2[0], -w/2, p2[1])))
            .fillet(t/5)
            .edges(cq.selectors.NearestToPointSelector((p4[0], -w/2, p4[1])))
            .fillet(t/5)
            .translate((0, w/2, 0))
            )
    return pin

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
