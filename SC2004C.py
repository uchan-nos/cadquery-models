'''
Copyright (c) 2024 Kota UCHIDA

SC2004C: Character LCD Display (SUNLIKE)
'''

import pin_header

FRAME_T = 0.7
FRAME_W = 96.2
FRAME_D = 35.2
FRAME_H = 4.8
SLIT_H = FRAME_H - 1

BOARD_T = 1.6

VA_W = 77.0
VA_D = 26.3

def make_pin_socket(xnum, ynum):
    body = (
        cq.Workplane()
        .box(xnum*2.54 - 0.08, ynum*2.54 + 0.3, 8.5, centered=(True, True, False))
    )
    pin = (
        cq.Workplane()
        .box(0.25, 0.5, 5, centered=(True, True, False))
        .edges('<Z and |X')
        .chamfer(0.5, 0.13)
        .translate((0, 0, -3))
    )
    assy = (
        cq.Assembly()
        .add(body, color=cq.Color('gray10'))
    )
    for x in range(xnum):
        for y in range(ynum):
            assy.add(pin, name=f'pinsocket_pin_{x}{y}',
                     loc=cq.Location((2.54*(x - xnum/2 + 0.5), 2.54*(y - ynum/2 + 0.5), 0)),
                     color=cq.Color('lightgoldenrod1'))
    return assy

def new():
    center = (True, True, False)

    board = (
        cq.Workplane()
        .box(118, 43, BOARD_T)
        .translate((0, 0, -BOARD_T/2))
        .faces('>Z')
        .center(-1, 0)
        .rect(108, 29)
        .vertices()
        .hole(3.5)
    )
    backlight = (
        cq.Workplane()
        .box(VA_W + 5, VA_D + 3, 1, centered=center)
    )

    lcd = (
        cq.Workplane()
        .box(FRAME_W - 2*FRAME_T, FRAME_D - 2*FRAME_T, FRAME_H - FRAME_T - 1, centered=center)
        .translate((0, 0, 1))
    )

    frame_slit_corner = (
        cq.Workplane()
        .rect(FRAME_W, FRAME_D, forConstruction=True)
        .vertices()
        .box(4, 4, FRAME_H, centered=center)
    )
    frame_slit_x = (
        cq.Workplane()
        .moveTo(-FRAME_W/2 + FRAME_T/2, 0)
        .lineTo(FRAME_W/2 - FRAME_T/2, 0)
        .vertices()
        .box(FRAME_T, 8, SLIT_H, centered=center)
    )
    frame = (
        cq.Workplane()
        .box(FRAME_W, FRAME_D, FRAME_H - 1)
        .translate((0, 0, FRAME_H/2))
        .edges('>Z')
        .fillet(FRAME_T/2)
        .cut(
            cq.Workplane()
            .box(FRAME_W - 2*FRAME_T, FRAME_D - 2*FRAME_T, FRAME_H - FRAME_T, centered=center)
        )
        .cut(
            cq.Workplane()
            .box(VA_W, VA_D, FRAME_T)
            .translate((0, 0, FRAME_H - FRAME_T/2))
        )
        .cut(frame_slit_corner)
        .cut(frame_slit_x)
    )

    pin = pin_header.new()
    pin_main = cq.Assembly()
    for x in range(2):
        for y in range(7):
            pin_main.add(pin, name=f'pin_main_{x}{y}',
                         loc=cq.Location((-x*2.54, (y-3)*2.54, -BOARD_T), (0, 1, 0), 180))
    sock_main = make_pin_socket(2, 7)

    pin_led = cq.Assembly()
    for y in range(5):
        pin_led.add(pin, name=f'pin_led_{y}',
                    loc=cq.Location((0, (y-2)*2.54, -BOARD_T), (0, 1, 0), 180))
    sock_led = make_pin_socket(1, 5)

    board = (
        board
        .faces('>Z')
        .workplane(origin=(-118/2 + 5.04 - 1.27, 0, 0))
        .rarray(2.54, 2.54, 2, 7)
        .hole(1)
        .faces('>Z')
        .workplane(origin=(118/2 - 6, 0, 0))
        .rarray(1, 2.54, 1, 5)
        .hole(1)
    )

    assy = (
        cq.Assembly()
        .add(board,     color=cq.Color('forestgreen'))
        .add(backlight, color=cq.Color('white'))
        .add(lcd,       color=cq.Color(3/255, 252/255, 252/255, 0.3))
        .add(frame,     color=cq.Color('gray10'))
        .add(pin_main,  loc=cq.Location((-118/2 + 5.04, 0, 0)))
        .add(sock_main, loc=cq.Location((-118/2 + 5.04 - 1.27, 0, -8.5 - 2.54 - BOARD_T)))
        .add(pin_led,   loc=cq.Location((118/2 - 6, 0, 0)))
        .add(sock_led,  loc=cq.Location((118/2 - 6, 0, -8.5 - 2.54 - BOARD_T)))
    )
    # 1 番ピンを原点とする
    return cq.Assembly().add(assy, loc=cq.Location((118/2 - 5.04, 15.24/2, BOARD_T + 2.54 + 8.5)))

def main():
    obj = new()
    show_object(obj)
    obj.save('step_files/SC2004C.step')

if __name__ == '__cq_main__':
    main()
