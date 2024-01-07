import cadquery as cq

a = cq.Workplane().box(2, 4, 10)
b = cq.Workplane().box(8, 1, 5)
l1 = cq.Location((0, 10, 0))
l2 = cq.Location((-10, 0, 0))

assy = (cq.Assembly()
        .add(a, name='body1', color=cq.Color(0,0,1,1))   # 青
        .add(b, name='arm1',  color=cq.Color(0,1,0,0.5)) # 緑
        .add(a, name='body2', loc=l1, color=cq.Color(0,1,1,1))   # 水色
        .add(b, name='arm2',  loc=l1, color=cq.Color(1,0,0,0.5)) # 赤
        .add(a, name='body3', loc=l2, color=cq.Color(1,0,1,1))   # 桃
        .add(b, name='arm3',  loc=l2, color=cq.Color(1,1,0,0.5)) # 黄
        )

assy.constrain('body2', 'Fixed')
assy.constrain('body2@faces@<Y', 'arm2@faces@<Y', 'PointInPlane')

assy.constrain('body3', 'Fixed')
assy.constrain('body3@faces@<Y', 'arm3@faces@<Y', 'Axis', param=0)
assy.constrain('body3@faces@<Z', 'arm3@faces@<Z', 'Axis', param=0)
assy.constrain('body3@edges@<Y', 'arm3@faces@<Y', 'PointInPlane')
assy.constrain('body3@edges@<Z', 'arm3@faces@<Z', 'PointInPlane')
assy.solve()

show_object(assy)
