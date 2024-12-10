"""
Classifies: CHEBI:33300 pnictogen
"""
from rdkit import Chem

PNICTOGEN_ELEMENTS = ['N', 'P', 'As', 'Sb', 'Bi']

def is_pnictogen(smiles: str):
    """
    Determines if a molecule contains a pnictogen element (N, P, As, Sb, Bi).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule contains a pnictogen element, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    pnictogen_atoms = []
    for atom in mol.GetAtoms():
        symbol = atom.GetSymbol()
        if symbol in PNICTOGEN_ELEMENTS:
            pnictogen_atoms.append(symbol)

    if pnictogen_atoms:
        pnictogen_str = ', '.join(sorted(set(pnictogen_atoms)))
        return True, f"Contains pnictogen element(s): {pnictogen_str}"
    else:
        return False, "Does not contain any pnictogen element"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33300',
                          'name': 'pnictogen',
                          'definition': 'Any p-block element atom that is in '
                                        'group 15 of the periodic table: '
                                        'nitrogen, phosphorus, arsenic, '
                                        'antimony and bismuth.',
                          'parents': ['CHEBI:33560']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': None,
    'attempt': 0,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 0,
    'num_false_positives': 100,
    'num_true_negatives': 50,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.33112582781456956}