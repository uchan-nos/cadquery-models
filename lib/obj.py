'''
Copyright (c) 2024 Kota UCHIDA

汎用的な造形を担当する関数群
'''

import math

def bended_board_2d(workplane, way_points, board_t):
    '''
    板を曲げ加工したような図形の横面図を生成

    :param workplane: 横面図を置く平面
    :param way_points: 板の中心点列
    :param board_t: 板厚
    '''

    def make_both_side_points(wp, dir, t):
        x, y = wp
        dx = math.sin(dir) * t/2
        dy = math.cos(dir) * t/2
        return ((x - dx, y + dy), (x + dx, y - dy))

    def calc_line_dir(line):
        return math.atan2(line[1][1] - line[0][1], line[1][0] - line[0][0])

    lines = []  # [ ( (x0, y0), (x1, y1) ) ]
    for i in range(len(way_points) - 1):
        p0 = way_points[i]
        p1 = way_points[i + 1]
        lines.append((p0, p1))

    side1_points = []
    side2_points = []

    # the first way point
    line_dir = calc_line_dir(lines[0])
    side_points = make_both_side_points(way_points[0], line_dir, board_t)
    side1_points.append(side_points[0])
    side2_points.append(side_points[1])

    for i in range(len(lines) - 1):
        l0 = lines[i]
        l1 = lines[i + 1]
        l0_dir = calc_line_dir(l0)
        l1_dir = calc_line_dir(l1)
        avg_dir = (l0_dir + l1_dir) / 2
        t = board_t / math.cos(l0_dir - avg_dir)
        side_points = make_both_side_points(l1[0], avg_dir, t)
        side1_points.append(side_points[0])
        side2_points.append(side_points[1])

    # the last way point
    line_dir = calc_line_dir(lines[-1])
    side_points = make_both_side_points(way_points[-1], line_dir, board_t)
    side1_points.append(side_points[0])
    side2_points.append(side_points[1])

    board2d = workplane.moveTo(*side1_points[0])
    for p in side1_points[1:]:
        board2d = board2d.lineTo(*p)
    for p in reversed(side2_points):
        board2d = board2d.lineTo(*p)
    board2d = board2d.close()
    return board2d
