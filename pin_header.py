import cadquery as cq

def new(length=11.6, pitch=2.54, pin_thickness=0.64, lower_length=2.98):
    pla_thickness = pitch
    pin = (
            cq.Workplane()
            .box(pin_thickness, pin_thickness, length)
            .edges('|Z').chamfer(pin_thickness/10)
            .translate((0, 0, length/2 - lower_length))
            )
    pla = (
            cq.Workplane()
            .box(pitch, pitch, pitch, combine=False)
            .edges('|Z').chamfer(0.2)
            .translate((0, 0, pla_thickness/2))
            )
    return (
            cq.Assembly()
            .add(pla, color=cq.Color('gray10'))
            .add(pin, color=cq.Color('lightgoldenrod1'))
            )

def main():
    show_object(new())

if __name__ == '__cq_main__':
    main()
