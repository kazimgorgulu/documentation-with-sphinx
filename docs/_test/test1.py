import gdstk
import numpy as np
import palgds.base_cells as bc

from palgds.circuit import Circuit

def draw(pcell):
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
    print(f"Saving {name} (scaling {scaling})")



class MyTrace(bc.Trace):
    """Trace template"""

    def __init__(self, name, points, bend_radius=5):
        super().__init__(name, points, width=0.45, bend_radius=bend_radius, offset=0, layer=3, datatype=0)
        pass


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
        self.ports.update({"in": (-radius, 0, np.pi, "op"), "out": (radius, 0, 0, "op")})

lib = gdstk.Library()
rr = RingResonator(name="rr", radius=5, gap=0.2, width=0.45)
rr.write_svg(rr.name + ".svg")
lib.add(rr, *rr.dependencies(True))


trace = bc.Trace("trace", [(0, 0), (5, 0), (5, 5)])
lib.add(trace, *trace.dependencies(True))

textcell = bc.TextCell("text", "AAA")
textcell.add(gdstk.Reference(trace))
tcell = gdstk.Cell("tcell")
text_polygons = gdstk.text("BBB", 45, (200, 0))
tcell.add(*text_polygons)
lib.add(textcell, *textcell.dependencies(True), tcell, *tcell.dependencies(True))

cell2 = gdstk.Cell('cell2')
cell2.add(gdstk.Reference(textcell), gdstk.Reference(tcell), gdstk.rectangle((-5,-5), (0, 0)))
lib.add(cell2, *cell2.dependencies(True))

lib.write_gds("lib.gds", max_points=4000)


lib2 = gdstk.Library()
gdscell = bc.GDSCell('cell2', "lib.gds", rename="cccell", ports_filename="cell2.txt")
lib2.add(gdscell, *gdscell.dependencies(True))

circuit = Circuit(name='rr_cct',
                  pcells={"dev1": rr, "dev2": rr, },
                  translations={"dev1": (0, 0),
                                "dev2": (100, 50),},
                  rotations={"dev1": 0, "dev2": 0},
                  links=[{"from": ("dev1", "out"), "to": ("dev2", "out")},
                         # {"from": ("dev1", "in"), "to": ("dev2", "in"), }
                         ]
                  )

print(circuit.ports)

# for i in circuit.dependencies(True):
#     print(i.__class__.__mro__)
    # print(Circuit.__mro__)

lib2.add(circuit, *circuit.dependencies(True))

lib2.write_gds("lib2.gds", max_points=4000)