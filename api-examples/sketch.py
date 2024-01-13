import cadquery as cq

sk = (
    cq.Sketch()
    .trapezoid(4, 3, 85, 75)
    .vertices()
    .circle(0.5, mode='s')
    .reset()
    .vertices()
    .fillet(0.25)
    .reset()
    .rarray(0.5, 0.9, 5, 2)
    .circle(0.2, mode='s')
)

obj = (
        cq.Workplane()
        .box(6, 2, 0.5)
        .faces('<Y').workplane()
        .placeSketch(sk).extrude(1)
        )

show_object(obj)
