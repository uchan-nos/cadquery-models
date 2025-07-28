'''
Copyright (c) 2025 Kota UCHIDA

LED-Tester2-Case: Original case for Uchan's LED Tester2
'''

import cadquery as cq

import hexnut
from lib import obj
import YM9_2_6

SPACER_H = 11
PCB_W = 85
PCB_D = 55.5
PCB_POS = cq.Vector(-PCB_W/2, PCB_D/2, YM9_2_6.T + SPACER_H + 1.6)

LCD_HOLE_DISTANCE_X = 75
LCD_HOLE_DISTANCE_Y = 31
LCD_HOLE_REF_Y = -6.45
LCD_HOLE_TO_PIN_X = 8 - (80 - LCD_HOLE_DISTANCE_X)/2

PIN_SOCK_SIZE = cq.Vector(2.54*16, 2.54, 8.5)
PIN_SOCK_POS = cq.Vector(
    -LCD_HOLE_DISTANCE_X/2 + LCD_HOLE_TO_PIN_X - 1.27 + PIN_SOCK_SIZE.x/2,
    LCD_HOLE_REF_Y + LCD_HOLE_DISTANCE_Y,
    YM9_2_6.T + SPACER_H + 1.6 + PIN_SOCK_SIZE.z/2)

SW2_POS = PCB_POS + cq.Vector(5.865, -50.236)
SW3_POS = PCB_POS + cq.Vector(5.865, -41.727)

ROT_POS = PCB_POS + cq.Vector(77.575, -46.39)

# TB のサイズ
TB_SIZE = cq.Vector(7.62, 12.8, 13.8)
# TB1 の左下の座標
TB1_POS = PCB_POS + cq.Vector(12.755, -52.48) + TB_SIZE/2
# TB の配置間隔
TB_SPACING = 15.24

J2_PIN2_POS = PCB_POS + cq.Vector(9.75, -14.64)
J2_J3_SPACING = 10.16

RV1_PIN1_POS = PCB_POS + cq.Vector(57.375, -6.385)
RV1_SIZE = cq.Vector(6.6, 4.7, 6.99)
RV1_POS = RV1_PIN1_POS + cq.Vector(2.54, RV1_SIZE.y/2 - 1.02, -RV1_SIZE.z/2 - 1.6)

USBC_SIZE = cq.Vector(8.94, 6.90, 3.16)
USBC_S1_POS = PCB_POS + cq.Vector(66.39, -6.591)
USBC_POS = USBC_S1_POS + cq.Vector(8.64/2, 3.8 + 2.6 - USBC_SIZE.y/2, USBC_SIZE.z/2)

def new():
    case = YM9_2_6.new(color=cq.Color(1, 1, 1, 0.2))
    pcb_file = r'C:\Users\uchan\work\gh\uchan-nos\elecpriv\LED-Current-Meter_2\LED-Current-Meter_2.step'
    pcb = cq.importers.importStep(pcb_file)
    pcb_loc = cq.Location(PCB_POS - cq.Vector(0, 0, 1.6))

    spacer = hexnut.new(2.6, 5, SPACER_H, fillet_side='both')
    spacers = spacer.translate((LCD_HOLE_DISTANCE_X/2, LCD_HOLE_REF_Y, YM9_2_6.T))
    spacers.add(spacers.mirror('YZ'))
    # この時点で spacers は左右 1 本ずつのスペーサのみを含む
    spacer_lcd = spacers.translate((0, 0, SPACER_H + 1.6))
    spacers.add(spacers.translate((0, LCD_HOLE_DISTANCE_Y, 0)))
    spacers.add(spacer_lcd)

    lcd_pin_socket = (
        cq.Workplane()
        .box(2.54 * 16, 2.54 * 1, 8.5)
        .translate(PIN_SOCK_POS)
    )

    tbs = (
        cq.Workplane()
        .rarray(TB_SPACING, 1, 4, 1)
        .box(*TB_SIZE.toTuple())
        .translate(TB1_POS + cq.Vector(3*TB_SPACING/2, 0))
    )

    rv1 = (
        cq.Workplane()
        .box(*RV1_SIZE.toTuple())
        .translate(RV1_POS)
    )

    usbc = (
        cq.Workplane()
        .box(*USBC_SIZE.toTuple())
        .translate(USBC_POS)
    )

    assy = (
        cq.Assembly(name='LED-Tester2-Case')
        .add(case, name='case')
        .add(pcb, name='pcb', loc=pcb_loc, color=cq.Color(0, 0.35, 0.11))
        .add(spacers, name='spacers', color=cq.Color('lightgray'))
        .add(lcd_pin_socket, name='lcd_pin_socket', color=cq.Color('gray10'))
        .add(tbs, name='terminal_blocks', color=cq.Color('darkseagreen'))
        .add(rv1, name='rv1', color=cq.Color('blue'))
        .add(usbc, name='usbc', color=cq.Color('lightgray'))
    )

    return assy

