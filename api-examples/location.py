import cadquery as cq

a = cq.Workplane().box(1, 0.1, 1).union(cq.Solid.makeCone(1, 0, 2))
plane1 = cq.Plane((0, 2, 1), normal=(0, 1, 0))
plane2 = cq.Plane((5, 5, 5), normal=(-1, 0, -1))
l1 = cq.Location((-2, 0, 0))
l2 = cq.Location(plane1)
l3 = cq.Location(plane2, (0, -2, 0))
l4 = cq.Location((2, 0, 0), (0, 1, 0), 45)
result = (cq.Assembly()
        .add(a, color=cq.Color(1,1,1,0.6)) # 白
        .add(a, loc=l1, color=cq.Color(0,0,1,0.6)) # 青
        .add(a, loc=l2, color=cq.Color(0,1,0,0.6)) # 緑
        .add(a, loc=l3, color=cq.Color(1,0,0,0.6)) # 赤
        .add(a, loc=l4, color=cq.Color(0,1,1,0.6)) # 水色
        )
show_object(result)
