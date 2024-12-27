'''
Copyright (c) 2024 Kota UCHIDA

OLED Display 128x64px I2C
'''

import pin_header

BOARD_W = 25.2
BOARD_D = 26.0
BOARD_T = 1.6

VA_W = 24
VA_D = 12
VA_T = 2
VAFRAME_W = 25
VAFRAME_D = 17

PAD_D = 3.5

def new():
    center = (True, True, False)

    board = (
        cq.Workplane()
        .box(BOARD_W, BOARD_D, BOARD_T, centered=center)
        .faces('>Z')
        .rect(21, 21.8)
        .vertices()
        .hole(PAD_D)
        .faces('>Z')
        .workplane(origin=(0, BOARD_D/2 - 1.27, 0))
        .rarray(2.54, 1, 4, 1)
        .hole(1)
    )
    board_slit = (
        cq.Workplane()
        .box(13, 2, BOARD_T, centered=(True, False, False))
        .edges('>Y and |Z')
        .fillet(0.5)
        .translate((0, -BOARD_D/2, 0))
    )
    board = board.cut(board_slit)

    pads = (
        cq.Workplane()
        .rect(21, 21.8, forConstruction=True)
        .vertices()
        .cylinder(BOARD_T + 0.1, PAD_D/2, centered = center)
        .faces('>Z')
        .hole(2)
    )

    va = (
        cq.Workplane()
        .box(VA_W, VA_D, VA_T)
        .translate((0, (VAFRAME_D - VA_D)/2 - 0.5, VA_T/2 + BOARD_T))
    )
    vaframe = (
        cq.Workplane()
        .box(VAFRAME_W, VAFRAME_D, VA_T)
        .translate((0, 0, VA_T/2 + BOARD_T))
        .cut(va)
    )

    cable_r = (BOARD_T + VA_T + 0.3)/2
    cable = (
        cq.Workplane('YZ')
        .moveTo(0, BOARD_T + VA_T)
        .hLine(-2)
        .threePointArc((-2 - cable_r, (BOARD_T + VA_T)/2 + 0.1), (-2, -0.3))
        .hLine(2)
        .vLine(0.1)
        .hLine(-2 + 0.1)
        .threePointArc((-2 - cable_r + 0.1, (BOARD_T + VA_T)/2 + 0.1), (-2, BOARD_T + VA_T - 0.1))
        .hLine(2)
        .close()
        .extrude(6, both=True)
        .translate((0, -BOARD_D/2 + (BOARD_D - VAFRAME_D)/2, 0))
    )

    assy = (
        cq.Assembly()
        .add(board, color=cq.Color('deepskyblue4'))
        .add(pads, color=cq.Color('gray90'))
        .add(va, color=cq.Color('darkorchid4'))
        .add(vaframe, color=cq.Color('black'))
        .add(cable, color=cq.Color('burlywood'))
    )

    pin = pin_header.new()
    for x in range(4):
        assy.add(pin, name=f'pin{x}',
                 loc=cq.Location((2.54*x - 2.54 - 1.27, BOARD_D/2 - 1.27, 0),
                                 (0, 1, 0),
                                 180))

    # 1 番ピンを原点とする
    return cq.Assembly().add(assy, loc=cq.Location((2.54 + 1.27, -BOARD_D/2 + 1.27, 2.54)))

def main():
    obj = new()
    show_object(obj)
    obj.save('step_files/OLED_Display_I2C.step')

if __name__ == '__cq_main__':
    main()
