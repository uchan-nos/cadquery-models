'''
Copyright (c) 2024 Kota UCHIDA

Acrylic plates of X86-ILLUMIBED-1 (MCU Board with an RGBLED)
'''

import cadquery as cq
from pathlib import Path

PCB_W = 50
PCB_H = 30

def new_top(t=3.0, mounthole_d=3.2):
    plate = (
        cq.Workplane()
        .box(PCB_W, PCB_H, t)
    )
    if mounthole_d is not None:
        plate = (
            plate
            .faces('>Z')
            .rect(PCB_W - 2*5, PCB_H - 2*5)
            .vertices()
            .hole(mounthole_d)
        )
    return plate

def new_spacer(t=3.0, mounthole_d=3.2):
    plate = (
        cq.Workplane()
        .box(2*5, PCB_H, t)
    )
    if mounthole_d is not None:
        plate = (
            plate
            .faces('>Z')
            .workplane()
            .pushPoints([(0, 5 - PCB_H/2, 0), (0, PCB_H/2 - 5, 0)])
            .hole(mounthole_d)
        )
    plate = plate.translate((5 + 0.5, 0, 0))
    plate_l = plate.mirror('YZ')
    plate = plate.add(plate_l)
    return plate

def main():
    top = new_top(mounthole_d=1)
    spacer = (
        new_spacer(mounthole_d=None)
        .translate((PCB_W/2 + 12, 0, 0))
    )
    show_object(top)
    show_object(spacer)

    dxf = cq.exporters.DxfDocument()
    dxf.add_shape(top)
    dxf.add_shape(spacer)
    dxf.document.saveas(f'dxf_files/{Path(__file__).stem}.dxf')

if __name__ == '__cq_main__':
    main()