def new_drawing():
    '''
    穴開けのための図面生成
    '''
    top_plane = cq.Plane(
        origin=(0, 0, 20),
        normal=cq.Vector(0, 0, 1)
    )
    top = (
        cq.Workplane(top_plane)
        .box(90, 60, 1)
        .translate((0, 0, -0.5))
        .pushPoints([(LCD_HOLE_DISTANCE_X/2, LCD_HOLE_REF_Y),
                     (-LCD_HOLE_DISTANCE_X/2, LCD_HOLE_REF_Y)])
        .hole(7)
        .faces('>Z')
        .workplane()
        .pushPoints([SW2_POS, SW3_POS])
        .hole(4)
        .cut(
            cq.Workplane(top_plane)
            .box(2.54 * 16 + 2, 2.54 + 2, YM9_2_6.T * 2)
            .translate((PIN_SOCK_POS.x, PIN_SOCK_POS.y, 0))
        )
        .cut(
            cq.Workplane(origin=cq.Vector(TB1_POS.x + 3*TB_SPACING/2, TB1_POS.y, 20))
            .rarray(TB_SPACING, 1, 4, 1)
            .box(9, 14, YM9_2_6.T * 2)
        )
        .pushPoints([ROT_POS])
        .hole(7)
    )

    left_plane = cq.Plane(
        origin=(-90/2, 0, 20/2),
        normal=cq.Vector(-1, 0, 0),
        xDir=cq.Vector(0, -1, 0)
    )
    left = (
        cq.Workplane(left_plane)
        .box(60, 20, 1)
        .translate((0.5, 0, 0))
        .cut(
            cq.Workplane(left_plane)
            .rarray(J2_J3_SPACING, 1, 2, 1)
            .box(2.54*3 + 1, 2.54 + 1, 2 * YM9_2_6.T)
            .translate(cq.Vector(0, J2_PIN2_POS.y - J2_J3_SPACING/2, PCB_POS.z + 2.54/2 - 20/2))
        )
    )
    right = left.mirror('YZ')
    right.plane.origin = cq.Vector(90/2, 0, 20/2)

    back_plane = cq.Plane(
        origin=(0, 60/2, 20/2),
        normal=cq.Vector(0, 1, 0),
        xDir=cq.Vector(-1, 0, 0)
    )
    back = (
        cq.Workplane(back_plane)
        .box(90, 20, 1)
        .translate((0, -0.5, 0))
        .cut(
            cq.Workplane(back_plane)
            .box(10, 4, 2 * YM9_2_6.T)
            .translate((USBC_POS.x, 0, USBC_POS.z - 20/2))
        )
    )

    bottom_plane = cq.Plane(
        origin=(0, 0, 0),
        normal=cq.Vector(0, 0, -1),
        xDir=cq.Vector(1, 0, 0)
    )
    bottom = (
        cq.Workplane(bottom_plane)
        .box(90, 60, 1)
        .translate((0, 0, 0.5))
        .faces('<Z')
        .workplane(origin=(0, LCD_HOLE_REF_Y + LCD_HOLE_DISTANCE_Y/2, 0))
        .rarray(LCD_HOLE_DISTANCE_X, LCD_HOLE_DISTANCE_Y, 2, 2)
        .hole(3)
    )

    return { k: v.section() for k,v in {
        'top': top,
        'left': left,
        'right': right,
        'back': back,
        'bottom': bottom,
    }.items()}

def main():
    '''
    obj = new()
    show_object(obj)
    #obj.save('step_files/LED-Tester2-Case.step')
    '''

    xy = cq.Workplane('XY')

    obj = new_drawing()

    ex = cq.Vector(1, 0, 0)
    ey = cq.Vector(0, 1, 0)
    ez = cq.Vector(0, 0, 1)

    back_comp = cq.exporters.utils.toCompound(obj['back'])
    back = (
        cq.Workplane(cq.Plane(origin=(0, 60/2 + 20/2 + 0.1, 0), xDir=-ex, normal=ez))
        .add(back_comp.transformShape(obj['back'].plane.fG))
    )
    left_comp = cq.exporters.utils.toCompound(obj['left'])
    left = (
        cq.Workplane(cq.Plane(origin=(0, 90/2 + 20/2 + 0.1, 0), xDir=ey, normal=ez))
        .add(left_comp.transformShape(obj['left'].plane.fG))
    )
    right_comp = cq.exporters.utils.toCompound(obj['right'])
    right = (
        cq.Workplane(cq.Plane(origin=(0, 90/2 + 20/2 + 0.1, 0), xDir=-ey, normal=-ez))
        .add(right_comp.transformShape(obj['right'].plane.fG))
    )
    bottom_comp = cq.exporters.utils.toCompound(obj['bottom'])
    bottom = (
        cq.Workplane(cq.Plane(origin=(0, -71.2, 0), xDir=ex, normal=ez))
        .add(bottom_comp.transformShape(obj['bottom'].plane.fG))
    )

    #show_object(obj['top'])
    #show_object(obj['left'])
    #show_object(obj['right'])
    #show_object(obj['back'])
    show_object(obj['bottom'])
    dxf = (
        cq.exporters.DxfDocument()
        .add_shape(obj['top'])
        .add_shape(back)
        .add_shape(left)
        .add_shape(right)
        .add_shape(bottom)
    )
    dxf.document.saveas("dxf_files/LED-Tester2-Case_panels.dxf")

    show_object(cq.importers.importDXF("dxf_files/LED-Tester2-Case_panels.dxf"))


if __name__ == '__cq_main__':
    main()
