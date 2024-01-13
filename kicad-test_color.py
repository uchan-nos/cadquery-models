import cadquery as cq

W = 2
a = cq.Workplane().box(W, 4, 0.8)
b = cq.Workplane().box(2, 4, 0.8)
c = cq.Workplane().box(1, 4, 0.8)
d = cq.Workplane().box(2, 4, 0.8)
base_a = cq.Workplane().box(2, 4, 1).cut(a)
base_b = cq.Workplane().box(2, 4, 1).cut(b)
base_c = cq.Workplane().box(2, 4, 1).cut(c)
base_d = cq.Workplane().box(2, 4, 1).cut(d)

l_a = cq.Location((0, 0, 0))
l_b = cq.Location((3, 0, 0))
l_c = cq.Location((6, 0, 0))
l_d = cq.Location((9, 0, 0))

result = (cq.Assembly()
        .add(base_a, loc=l_a, color=cq.Color('green'))
        .add(a,      loc=l_a, color=cq.Color('blue'))
        .add(base_b, loc=l_b, color=cq.Color('gold'))
        .add(b,      loc=l_b, color=cq.Color('blue'))
        .add(base_c, loc=l_c, color=cq.Color('gold'))
        .add(c,      loc=l_c, color=cq.Color('blue'))
        .add(base_d, loc=l_d, color=cq.Color('gold'))
        .add(d,      loc=l_d, color=cq.Color('blue'))
        )

show_object(result)
result.save('step_files/kicad-test_color.step')
