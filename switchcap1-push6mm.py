'''
Copyright (c) 2026 Kota UCHIDA

6mm 角のタクタイルスイッチの軸に取り付けるキャップ
'''

import cadquery as cq
import math

CAP_R = 4.5
CAP_SPHERE_R = CAP_R*2

SHAFT_H = 2.0
SHAFT_D = 3.3

CAP_H = SHAFT_H + 1

GAP = 0.05

def new_shaft():
    shaft = (
        cq.Workplane()
        .add(
            cq.Solid.makeCone(
                (SHAFT_D + 0.1)/2 + GAP,
                SHAFT_D/2 + GAP,
                SHAFT_H
            )
        )
    )
    return shaft

def new_button_mark(txt='A', size=None):
    # 球形の殻を作る
    shell_t = 0.3
    spherical_shell = (
        cq.Workplane()
        .sphere(CAP_SPHERE_R)
        .cut(
            cq.Workplane()
            .sphere(CAP_SPHERE_R - shell_t)
        )
    )

    if size is None:
        if len(txt) == 1:
            size = CAP_R * 1.5
        elif len(txt) == 2:
            size = CAP_R * 1.1
        else:
            size = CAP_R * 0.8

    return (
        cq.Workplane()
        .text(txt, size, 100)
        .intersect(spherical_shell)
    )

def new(button_mark='A'):
    switch_shaft = new_shaft()

    cap_sphere_angle = math.acos((CAP_R + 2) / CAP_SPHERE_R) * 180 / math.pi
    cap = (
        cq.Workplane()
        .sphere(CAP_SPHERE_R, (0, 0, 1))
        .cut(
            new_button_mark(button_mark)
        )
        .translate((0, 0, CAP_H - CAP_SPHERE_R))
        .intersect(
            cq.Workplane()
            .cylinder(100, CAP_R)
            .translate((0, 0, 50))
        )
        .cut(switch_shaft)
    )

    return cap

def main():
    obj1 = new('A')
    obj2 = new('B')
    obj3 = new('Opt')
    show_object(obj1, options={ 'alpha': 0.7 })
    show_object(obj2.translate((CAP_R*3, 0, 0)), options={ 'alpha': 0.7 })
    show_object(obj3.translate((-CAP_R*3, 0, 0)), options={ 'alpha': 0.7 })
    cq.exporters.export(obj1, 'step_files/switchcap1-push6mm_A.step')
    cq.exporters.export(obj2, 'step_files/switchcap1-push6mm_B.step')
    cq.exporters.export(obj3, 'step_files/switchcap1-push6mm_Opt.step')

if __name__ == '__cq_main__':
    main()
