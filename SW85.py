'''
Copyright (c) 2024 Kota UCHIDA

SW-85: Plastic Case (Takachi)
'''

import cadquery as cq
from lib import obj

EXT_BOT_W = 60
EXT_BOT_D = 85
EXT_TOP_W = EXT_BOT_W - 1.7
EXT_TOP_D = EXT_BOT_D - 1.7
HEIGHT = 40

EXT_TOP_R = 1.5
EXT_SIDE_R = 2.0

PLATE_T = 2.3     # 板厚
BOT_PLATE_T = 2.0 # 底面の板厚

GUIDE_H = 3.0
GUIDE_T = 1.3

def new(color=cq.Color('lightgray')):
    z_rough_selector = cq.selectors.DirectionSelector((0, 0, 1), 0.1)

    side_inner = (
        cq.Workplane()
        .workplane(offset=BOT_PLATE_T)
        .sketch()
        .rect(EXT_BOT_W - PLATE_T*2, EXT_BOT_D - PLATE_T*2)
        .finalize()
        .extrude(HEIGHT - BOT_PLATE_T - PLATE_T, taper=1.217)
        .edges('not <Z')
        .fillet(0.5)
    )
    side = (
        cq.Workplane()
        .workplane(offset=BOT_PLATE_T)
        .sketch()
        .rect(EXT_BOT_W, EXT_BOT_D)
        .finalize()
        .extrude(HEIGHT - BOT_PLATE_T, taper=1.217)
        .edges(cq.selectors.DirectionSelector(cq.Vector(0, 0, 1), 0.5))
        .fillet(EXT_SIDE_R)
        .edges('>Z')
        .fillet(EXT_TOP_R)
        .cut(side_inner)
    )

    bottom = (
        cq.Workplane()
        .box(EXT_BOT_W, EXT_BOT_D, BOT_PLATE_T, centered=(True, True, False))
        .edges('|Z or <Z')
        .fillet(EXT_TOP_R)
    )

    guide_inner = (
        bottom.faces('>Z').workplane()
        .sketch()
        .rect(EXT_BOT_W - PLATE_T*2 - GUIDE_T*2, EXT_BOT_D - PLATE_T*2 - GUIDE_T*2)
        .finalize()
        .extrude(GUIDE_H, combine=False)
    )
    guide = (
        bottom.faces('>Z').workplane()
        .sketch()
        .rect(EXT_BOT_W - PLATE_T*2, EXT_BOT_D - PLATE_T*2)
        .finalize()
        .extrude(GUIDE_H, combine=False)
        .cut(
            guide_inner.faces('>Y').workplane()
            .box(12, GUIDE_H, GUIDE_T, centered=(True, False, False))
        )
        .edges('|Z')
        .fillet(0.5)
        .cut(guide_inner)
    )

    assy = (
        cq.Assembly()
        .add(side, color=color)
        .add(bottom, color=color)
        .add(guide, color=color)
    )

    return assy

def main():
    obj = new()
    show_object(obj)
    obj.save('step_files/SW85.step')

if __name__ == '__cq_main__':
    main()
