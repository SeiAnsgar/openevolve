"""
-muss ich überhaupt model und hardare mitgeben? (hardware könnte sinnvoll sein)
-programm dass mapping erzeugt, hat pfat zu .yaml mapping
-programm muss datei anlegen und an vorbereiteten pfad abspeichern, evaluator bekommt dann diesen pfad und kann das mapping laden

"""

"""
@dataclass
class LayerMapping:
    name: str
    spatial_mapping: dict[str, tuple[str, int]]           # {"D1": ("K", 32)}
    memory_operand_links: dict[str, str]                  # {"O": "O", "W": "I2", "I": "I1"}
    temporal_ordering: list[tuple[str, int]] | None = None  # innerste -> äußerste Loop-Reihenfolge


# EVOLVE-BLOCK-START
def generate_mapping(model, hardware): 


    return my_loop_mapping
# EVOLVE-BLOCK-END


if __name__ == "__main__":
    
    my_loop_mapping = generate_mapping()

"""



#---------------------------Von claude erzeugt, einfach mal testen:--------------------------
