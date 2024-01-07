import cadquery as cq

box = cq.Workplane().box(5, 10, 10)
slit1 = box.faces('>Z').box(5, 3, 7, combine=False).translate((0, 0, -7/2))
body1 = box.cut(slit1)
slit2 = box.faces('>Z').box(5, 3, 7, combine=True).translate((0, 0, -7/2))
body2 = box.cut(slit2)

assy = (cq.Assembly()
        .add(box)
        .add(body1, loc=cq.Location((10,0,0)), color=cq.Color(0,0,1,1))   # 青
        .add(slit1, loc=cq.Location((10,0,0)), color=cq.Color(0,1,0,0.5)) # 緑
        .add(body2, loc=cq.Location((20,0,0)), color=cq.Color(0,0,1,1))   # 青
        .add(slit2, loc=cq.Location((20,0,0)), color=cq.Color(0,1,0,0.5)) # 緑
        )

show_object(assy)
