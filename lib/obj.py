'''
Copyright (c) 2024 Kota UCHIDA

汎用的な造形を担当する関数群
'''

from cadquery import NearestToPointSelector, Selector
import math

class NullSelector(Selector):
    def filter(self, objectList):
        return []

def bended_board_2d(workplane, way_points, board_t, sharpness=0.5):
    '''
    板を曲げ加工したような図形の横面図を生成

    :param workplane: 横面図を置く平面
    :param way_points: 板の中心点列
    :param board_t: 板厚
    :param shapness: 曲げ加工の鋭さ（0～1）
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
    outer_points = []
    inner_points = []

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

        reldir = l1_dir - l0_dir # relative direction
        if reldir > math.pi:
            reldir -= math.pi * 2
        elif reldir < -math.pi:
            reldir += math.pi * 2
        # Now, -pi <= reldir <= pi

        if reldir < 0:
            outer_points.append(side_points[0])
            inner_points.append(side_points[1])
        elif reldir > 0:
            outer_points.append(side_points[1])
            inner_points.append(side_points[0])

    # the last way point
    line_dir = calc_line_dir(lines[-1])
    side_points = make_both_side_points(way_points[-1], line_dir, board_t)
    side1_points.append(side_points[0])
    side2_points.append(side_points[1])

    fillet_factor = (1 - sharpness) / 2
    skt = workplane.sketch()
    skt.polygon(side1_points + list(reversed(side2_points)))
    if fillet_factor > 0:
        skt.vertices(
            sum(map(NearestToPointSelector, inner_points), start=NullSelector())
        ).fillet(board_t*fillet_factor).reset()
    skt.vertices(
        sum(map(NearestToPointSelector, outer_points), start=NullSelector())
    ).fillet(board_t*(fillet_factor+0.5)).reset()

    return skt.finalize()
