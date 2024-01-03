'''
Copyright (c) 2024 Kota UCHIDA

CNZ1023: Photointerrupter (Panasonic)
'''

import cadquery as cq

L = 12
W = 5
H = 10
SLIT_W = 3
SLIT_H = H - 2.5
ARM_THICKNESS = 2
ARM_HOLE_D = 3
LEG_W = 0.45
LEG_L = 1.6+1

slit = (
        cq.Workplane()
        .box(W, SLIT_W, SLIT_H)
        .translate((0, 0, (H - SLIT_H) / 2))
        )
body = (
        cq.Workplane()
        .box(W, L, H)
        .edges('>Z and >X')
        .chamfer(1.2)
        .cut(slit)
        )

landscape_hole = (
        cq.Workplane('XZ')
        .moveTo(0.25, ARM_HOLE_D/2)
        .threePointArc((0.25+ARM_HOLE_D/2, 0), (0.25, -ARM_HOLE_D/2))
        .hLine(-0.5)
        .threePointArc((-0.25-ARM_HOLE_D/2, 0), (-0.25, ARM_HOLE_D/2))
        .close()
        .extrude(ARM_THICKNESS).translate((0, ARM_THICKNESS/2, 0))
        )
arm = (
        cq.Workplane()
        .box(18, ARM_THICKNESS, 6)
        .edges('|Y')
        .fillet(2)
        .cut(landscape_hole.translate((6, 0, 0)))
        .faces('<Y')
        .workplane()
        .moveTo(-6, 0)
        .hole(ARM_HOLE_D)
        )

leg = (
        cq.Workplane()
        .box(LEG_W, LEG_W, LEG_L)
        .translate((0, 0, -LEG_L/2))
        )

result = (
        cq.Assembly()
        .add(body, name='body', loc=cq.Location((0, 0, H/2)), color=cq.Color('gray10'))
        .add(arm, name='arm', color=cq.Color('gray10'))
        .add(leg, name='leg1', loc=cq.Location((1.27, 7.6/2, 0)), color=cq.Color('gray'))
        .add(leg, name='leg2', loc=cq.Location((1.27, -7.6/2, 0)), color=cq.Color('gray'))
        .add(leg, name='leg3', loc=cq.Location((-1.27, 7.6/2, 0)), color=cq.Color('gray'))
        .add(leg, name='leg4', loc=cq.Location((-1.27, -7.6/2, 0)), color=cq.Color('gray'))
        )

result.constrain('body', 'Fixed')
result.constrain('body@faces@>Y', 'arm@faces@>Y', 'Axis', param=0)
result.constrain('body@faces@>Z', 'arm@faces@>Z', 'Axis', param=0)
result.constrain('arm@faces@>Y', 'body@faces@>Y', 'PointInPlane')
result.constrain('arm@faces@<Z', 'body@faces@<Z', 'PointInPlane')
result.solve()
result.save('cnz1023.step')

show_object(result)
