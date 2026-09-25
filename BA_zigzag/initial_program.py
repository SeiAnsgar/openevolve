import uuid
from pathlib import Path
import yaml

def handling(some_mapping):
    ordner = Path("BA_zigzag/zigzag_inputs/mappings/working_dir")
    ordner.mkdir(parents=True, exist_ok=True)

    # Generiert einen eindeutigen Namen pro Evaluation, ohne Schleife
    yamlfile = ordner / f"mapping_{uuid.uuid4().hex[:8]}.yaml"
    
    with yamlfile.open("w", encoding="utf-8") as f:
        yaml.safe_dump(some_mapping, f, sort_keys=False, allow_unicode=True)
    return str(yamlfile)


def generate_mapping():
# EVOLVE-BLOCK-START
    mapping = [
        {
            'name': 'Conv',
            'spatial_mapping': {'D1': ['K, 16'], 'D2': ['C, 16']},
            'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
        },
        {
            'name': 'Gemm',
            'spatial_mapping': {'D1': ['K, 16'], 'D2': ['C, 16']},
            'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
        },
        {
            'name': 'default',
            'spatial_mapping': {'D1': ['K, 16'], 'D2': ['C, 16']},
            'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
        }
    ]
# EVOLVE-BLOCK-END
    return handling(mapping)


if __name__ == "__main__":
    print(generate_mapping())
    #DEBUG
    print("initial_program test complete!")



""" real baseline
# EVOLVE-BLOCK-START
    mapping = [
        {
            'name': 'Conv',
            'spatial_mapping': {'D1': ['K, 16'], 'D2': ['C, 16']},
            'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
        },
        {
            'name': 'Gemm',
            'spatial_mapping': {'D1': ['K, 16'], 'D2': ['C, 16']},
            'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
        },
        {
            'name': 'default',
            'spatial_mapping': {'D1': ['K, 16'], 'D2': ['C, 16']},
            'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'}
        }
    ]
# EVOLVE-BLOCK-END
"""