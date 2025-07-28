'''
Copyright (c) 2025 Kota UCHIDA

RKJXV122400R の軸に取り付けるキャップ
'''

import cadquery as cq
import math

CAP_R = 8.5

SHAFT_H = 3.8
SHAFT_D = 4
SHAFT_W = 3

GAP = 0.05

def new_shaft():
    shaft = (
        cq.Workplane()
        .cylinder(SHAFT_H, SHAFT_D/2 + GAP)
        .edges('>Z')
        .chamfer(0.8, 0.5)
        .intersect(
            cq.Workplane()
            .box(100, SHAFT_W + GAP*2, SHAFT_H)
            .edges('>Z')
            .chamfer(0.8, 0.5)
        )
        .translate((0, 0, SHAFT_H/2))
    )
    return shaft

def new():
    switch_shaft = new_shaft()
    mount_base = (
        cq.Workplane()
        .cylinder(SHAFT_H, SHAFT_D/2 + 1.5, centered=(True, True, False))
        .edges('>Z')
        .chamfer(1)
    )
    mount = mount_base.cut(switch_shaft)

    '''
    cap_sphere_r = 15
    cap_sphere_angle = math.acos((CAP_R + 2) / cap_sphere_r) * 180 / math.pi
    cap = (
        cq.Workplane()
        .sphere(cap_sphere_r, (0, 0, 1), cap_sphere_angle, 90)
        .intersect(
            cq.Workplane()
            .cylinder(100, CAP_R)
        )
        .translate((0, 0, -cap_sphere_r * math.sin(cap_sphere_angle * math.pi / 180)))
        .cut(mount_base)
    )
    '''

    cap_ring_h = 2.25
    cap_cone_h = 3.1
    cap = (
        cq.Workplane()
        .cylinder(cap_ring_h, CAP_R, centered=(True, True, False))
        .add(
            cq.Solid.makeCone(CAP_R, CAP_R - 1.5, cap_cone_h, (0, 0, cap_ring_h), (0, 0, 1))
        )
        .cut(
            cq.Solid.makeCone(CAP_R - 3, CAP_R - 3.5, 0.6, (0, 0, cap_ring_h + cap_cone_h), (0, 0, -1))
        )
        .edges('>Z')
        .fillet(1)
        .cut(mount_base)
    )

    a = (
        cq.Assembly()
        .add(cap,   name='cap', color=cq.Color(1,1,1,0.5))
        .add(mount, name='mount')
    )

    return a

def main():
    obj = new()
    show_object(obj)
    obj.save('step_files/joistickcap1-RKJXV122400R.step')

if __name__ == '__cq_main__':
    main()
