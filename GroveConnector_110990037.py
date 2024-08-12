'''
Copyright (c) 2024 Kota UCHIDA

110990037: Grove Connector (Seeed Studio)
'''

import cadquery as cq
from lib import obj

def new():
    t = 0.75
    bottom_slit = (
        cq.Workplane()
        .box(1.2, 1.2, t)
    )
    bottom_slits = cq.Workplane()
    for i in range(0, 4):
        bottom_slits = bottom_slits.add(bottom_slit.translate((2*i, 0, 0)))

    bottom_plate = (
        cq.Workplane()
        .box(10, 8, t)
        .translate((1 + 2, 8/2 - 1.2/2, 0))
        .cut(bottom_slits)
    )

    pin = obj.bended_plate_2d(
        cq.Workplane('YZ'),
        [
            (0, -3.1),
            (0, 2.5),
            (5, 2.5)
        ],
        0.64
    ).extrude(0.64/2, both=True)
    pins = cq.Workplane()
    for i in range(0, 4):
        pins = pins.add(pin.translate((2*i, 0, 0)))

    assy = (
        cq.Assembly()
        .add(bottom_plate, color=cq.Color('white'))
        .add(pins, color=cq.Color('gray80'))
    )
    return assy

def main():
    obj = new()
    show_object(obj)

if __name__ == '__cq_main__':
    main()
