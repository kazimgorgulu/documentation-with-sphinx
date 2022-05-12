import gdstk
import numpy as np
import palgds.base_cells as bc

from palgds.circuit import Circuit

def draw(pcell):
    """ svg export function from gdstk library."""
    bb = pcell.bounding_box()
    scaling = 300 / (1.1 * (bb[1][0] - bb[0][0]))
    name = (pcell.name + ".svg")
    pcell.write_svg(
        name,
        scaling=scaling,
        background="none",
        shape_style={(0, 0): {"fill": "darkorange", "stroke": "chocolate"}},
        label_style={(3, 2): {"stroke": "red", "fill": "none", "font-size": "32px"}},
        pad="5%",
    )
    # print(f"Saving {name} (scaling {scaling})")

# RingResonator PCell class example:
class RingResonator(bc.PCell):
    def __init__(self, name, radius, gap, width, layer=0, datatype=0):
        super().__init__(name)
        self._create_elements(radius, gap, width, layer, datatype)
        self._create_ports(radius)

    def _create_elements(self, radius, gap, width, layer, datatype):
        center = (0, radius+gap+width)
        ring = gdstk.ellipse(center, radius+width/2, radius-width/2, layer=layer, datatype=datatype, tolerance=2e-4)
        straight_waveguide = gdstk.rectangle((-radius, -width/2), (radius, width/2), layer=layer, datatype=datatype)
        self.add(ring, straight_waveguide)

    def _create_ports(self, radius):
        self.ports.update({"in": bc.Port((-radius, 0), np.pi, "op"),
                           "out": bc.Port((radius, 0), 0, "op"),})

if __name__ == "__main__":
    ring_res = RingResonator(name="RingRes", radius=5, gap=0.2, width=0.45)
    ring_res.write_svg(ring_res.name + ".svg")
    lib = gdstk.Library()
    lib.add(ring_res, *ring_res.dependencies(True))
    lib.write_gds("RingRes.gds", max_points=4000)
    draw(ring_res)
    print(ring_res)
    print(ring_res.ports)



import os
path = os.path.abspath('../../palgds-demo/samples/')
# print(path)
gdscell = bc.GDSCell(name='MMI', filename=path+"/MMI.gds", rename="cccell")

# p = bc.Port((1,2.222), 3.33)
# print(p)
# ring_res = RingResonator(name="RingRes", radius=10, gap=0.2, width=0.45)
# lib = gdstk.Library()
# lib.add(ring_res.cell, *ring_res.cell.dependencies(True))
# lib.write_gds("ring_resonator.gds",max_points=4000)
#
#
#
# # In the following lines we will create connect two ring resonators in a circuit:
#
# circuit = Circuit(name='rr_cct',
#                   pcells={"dev1": ring_res, "dev2": ring_res, },
#                   translations={"dev1": (0, 0),
#                                 "dev2": (100, 50),},
#                   rotations={"dev1": 0, "dev2": 0},
#                   links=[{"from": ("dev1", "out"), "to": ("dev2", "out"), }]
#                   )
#
# lib = gdstk.Library()
# lib.add(circuit.cell, *circuit.cell.dependencies(True))
# lib.write_gds("ring_res_circuit.gds",max_points=4000)
#
# # In above circuit you will realize that the routing waveguide is not correct.
# # Layer number is not matching with the ring resonators. This is because Circuit class uses default Optical Trace
# # from technology file. So we will create a custom Trace and use it in ring resonator circuit:





