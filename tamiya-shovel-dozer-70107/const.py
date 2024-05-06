T = True
F = False

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
ARM_LENGTH_SHORT = 20 # 中央の穴から端の穴までの距離
ARM_LENGTH_LONG = 50  # 中央の穴から端の穴までの距離
