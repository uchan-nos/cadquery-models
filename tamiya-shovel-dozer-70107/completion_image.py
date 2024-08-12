'''
Copyright (c) 2024 Kota UCHIDA

SHOVEL/DOZER の完成イメージ
'''

import cadquery as cq
from common import *
from pla import *

import fa130

def assemble():

    L2_L3_SPACE = 2
    L2_ANGLE = 80

    l3_l2_angle = 20

    l1 = (
        new_l1()
        .translate((0, -30, 0))
    )
    l2 = (
        new_l2()
        .rotate(O, ey, -90)
        .rotate(O, ex, L2_ANGLE)
        .translate((20, 0, 20))
    )
    l3 = (
        new_l3()
        .rotate(O, ey, 90)
        .translate((L2_L3_SPACE, L3_LENGTH_LONG - L2_LENGTH, 0))
        .rotate(O, ex, L2_ANGLE)
        .translate((20, 0, 20))
    )
    l3_l2_link = (
        l3
        .edges('%CIRCLE and <X')
        .edges(ClosedSelector())
        .edges('<Z')
        .val().Center()
    )
    l3 = (
        l3
        .rotate(l3_l2_link, l3_l2_link + ex, l3_l2_angle)
    )
    l3_arm_link = (
        l3
        .edges('%CIRCLE and <X')
        .edges(ClosedSelector())
        .edges('<<Z[1]')
        .val().Center()
    )

    print('O to coords of l3')
    print(l3.plane.toLocalCoords(O))
    #l2_l3_spacer = new_spacer(L2_L3_SPACE)
    l4 = (
        new_l4()
        .rotate(O, O + ez, 90)
        .rotate(O, O + ey, 180)
        .translate((25, 30, -5))
    )
    arm = (
        new_arm()
        .rotate(O, ex, 90)
        .rotate(O, ez, 90)
        .rotate(O, ex, 30)
        .translate(l3_arm_link + cq.Vector(-2, 0, 0))
    )

    shaft_h = 30
    shaft = (
        new_hex_shaft(shaft_h)
        .translate((0, 0, -shaft_h/2))
        .rotateAboutCenter(ey, 90)
        .rotateAboutCenter(ex, L2_ANGLE)
        .translate((0, 0, 20))
    )

    motor_l = (
        fa130.new()
    )

    assy = (
        cq.Assembly()
        .add(l1)
        .add(l2)
        .add(l3)
        #.add(l2_l3_spacer, loc=cq.Location((0, -L2_LENGTH, -L2_L3_SPACE/2)))
        .add(shaft, color=cq.Color('goldenrod'))
        .add(l4)
        .add(arm)
        .add(motor_l)
    )

    return assy

def main():
    show_object(assemble())

if __name__ == '__cq_main__':
    main()
