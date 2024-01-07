import cadquery as cq

def format_vec(v):
    return f'({v[0]:.3g}, {v[1]:.3g}, {v[2]:.3g})'

def print_loc(loc):
    t, r = loc.toTuple()
    print(f'(translation, rotation) = ({format_vec(t)}, {format_vec(r)})')

print('eachpoint.py')

print(cq.Workplane().size())
print(cq.Workplane().objects)
print(cq.Workplane().box(1, 1, 1).objects)

a = cq.Workplane().box(1, 2, 3).faces('Z').box(1, 1, 1)

a.eachpoint(print_loc)
print('a.all() =', a.all())
'''
(translation, rotation) = ((-7.8e-18, 1.96e-17, 0.135), (0, -0, 0))
a.all() = [<cadquery.cq.Workplane object at 0x000001AD0D625090>]
'''

b = a.add(cq.Solid.makeBox(4, 0.1, 0.1))

b.eachpoint(print_loc)
print('b.all() =', b.all())
'''
(translation, rotation) = ((-7.8e-18, 1.96e-17, 0.135), (0, -0, 0))
(translation, rotation) = ((2, 0.05, 0.05), (0, -0, 0))
b.all() = [<cadquery.cq.Workplane object at 0x000001AD0D644450>, <cadquery.cq.Workplane object at 0x000001AD0D645490>]
'''

c = b.box(0.2, 5, 1)
