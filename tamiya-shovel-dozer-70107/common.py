import sys

import cadquery as cq

T = True
F = False

O = cq.Vector(0, 0, 0)
ex = cq.Vector(1, 0, 0)
ey = cq.Vector(0, 1, 0)
ez = cq.Vector(0, 0, 1)

# ステップネジのステップの部分の直径
STEP_SCREW_STEP_D = 3.2
# ネジ用の穴の直径
SCREW_HOLE_INNER_D = 3.1
SCREW_HOLE_OUTER_D = 5.5

# 六角シャフト
SHAFT_D = 3.0
SHAFT_HOLE_D = 3.1

L1_LENGTH = 50
L1_WIDTH = 6

# L2の両端の穴の距離
L2_LENGTH = 14

# L3の中央の穴から端の穴までの距離
L3_LENGTH_SHORT = 12.0
L3_LENGTH_LONG = L2_LENGTH + 5

'''
                 .--.  -------
                 |  |       |
                 |  |       | L4_HEIGHT
            ---  |  `----.  |
L4_THICKNESS |   |  L4   |  |
            ---  `-------' ---
                    |----|
                   L4_WIDTH
'''
L4_WIDTH = 10 - 1.5 # 内側の幅
L4_HEIGHT = 6 # 底面からの高さ
L4_THICKNESS = 1.5
L4_LENGTH = 70

# ドーザーアーム
ARM_LENGTH_SHORT = 35 # 中央の穴から端の穴までの距離
ARM_LENGTH_LONG = 85  # 中央の穴から端の穴までの距離

def new_hex_shaft(length, dia=3.0):
    hexVecs = [cq.Vector(loc.toTuple()[0]) for loc in
               cq.Sketch().parray(dia/2, 0, 360, 6).vals()]
    shaft = (
        cq.Workplane()
        .sketch()
        .polygon(hexVecs)
        .finalize()
        .extrude(length)
    )
    return shaft

if '..' not in sys.path:
    sys.path.append('..')
