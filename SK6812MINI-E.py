'''
Copyright (c) 2024 Kota UCHIDA

SK6812MINI-E: RGBLED with MCU (OPSCO Optoelectronics)
'''

import cadquery as cq

pin_t = 0.2

def new():
    pin = (
        cq.Workplane()
        .box(1.34, 0.68, pin_t, centered=(True, True, False))
        .translate((0, 0, -pin_t))
    )
    pin_x = (3.2 + 1.34)/2
    pin_y = (0.68 + 0.82)/2
    pin1_loc = cq.Location((-pin_x,  pin_y, 0))
    pin2_loc = cq.Location((-pin_x, -pin_y, 0))
    pin3_loc = cq.Location(( pin_x, -pin_y, 0))
    pin4_loc = cq.Location(( pin_x,  pin_y, 0))

    pin3 = pin.edges('|Z and >X and <Y').chamfer(0.3)

    body_chamfer = (
        cq.Workplane()
        .transformed(rotate=(0, 0, 45), offset=(3.2 - 0.85, -(2.8 - 0.85), 0.5))
        .box(3, 3, 3, centered=(True, True, False))
    )
    led_hole = (
        cq.Solid.makeCone(1.3, 1.0, 0.5, pnt=(0, 0, 0.84), dir=(0, 0, -1))
    )
    body_top = (
        cq.Workplane()
        .box(3.2, 2.8, 0.84 + pin_t, centered=(True, True, False))
        .translate((0, 0, -pin_t))
        .cut(body_chamfer)
        .cut(led_hole)
    )
    body_bottom = (
        cq.Workplane()
        .rect(3.2, 2.8)
        .extrude(-(1.78 - 0.84 - pin_t), taper=10)
        .translate((0, 0, -pin_t))
    )
    result = (
        cq.Assembly()
        .add(body_top, color=cq.Color('white'))
        .add(body_bottom, color=cq.Color('white'))
        .add(pin,  loc=pin1_loc, color=cq.Color('gray60'))
        .add(pin,  loc=pin2_loc, color=cq.Color('gray60'))
        .add(pin3, loc=pin3_loc, color=cq.Color('gray60'))
        .add(pin,  loc=pin4_loc, color=cq.Color('gray60'))
    )
    return result

def main():
    obj = new()
    show_object(obj)
    obj.save('step_files/SK6812MINI-E.step')

if __name__ == '__cq_main__':
    main()
