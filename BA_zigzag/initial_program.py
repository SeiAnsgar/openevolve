import yaml
from pathlib import Path



def handling(some_mapping):
    ordner = Path("BA_zigzag/zigzag_inputs/mappings/working_dir")
    ordner.mkdir(exist_ok=True)

    version = 1
    while (yamlfile := ordner / f"v{version:02d}.yaml").exists():
        version += 1
    with yamlfile.open("w", encoding="utf-8") as f:
        yaml.safe_dump(some_mapping, f, sort_keys=False, allow_unicode=True)
    return str(yamlfile)

# EVOLVE-BLOCK-START
def generate_mapping():
    mapping=[{'memory_operand_links': {'I': 'I1', 'O': 'O', 'W': 'I2'},
  'name': 'default',
  'spatial_mapping': {'D1': ['K, 16'],
                      'D2': ['C, 16'],
                      'D3': ['OX, 2'],
                      'D4': ['OY, 2']}},
 {'memory_operand_links': {'I': 'I1', 'O': 'O', 'W': 'I2'},
  'name': 'Add',
  'spatial_mapping': {'D1': ['G, 16'],
                      'D2': ['C, 1'],
                      'D3': ['OX, 1'],
                      'D4': ['OY, 1']}}]
    return handling(mapping)
# EVOLVE-BLOCK-END

"""
first mapping with sccess

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
"""

if __name__ == "__main__":
    print(generate_mapping())
    #DEBUG
    print("initial_program test complete!")
