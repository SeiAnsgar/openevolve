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


"""
#first baseline
mapping = [{'name': 'default',
        'spatial_mapping': {'D1': ['K, 32'], 'D2': ['C, 3']},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}}]

#best result after run 1.0:
mapping = [{'name': 'default',
            'spatial_mapping': {'D1': ['K, 8', 'C, 4'], 'D2': ['C, 6']},
            'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}}]

    mapping = [{'name': 'default',
            'spatial_mapping': {'D1': ['K, 8', 'C, 4'], 'D2': ['C, 6']},
            'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}}]
#current best, v2.2
mapping = [{
                'name': 'default',
                'spatial_mapping': {
                    'D1': ['K, 128'],         # Full utilization of D1 dimension
                    'D2': ['C, 128']          # Full utilization of D2 dimension
                },
                'memory_operand_links': {
                    'O': 'O',   # Output to output buffer
                    'W': 'I2',  # Weight to I2 (local buffer) - maximizes reuse
                    'I': 'I1'   # Input to I1 (local buffer)
                }
            }]
"""

def generate_mapping():
# EVOLVE-BLOCK-START
    mapping = [{'name': 'default',
            'spatial_mapping': {'D1': ['K, 64'], 'D2': ['C, 128']},
            'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}}]

# EVOLVE-BLOCK-END

    return handling(mapping)


if __name__ == "__main__":
    print(generate_mapping())
    #DEBUG
    print("initial_program test complete!")
