import math

import cadquery as cq
from const import *

class ClosedSelector(cq.Selector):
    def filter(self, objectList):
        return filter(lambda o: o.IsClosed(), objectList)

def new_l1():
    SHAFT_HOLDER_LENGTH = 10
    d = SHAFT_HOLE_D
    t = 1

    shaft_holder = (
        cq.Workplane('YZ')
        .moveTo(-d/2 - t, 0)
        .vLine(d/2)
        .threePointArc((0, d + t), (d/2 + t, d/2))
        .vLine(-d/2)
        .hLine(-t)
        .vLine(d/2)
        .threePointArc((0, d), (-d/2, d/2))
        .vLine(-d/2)
        .close()
        .extrude(SHAFT_HOLDER_LENGTH/2, both=T)
        .translate((0, -d/2, 0))
    )
    shaft_holder_r = shaft_holder.translate((20, 0, 0))
    shaft_holder_l = shaft_holder.translate((-20, 0, 0))

    l1 = (
        cq.Workplane()
        .box(L1_LENGTH - SHAFT_HOLDER_LENGTH*1.3, L1_WIDTH, 1, centered=(T, F, F))
        .workplane(origin=(0, 0, 0))
        .box(L1_LENGTH, 2, 1, centered=(T, F, T))
        .edges('|Z and (not <Y)')
        .fillet(1)
        .faces('>Z')
        .workplane(origin=(0, L1_WIDTH/2, 0))
        .rarray(L1_LENGTH - SHAFT_HOLDER_LENGTH*2 - 10, 1, 2, 1)
        .hole(SCREW_HOLE_INNER_D)
        .add(shaft_holder_r)
        .add(shaft_holder_l)
        .rotate((0, 0, 0), (0, 0, 1), 180)
    )
    return l1

def new_l2():
    CYLINDER_THICKNESS = 5

    p0 = cq.Vector(0, 0, 0)
    p1 = cq.Vector(0, -L2_LENGTH, 0)

    hex_shaft = (
        new_hex_shaft(CYLINDER_THICKNESS - 0.5, dia=3.0)
        .translate((0, 0, 0.5))
    )

    l2 = (
        cq.Workplane()
        .sketch()
        .arc(p0, SCREW_HOLE_OUTER_D/2, 0, 360)
        .arc(p1, SCREW_HOLE_OUTER_D/2, 0, 360)
        .hull()
        .finalize()
        .extrude(1)
        .pushPoints([p0])
        .cylinder(CYLINDER_THICKNESS, SCREW_HOLE_OUTER_D/2, centered=(T, T, F))
        .pushPoints([p1 + cq.Vector(0, 0, -2)])
        .cylinder(CYLINDER_THICKNESS + 1, SCREW_HOLE_OUTER_D/2, centered=(T, T, F))
        .faces('>Z[3]')
        .workplane(origin=p1)
        .hole(SCREW_HOLE_INNER_D)
        .cut(hex_shaft)
    )

    return l2

def new_l3():
    p0 = cq.Vector(0, 0, 0)
    p1 = cq.Vector(0, -L3_LENGTH_LONG, 0)
    p2 = cq.Vector(0, L3_LENGTH_SHORT, 0)

    l3 = (
        cq.Workplane()
        .pushPoints([p0])
        .sketch()
        .arc(p0, SCREW_HOLE_OUTER_D/2 + 1, 0, 360)
        .arc(p1, SCREW_HOLE_OUTER_D/2,     0, 360)
        .arc(p2, SCREW_HOLE_OUTER_D/2,     0, 360)
        .hull()
        .push([p1])
        .circle(STEP_SCREW_STEP_D/2, mode='s')
        .finalize()
        .extrude(1)
        .pushPoints([p2])
        .cylinder(2, SCREW_HOLE_OUTER_D/2, centered=(T, T, F))
        .faces('>Z')
        .hole(STEP_SCREW_STEP_D)
        .pushPoints([p0])
        .cylinder(5, SCREW_HOLE_OUTER_D/2, centered=(T, T, F))
        .faces('>Z')
        .hole(STEP_SCREW_STEP_D)
    )

    return l3

