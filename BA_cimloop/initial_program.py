import accelforge as af
from accelforge.frontend.mapping import Storage, Temporal, Spatial, Compute


def generate_mapping() -> af.Mapping:
    # EVOLVE-BLOCK-START
    
    # EVOLVE-BLOCK-END
    print("WRONG FUNCTION!!!")
    return af.Mapping(nodes=nodes)

"""
nodes = [
        Storage(tensors=["T0", "W0", "T1"], component="MainMemory"),
        Storage(tensors=["T0", "W0", "T1"], component="GlobalBuffer"),
        Temporal(rank_variable="m", tile_shape=1),
        Temporal(rank_variable="n0", tile_shape=1),
        Temporal(rank_variable="n1", tile_shape=1),
        Compute(einsum="Matmul0", component="MAC"),
    ]
"""
if __name__ == "__main__":
    # Lokaler Schnelltest ohne OpenEvolve: einfach das erzeugte Mapping
    # anzeigen, um Tippfehler/Strukturprobleme frueh zu bemerken.
    m = generate_mapping()
    print(m.compact_str())




