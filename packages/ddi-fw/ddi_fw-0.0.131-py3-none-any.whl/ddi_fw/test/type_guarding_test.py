# from typing import List
# from itertools import product
# from ddi_fw.utils import ZipHelper

# from ddi_fw.utils.enums import DrugBankTextDataTypes, UMLSCodeTypes

# def generate_pairs(umls_code_types:  List[UMLSCodeTypes] = None, text_types:  List[DrugBankTextDataTypes] = None):
#     _umls_codes = [t.value[0] for t in umls_code_types]
#     _text_types = [t.value[0] for t in text_types]
#     items = [f'{item[0]}_{item[1]}' for item in product(_umls_codes, _text_types)]
#     print(items)


# if __name__ == "__main__":
#     generate_pairs(umls_code_types=[UMLSCodeTypes.TUI, UMLSCodeTypes.ENTITIES], text_types= [DrugBankTextDataTypes.DESCRIPTION])


# # reveal_type(UMLSCodeTypes.ENTITIES)  # Revealed type is "Literal[Direction.up]?"
