import cadquery as cq

a = cq.Solid.makeCone(0.5, 0, 1.5)
b = cq.Solid.makeCone(0.8, 0, 1)
l1 = cq.Location((2, 0, 0))

assy = (cq.Assembly()
        .add(a, name='cone1', color=cq.Color(0,0,1,1))   # 青
        .add(b, name='cone2', color=cq.Color(0,1,0,0.5)) # 緑
        .add(a, name='cone3', loc=l1, color=cq.Color(0,1,1,1))   # 水色
        .add(b, name='cone4', loc=l1, color=cq.Color(1,0,0,0.5)) # 赤
        )

assy.constrain('cone1', 'Fixed')
assy.constrain('cone3', 'Fixed')
assy.constrain('cone1@faces@<Z', 'cone2@faces@<Z', 'Axis')
assy.constrain('cone3@faces@<Z', 'cone4@faces@<Z', 'Axis', param=10)
assy.solve()
show_object(assy)
