import yaml
from pathlib import Path


def handling(some_mapping):
    ordner = Path("zigzag_inputs/mappings/working_dir")
    ordner.mkdir(exist_ok=True)

    version = 1
    while (yamlfile := ordner / f"v{version:02d}.yaml").exists():
        version += 1

    with yamlfile.open("w", encoding="utf-8") as f:
        yaml.safe_dump(some_mapping, f, sort_keys=False, allow_unicode=True)



def generate_mapping():
# EVOLVE-BLOCK-START
    mapping = [
        {
            "name": "default",
            "spatial_mapping": {
                "D1": ["K, 32"],
                "D2": ["C, 32"],
            },
            "memory_operand_links": {"O": "O", "W": "I2", "I": "I1"},
        }
    ]
# EVOLVE-BLOCK-END
    return mapping


if __name__ == "__main__":
    handling(generate_mapping())
    #DEBUG
    print("initial_program test complete!")




############experementing code artifacts maybe delete later###############

"""
@dataclass
class LayerMapping:
    name: str
    spatial_mapping: dict[str, tuple[str, int]]           # {"D1": ("K", 32)}
    memory_operand_links: dict[str, str]                  # {"O": "O", "W": "I2", "I": "I1"}
    temporal_ordering: list[tuple[str, int]] | None = None  # innerste -> äußerste Loop-Reihenfolge
"""