def new_spacer(height=2.0):
    sp = (
        cq.Workplane()
        .cylinder(height, SCREW_HOLE_OUTER_D/2)
        .faces('>Z')
        .hole(STEP_SCREW_STEP_D)
    )
    return sp

def new_l4():
    SHAFT_HOLE_HEIGHT = L4_HEIGHT - SHAFT_HOLE_D/2 - 1
    SHAFT_HOLE_STRIDE = (L4_LENGTH - 10)/3
    arch_solid = (
        cq.Workplane()
        .sketch()
        .arc((0, SHAFT_HOLE_HEIGHT), SHAFT_HOLE_D/2, 0, 360)
        .segment((-SHAFT_HOLE_D/2, 0), (SHAFT_HOLE_D/2, 0))
        .hull()
        .finalize()
        .extrude(-L4_THICKNESS * 1.5)
        .val()
    )

    HILL_LENGTH = L4_WIDTH/2
    hill_solid = ( # 車軸を載せる少し盛り上がったところ
        cq.Workplane()
        .box(SHAFT_HOLE_D/2,
             HILL_LENGTH,
             SHAFT_HOLE_HEIGHT - SHAFT_HOLE_D/2 - L4_THICKNESS,
             centered=(T, F, F))
        .edges('|Z')
        .fillet(SHAFT_HOLE_D/6)
        .translate((0, -L4_WIDTH*0.45))
        .val()
    )

    plate_v = (
        cq.Workplane('XZ')
        .box(L4_LENGTH, L4_HEIGHT, L4_THICKNESS, centered=(T, F, F))
    )
    plate_h = (
        cq.Workplane()
        .box(L4_LENGTH, L4_WIDTH, L4_THICKNESS, centered=(T, T, F))
        .faces('>Z')
        .workplane()
        .rarray(50, 1, 2, 1) # 取り付けねじ穴
        .hole(STEP_SCREW_STEP_D)
        .rarray(SHAFT_HOLE_STRIDE, 1, 4, 1)
        .eachpoint(lambda loc: hill_solid.moved(loc), combine='a')
    )

    plate = (
        plate_h
        .translate((0, -L4_WIDTH/2 - L4_THICKNESS, 0))
        .add(plate_v)
        .combine()
        .faces('>Y')
        .workplane(origin=(0, 0, 0))
        .rarray(SHAFT_HOLE_STRIDE, 1, 4, 1)
        .eachpoint(lambda loc: arch_solid.moved(loc), combine='s')
    )
    return plate

def new_arm():
    p0 = cq.Vector(0, 0)
    p1 = cq.Vector(ARM_LENGTH_SHORT, 0)
    p2 = cq.Vector(-ARM_LENGTH_LONG, 0)

    arm = (
        cq.Workplane()
        .sketch()
        .segment(p1 + cq.Vector(3, 3), p1 + cq.Vector(3, -3))
        .segment(p2 + cq.Vector(9, -6), p1 + cq.Vector(3, -3))
        .arc(p2, 3, 0, 360)
        .hull()
        .finalize()
        .extrude(2)
        .faces('>Z')
        .workplane()
        .pushPoints([p0])
        .hole(STEP_SCREW_STEP_D)
        .pushPoints([p1, p2])
        .hole(SHAFT_HOLE_D)
    )

    return arm

def main():
    l1 = new_l1()
    l2 = new_l2()
    l3 = new_l3()
    l4 = new_l4()
    spacer = new_spacer()
    arm = new_arm()

    assy = (
        cq.Assembly()
        .add(l1, loc=cq.Location((0, 0, 0)))
        .add(l2, loc=cq.Location((0, 30, 0)))
        .add(l3, loc=cq.Location((20, 30, 0)))
        .add(l4, loc=cq.Location((0, 60, 0)))
        .add(spacer, loc=cq.Location((-20, 30, 0)))
        .add(arm, loc=cq.Location((0, 80, 0)))
    )
    show_object(assy)

if __name__ == '__cq_main__':
    main()
