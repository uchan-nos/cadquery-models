'''
Copyright (c) 2024 Kota UCHIDA

RSP12-6: Spiral Cable Ground (TAKACHI)
'''

import cadquery as cq
import math

import hexnut

NUT_M = 12
NUT_SIZE = 17
NUT_T = 5
NUT_SEAT_D = 18.8

INT_LEN = 9
EXT_LEN = 62
HOLE_D = 8.4

def new(fast=True, color=cq.Color('gray20')):
    fixing_nut = (
        hexnut.new(NUT_M, NUT_SIZE, NUT_T - 1.3, fillet_side='top')
        .intersect(
            cq.Workplane()
            .cylinder(NUT_T, NUT_SEAT_D/2, centered=(True, True, False))
        )
        .translate((0, 0, 1.3))
        .union(
            cq.Workplane()
            .cylinder(1.3, NUT_SEAT_D/2, centered=(True, True, False))
            .faces('>Z')
            .hole(NUT_M)
        )
        .rotate((0, 0, 0), (1, 0, 0), 180)
        .translate((0, 0, -1.5))
    )

    pipe = (
        cq.Workplane()
        .cylinder(INT_LEN + 4.5 + INT_LEN, NUT_M/2)
        .translate((0, 0, 4.5/2))
        .union(
            hexnut.new(NUT_M, NUT_SIZE - 1, 4.5)
        )
        .faces('>Z')
        .hole(HOLE_D)
    )

    cover_nut_pos = 5
    cover_nut_len = 9
    cover_nut = (
        hexnut
        .new(NUT_M, NUT_SIZE - 1, cover_nut_len, fillet_side='top')
        .translate((0, 0, cover_nut_pos))
    )

    # カバー部の根元と先端の直径
    cover_root_d = NUT_SIZE - 1.8
    cover_tip_d = NUT_SIZE - 5.3

    # カバー部の長さと角度
    cover_root_len = 4
    cover_tip_len = 5.8
    cover_len = EXT_LEN - cover_nut_pos - cover_nut_len
    cover_angle = -math.atan2(cover_root_d/2 - cover_tip_d/2, cover_len)

    cover_pos = cover_nut_pos + cover_nut_len
    cover = (
        cq.Workplane(
            cq.Solid.makeCone(
                cover_root_d/2,
                cover_tip_d/2,
                cover_len
            )
        )
        .translate((0, 0, cover_pos))
        .union(cover_nut)
    )

    spiral_pitch = 4.9
    spiral_len = cover_len - cover_root_len - cover_tip_len

    if fast:
        split_t = spiral_pitch - 2
        split = (
            cq.Workplane()
            .box(cover_root_d, cover_root_d, split_t)
        )
        split_pos = cover_pos + cover_root_len + split_t/2
        while split_pos < cover_pos + cover_root_len + spiral_len:
            cover = cover.cut(
                split
                .translate((0, 0, split_pos))
            )
            split_pos += spiral_pitch
    else:
        cover_root_tip = (
            cover
            .cut(
                cq.Workplane()
                .cylinder(spiral_len,
                          cover_root_d/2,
                          centered=(True, True, False))
                .translate((0, 0, cover_pos + cover_root_len))
            )
        )

        spiral_root_d = cover_root_d + cover_root_len * math.tan(cover_angle)

        spiral_wire = cq.Wire.makeHelix(
            spiral_pitch,               # pitch
            spiral_len + spiral_pitch,  # height
            spiral_root_d/2,            # radius
            angle=cover_angle*180/math.pi
        )

        spiral_face = (
            cq.Workplane('XZ')
            .center(spiral_root_d/2, 0)
            .moveTo(-3.5, 2.4)
            .lineTo(0, 1.2)
            .lineTo(0, -1.2)
            .lineTo(-3.5, -2.4)
            .close()
        )

        spiral = (
            spiral_face
            .sweep(spiral_wire, isFrenet=True)
            .translate((0, 0, cover_pos + cover_root_len - spiral_pitch/2))
            .cut(
                cq.Workplane()
                .box(NUT_SIZE, NUT_SIZE, cover_tip_len, centered=(True, True, False))
                .translate((0, 0, cover_root_len + spiral_len))
                .box(NUT_SIZE, NUT_SIZE, cover_root_len, centered=(True, True, False))
                .translate((0, 0, cover_pos))
            )
        )
        cover = cover_root_tip.union(spiral)

    cover = (
        cover
        .faces('>Z')
        .hole(HOLE_D)
    )

    assy = (
        cq.Assembly(name='RSP12-6')
        .add(fixing_nut, name='fixing_nut', color=color)
        .add(pipe, name='pipe', color=color)
        .add(cover, name='cover', color=color)
    )

    return assy

def main():
    obj = new(False)
    show_object(obj)
    obj.save('step_files/RSP12-6B.step')
    # obj.objects[Name] でパーツごとに参照可能

if __name__ == '__cq_main__':
    main()
