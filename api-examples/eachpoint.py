import cadquery as cq

def format_vec(v):
    return f'({v[0]:.3g}, {v[1]:.3g}, {v[2]:.3g})'

def print_loc(loc):
    t, r = loc.toTuple()
    print(f'(translation, rotation) = ({format_vec(t)}, {format_vec(r)})')

print('eachpoint.py')

a = cq.Workplane().box(1, 2, 3)
a.eachpoint(print_loc)
print('a.all() =', a.all())
'''
(translation, rotation) = ((4.77e-18, 2.31e-18, 3.7e-17), (0, -0, 0))
a.all() = [<cadquery.cq.Workplane object at 0x000001D947CB6090>]
'''

b = a.faces('Z').sphere(1)
b.eachpoint(print_loc)
print('b.all() =', b.all())
'''
(translation, rotation) = ((-3.09e-10, 2.61e-10, 0.538), (0, -0, 0))
b.all() = [<cadquery.cq.Workplane object at 0x000001D947D89190>]
'''

c = b.add(cq.Solid.makeBox(4, 0.1, 0.1))
c.eachpoint(print_loc)
print('c.all() =', c.all())
'''
(translation, rotation) = ((-3.09e-10, 2.61e-10, 0.538), (0, -0, 0))
(translation, rotation) = ((2, 0.05, 0.05), (0, -0, 0))
c.all() = [<cadquery.cq.Workplane object at 0x000001D947D88490>, <cadquery.cq.Workplane object at 0x000001D947D8A0D0>]
'''

d = c.box(0.2, 5, 1)
show_object(d)
