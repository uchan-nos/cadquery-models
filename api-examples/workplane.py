import cadquery as cq

a = cq.Workplane('XY').box(0.1, 1, 3).edges('>Z and |X').chamfer(0.3)
b = cq.Workplane('YZ').box(0.1, 1, 3).edges('>X and |Y').chamfer(0.3)
c = cq.Workplane('XZ').box(0.1, 1, 3).edges('>Y and |X').chamfer(0.3)
d = cq.Workplane('XZ').box(0.1, 1, 3).edges(cq.selectors.AndSelector(
    cq.selectors.DirectionMinMaxSelector(cq.Vector(0, 1, 0), directionMax=True),
    cq.selectors.ParallelDirSelector(cq.Vector(1, 0, 0)))
    ).chamfer(0.3)
assy = (cq.Assembly()
        .add(a, color=cq.Color(1,1,1,0.6)) # 白
        .add(b, loc=cq.Location((2, 0, 0)), color=cq.Color(0,0,1,0.6)) # 青
        .add(c, loc=cq.Location((-2, 0, 0)), color=cq.Color(0,1,0,0.6)) # 緑
        .add(d, loc=cq.Location((0, 2, 0)), color=cq.Color(1,0,0,0.6)) # 赤
        #.add(a, color=cq.Color(0,1,1,0.6)) # 水色
        )
show_object(assy)
