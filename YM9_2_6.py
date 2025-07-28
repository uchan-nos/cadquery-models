'''
Copyright (c) 2025 Kota UCHIDA

YM9-2-6: Aluminum thin case (Takachi)
'''

import cadquery as cq
import math

from lib import obj
import screw

T = 1.0
CORNER_GAP = 0.2
SCREW_M = 2.6
SCREW_L = 5

def new(width=90, height=20, depth=60, color=None):
    screw_hole = (
        cq.Workplane('YZ')
        .cylinder(width + 0.1, SCREW_M/2)
        .translate((0, -depth/2 + 5, 10))
    )
    screw_hole = screw_hole.add(screw_hole.mirror('XZ'))

    washer = (
        cq.Workplane()
        .cylinder(0.5, 6.5/2, centered=(True, True, False))
        .faces('>Z')
        .hole(2.8)
    )

    screw1 = (
        screw.new_truss(SCREW_M, SCREW_L)
        .translate((0, 0, 0.5))
        .add(washer)
    )

    screw_rf = (
        screw1
        .rotate((0, 0, 0), (0, 1, 0), 90)
        .translate((width/2, -depth/2 + 5, 10))
    )

    screw_lrf = screw_rf.add(screw_rf.mirror('YZ'))
    screws = screw_lrf.add(screw_lrf.mirror('XZ'))

    cover = (
        obj.bended_plate_2d(
            cq.Workplane('XZ'),
            [
                (-width/2 + T/2, 0),
                (-width/2 + T/2, height - T/2),
                (width/2 - T/2, height - T/2),
                (width/2 - T/2, 0)
            ],
            T
        )
        .extrude(depth/2, both=True)
        .cut(screw_hole)
    )

    base_side1 = (
        obj.bended_plate_2d(
            cq.Workplane('XY'),
            [
                (-width/2 + T + T/2, 10),
                (-width/2 + T + T/2, T/2),
                (width/2 - T - T/2, T/2),
                (width/2 - T - T/2, 10)
            ],
            T
        )
        .extrude(height - T - T - CORNER_GAP)
        .translate((0, -depth/2, T + CORNER_GAP))
        .edges('>Y and <Z')
        .chamfer(10 - T - 0.1)
        .cut(screw_hole)
    )

    base_side2 = (
        obj.bended_plate_2d(
            cq.Workplane('XZ'),
            [
                (-width/2 + T + T/2, 10),
                (-width/2 + T + T/2, T/2),
                (width/2 - T - T/2, T/2),
                (width/2 - T - T/2, 10)
            ],
            T
        )
        .extrude(depth/2 - T - 2*CORNER_GAP, both=True)
        .edges('|X and >Z')
        .chamfer(10 - T - 0.1)
    )

    base_main = (
        obj.bended_plate_2d(
            cq.Workplane('YZ'),
            [
                (-depth/2 + T/2, height - T),
                (-depth/2 + T/2, T/2),
                (depth/2 - T/2, T/2),
                (depth/2 - T/2, height - T)
            ],
            T,
            fillet=CORNER_GAP
        )
        .extrude(width/2 - 2*(1.5*T), both=True)
        .add(base_side1)
        .add(base_side1.mirror('XZ'))
        .add(base_side2)
    )

    assy = (
        cq.Assembly(name='YM9-2-6')
        .add(cover, name='cover', color=color or cq.Color('lightgray'))
        .add(base_main, name='base', color=color or cq.Color('gray30'))
        .add(screws, name='screws', color=color or cq.Color('gray'))
    )

    return assy

def main():
    obj = new()
    show_object(obj)
    obj.save('step_files/YM9-2-6.step')
    # obj.objects['cover'] と obj.objects['base'] でパーツごとに参照可能

if __name__ == '__cq_main__':
    main()
