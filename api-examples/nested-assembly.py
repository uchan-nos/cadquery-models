import cadquery as cq

pcb = cq.Workplane().box(5, 5, 1.6).faces('>Z').hole(1.5)

def make_pin_header():
    pin = cq.Workplane().box(0.6, 0.6, 10).translate((0, 0, 1))
    pla = cq.Workplane().box(2.54, 2.5, 2.5).edges('|Z').chamfer(0.2)
    return (cq.Assembly()
            .add(pla, color=cq.Color('gray10'))
            .add(pin, color=cq.Color('lightgoldenrod1')))

l = cq.Location((0, 0, -(1.6+2.5)/2), (1, 0, 0), 180)
assy = (cq.Assembly()
        .add(pcb, color=cq.Color('green4'))
        .add(make_pin_header(), loc=l))
show_object(assy)
