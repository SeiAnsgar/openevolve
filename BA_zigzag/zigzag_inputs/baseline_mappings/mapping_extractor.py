
import json
import re
import yaml
from pprint import pformat

JSON_PATH = "/home/ansi/Documents/zzig/zigzag/outputs/2026-07-21 00:26:15.284500/_conv1_Conv_complete.json"

with open(JSON_PATH) as f:
    data = json.load(f)

raw_spatial_mapping = data["inputs"]["layer"]["user_spatial_mapping"]
raw_memory_operand_links = data["inputs"]["layer"]["memory_operand_links"]
raw_temporal_ordering = data["inputs"]["temporal_mapping"]

############### SPATIAL MAPPING HANDLER ##################

spatial_mapping = {}
for dim, inner_dict in raw_spatial_mapping.items():
    # inner_dict hat genau einen Eintrag, z.B. {"K": 32}
    name, factor = next(iter(inner_dict.items()))
    spatial_mapping[dim] = [f"{name}, {factor}"]

print(spatial_mapping)


################ TEMPORAL MAPPING HANDLER ################
def parse_entry(entry_str):
    # "(FX, 7)" -> ("FX", 7)
    match = re.match(r"\(\s*(\w+)\s*,\s*(\d+)\s*\)", entry_str)
    dim, factor = match.groups()
    return (dim, int(factor))

seen = set()
temporal_result = []

for operand in ("O", "W", "I"):
    for level in raw_temporal_ordering[operand]:
        for entry_str in level:
            entry = parse_entry(entry_str)
            if entry not in seen:
                seen.add(entry)
                temporal_result.append(list(entry))


mapping = {}
mapping["name"] = "default" 
mapping["spatial_mapping"] = spatial_mapping

mapping["memory_operand_links"] = raw_memory_operand_links
mapping_to_list = [mapping]
#mapping["temporal_ordering"] = temporal_result
print(mapping_to_list)

#################### SAVE TO YAML FILE (for debugging) ############################
with open("BA_zigzag/zigzag_inputs/baseline_mappings/extractor_dump.yaml", "w") as f:
    yaml.dump(mapping_to_list, f, sort_keys=False)

print("temporal mapping")
print(temporal_result)

############# PRINT STAGE ######################
code_str = "mapping = " + pformat(mapping_to_list, indent=4, sort_dicts=False)
print(code_str)



"""
#beispiel mapping in richtigem format:
- name: example_name_of_layer0
  spatial_mapping:
    D1:
    - C, 32
    D2:
    - K, 32
temporal_ordering:
    - [OX, 112] # Innermost loop
    - [OY, 112]
    - [FX, 7]
    - [FY, 7]
    - [K, 2] # Outermost loop
memory_operand_links:
    O: O
    W: I2
    I: I1

"""