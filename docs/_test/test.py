import gdstk
import numpy as np
import palgds.base_cells as bc

from palgds.circuit import Circuit

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
                           "out": bc.Port((radius, 0), 0, "op")})

lib2 = gdstk.Library()
gdscell = bc.GDSCell('cell2', "lib.gds", rename="cccell", ports_filename="cell2.txt")
lib2.add(gdscell, *gdscell.dependencies(True))


rr = RingResonator(name="rr", radius=5, gap=0.2, width=0.45)

circuit = Circuit(name='rr_cct',
                  pcells={"dev1": rr, "dev2": rr, },
                  translations={"dev1": (0, 0),
                                "dev2": (100, 50),},
                  rotations={"dev1": 0, "dev2": np.pi/2},
                  links=[{"from": ("dev1", "out"), "to": ("dev2", "out")},
                         # {"from": ("dev1", "in"), "to": ("dev2", "in"), }
                         ]
                  )
print(circuit.ports)
for key in circuit.ports:
    print(key, circuit.ports[key].position, circuit.ports[key].angle, circuit.ports[key].port_type)

lib2.add(circuit, *circuit.dependencies(True))
lib2.write_gds("aaaa.gds", max_points=4000)