"""
Classifies: CHEBI:33560 p-block element atom
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_p_block_element_atom(smiles: str):
    """
    Determines if a molecule is a p-block element atom (main group element atom belonging to the p-block of the periodic table).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a p-block element atom, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    if mol.GetNumAtoms() != 1:
        return False, "Not a single atom"

    atom = mol.GetAtomWithIdx(0)
    atomic_number = atom.GetAtomicNum()
    symbol = atom.GetSymbol()
    mass_number = atom.GetMass()

    # Determine the group and period of the element
    period = AllChem.Atom.Atom(symbol).GetPeriod()
    group = AllChem.Atom.Atom(symbol).GetGroup()

    # Check if the element belongs to the p-block
    if 13 <= group <= 18 or group == 1:
        if mass_number == 0:
            return True, f"{symbol} is a p-block element atom"
        else:
            return True, f"{symbol}-{mass_number} is a p-block element atom"
    else:
        if mass_number == 0:
            return False, f"{symbol} is not a p-block element atom"
        else:
            return False, f"{symbol}-{mass_number} is not a p-block element atom"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33560',
                          'name': 'p-block element atom',
                          'definition': 'Any main group element atom belonging '
                                        'to the p-block of the periodic table.',
                          'parents': ['CHEBI:33318']},
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
    'success': False,
    'best': True,
    'error': "type object 'Atom' has no attribute 'Atom'",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}