'''
Copyright (c) 2024 Kota UCHIDA

110990037: Grove Connector (Seeed Studio)
'''

import cadquery as cq
from lib import obj

PIN_PITCH = 2   # ピンピッチ
PIN_WIDTH = 0.5 # ピンの幅

WIDTH = 10 # 本体の幅（X）
DEPTH = 8  # 本体の奥行（Y）
HEIGHT = 5 # 本体の厚み（Z）
PIN_SLIT_DEPTH = 0.8
PIN_SLIT_WIDTH = 0.8
PLATE_T = 0.6
TOP_OFFSET = 0.9
BACK_T = 2.0
TOP_FRAME_D = 1.2
TOP_SLIT_DEPTH = 3
SIDE_COVER_WIDTH = 1.6

def new():
    pin_slit = (
        cq.Workplane()
        .box(PIN_SLIT_WIDTH, PIN_SLIT_DEPTH, HEIGHT, centered=(True, False, False))
    )
    pin_slits = cq.Workplane()
    for i in range(0, 4):
        pin_slits.add(pin_slit.translate((PIN_PITCH*i, 0, 0)))

    side_cover_r = (
        cq.Workplane('XZ')
        .moveTo(WIDTH/2, HEIGHT)
        .hLine(-0.4 - PLATE_T*2)
        .vLine(-TOP_OFFSET)
        .hLine(-0.4)
        .vLine(-PLATE_T)
        .hLine(0.4 + PLATE_T)
        .vLine(TOP_OFFSET)
        .hLine(0.4 + PLATE_T)
        .close()
        .extrude(DEPTH - TOP_FRAME_D)
        .translate((0, DEPTH, 0))
    )
    side_plate_r = (
        cq.Workplane()
        .box(PLATE_T, DEPTH - BACK_T, HEIGHT, centered=(True, False, False))
        .add(
            cq.Workplane()
            .box(SIDE_COVER_WIDTH, BACK_T - TOP_FRAME_D, TOP_OFFSET, centered=False)
            .translate((PLATE_T/2 - SIDE_COVER_WIDTH, TOP_FRAME_D - BACK_T, HEIGHT - TOP_OFFSET))
        )
        .translate((WIDTH/2 - PLATE_T/2, BACK_T, 0))
        .add(side_cover_r)
    )
    side_plate_l = side_plate_r.mirror('YZ')

    main_depth = DEPTH - TOP_SLIT_DEPTH

    claw = (
        cq.Workplane('YZ')
        .moveTo(main_depth, HEIGHT - TOP_OFFSET)
        .line(-1.7, TOP_OFFSET)
        .hLine(-0.1)
        .vLine(-TOP_OFFSET)
        .close()
        .extrude(4.6/2, both=True)
    )

    top_plate_main = (
        cq.Workplane()
        .box(WIDTH - SIDE_COVER_WIDTH*2, main_depth, PLATE_T)
        .translate((0, main_depth/2, HEIGHT - PLATE_T/2 - TOP_OFFSET))
        .add(claw)
    )


    back_plate = (
        cq.Workplane()
        .box(WIDTH, BACK_T, HEIGHT - TOP_OFFSET, centered=(True, False, False))
    )

    bottom_plate = (
        cq.Workplane()
        .box(WIDTH, DEPTH, PLATE_T, centered=(True, True, False))
        .cut(
            cq.Workplane()
            .box(WIDTH - SIDE_COVER_WIDTH*2, 1.5, PLATE_T, centered=(True, True, False))
            .translate((0, DEPTH/2 - 1.5/2, 0))
        )
        .translate((0, DEPTH/2, 0))
        .add(top_plate_main)
        .add(back_plate)
        .add(side_plate_r)
        .add(side_plate_l)
        .combine()
        .translate((PIN_PITCH/2 + PIN_PITCH, 0, 0))
        .cut(pin_slits)
    )

    pin = obj.bended_plate_2d(
        cq.Workplane('YZ'),
        [
            (0, -3.1),
            (0, HEIGHT/2),
            (6, HEIGHT/2)
        ],
        PIN_WIDTH
    ).extrude(PIN_WIDTH/2, both=True)
    pins = cq.Workplane()
    for i in range(0, 4):
        pins.add(pin.translate((PIN_PITCH*i, 0, 0)))

    assy = (
        cq.Assembly()
        .add(bottom_plate, color=cq.Color('white'))
        .add(pins, color=cq.Color('lightgray'))
    )
    return assy

def main():
    obj = new()
    show_object(obj)
    obj.save('step_files/GroveConnector_110990037.step')

if __name__ == '__cq_main__':
    main()
