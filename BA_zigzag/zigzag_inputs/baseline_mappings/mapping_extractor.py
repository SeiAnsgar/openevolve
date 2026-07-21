
import pickle

with open("/home/ansi/Documents/zzig/zigzag/outputs/2026-07-21 00:26:15.284500/cmes.pickle", "rb") as fp:
    cmes = pickle.load(fp)

cme = cmes[0]
#print(cmes)
print(cme.spatial_mapping)
print(cme.temporal_mapping)
print("################")
print(cme.spatial_mapping_int)







"""
SpatialMapping
(
    {
        O: [[], [(K, 32.0), (C, 3.0)], [], []], 
        W: [[], [(K, 32.0), (C, 3.0)], []], 
        I: [[(K, 32.0), (C, 3.0)], [], []]
    }
)
{   
    O: [[(FX, 7), (FY, 7)], [(OY, 16), (OY, 7), (OX, 112), (K, 2)], []], 
    W: [[(FX, 7), (FY, 7), (OY, 16), (OY, 7), (OX, 112), (K, 2)], []], 
    I: [[(FX, 7), (FY, 7), (OY, 16), (OY, 7), (OX, 112), (K, 2)], []]
}

"""












#claude (slop?)
"""
import pickle
import yaml

pickle_path = "/home/ansi/Documents/zzig/zigzag/outputs/2026-07-21 00:26:15.284500/cmes.pickle"

with open(pickle_path, "rb") as fp:
    cmes = pickle.load(fp)

cme = cmes[0]


def to_clean_number(size):
    size = float(size)
    return int(size) if size.is_integer() else size


def flatten_operand_mapping(mapping_dict):
    
    flat = {}
    for operand, levels in mapping_dict.items():
        combined = []
        for level in levels:
            for dim, size in level:
                combined.append((str(dim), to_clean_number(size)))
        flat[str(operand)] = combined
    return flat


def consistent_flat_order(flat_per_operand, label):
    sequences = list(flat_per_operand.values())
    reference = sequences[0]
    for operand, seq in flat_per_operand.items():
        if seq != reference:
            print(f"WARNUNG ({label}): Operand '{operand}' weicht ab!")
            print(f"  Referenz: {reference}")
            print(f"  {operand}: {seq}")
    return reference


# --- Spatial Mapping: bereits flach, direkt verwenden ---
spatial_order = [
    (str(dim), to_clean_number(size))
    for dim, size in cme.spatial_mapping.spatial_loop_dim_size
]

# --- Temporal Mapping: pro Operand+Level flatten ---
temporal_flat = flatten_operand_mapping(cme.temporal_mapping.mapping_dic_origin)
temporal_order = consistent_flat_order(temporal_flat, "temporal_mapping")


# ACHTUNG: Prüfen, ob deine Hardware mehrere Array-Dimensionen (D1, D2, ...) hat.
# Falls ja und K/C sollen auf getrennte Dimensionen, hier ggf. manuell aufteilen.
spatial_mapping_yaml = {
    "D1": [[dim, size] for dim, size in spatial_order]
}

temporal_ordering_yaml = [[dim, size] for dim, size in temporal_order]

mapping_yaml_structure = [
    {
        "name": "default",
        "core_allocation": 1,
        "spatial_mapping": spatial_mapping_yaml,
        "temporal_ordering": temporal_ordering_yaml,
        "memory_operand_links": {
            "O": "O",
            "W": "I2",
            "I": "I1",
        },
    }
]

print("--- YAML-Vorschau ---")
print(yaml.dump(mapping_yaml_structure, sort_keys=False))

print("\n--- Zum Copy-Pasten in initial_program.py ---\n")
print("def get_mapping():")
print(f"    return {mapping_yaml_structure!r}")

"""