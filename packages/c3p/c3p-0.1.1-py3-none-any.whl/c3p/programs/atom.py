"""
Classifies: CHEBI:33250 atom
"""
from rdkit import Chem

def is_atom(smiles: str):
    """
    Determines if a molecule is an atom.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an atom, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has only one atom
    if mol.GetNumAtoms() != 1:
        return False, "Not an atom (more than one atom present)"

    # Check if the SMILES string matches the atom symbol and isotope
    atom = mol.GetAtomWithIdx(0)
    atom_symbol = atom.GetSymbol()
    atom_isotope = atom.GetIsotope()

    smiles_atom = smiles.strip('[]')
    if smiles_atom.isdigit():
        smiles_isotope = int(smiles_atom)
        smiles_symbol = ''
    else:
        try:
            smiles_isotope = int(''.join(char for char in smiles_atom if char.isdigit()))
        except ValueError:
            smiles_isotope = 0
        smiles_symbol = ''.join(char for char in smiles_atom if not char.isdigit())

    if smiles_symbol.upper() != atom_symbol.upper():
        return False, "Not an atom (symbol mismatch)"

    if smiles_isotope != 0 and smiles_isotope != atom_isotope:
        return False, "Not an atom (isotope mismatch)"

    return True, "Molecule is an atom"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33250',
                          'name': 'atom',
                          'definition': 'A chemical entity constituting the '
                                        'smallest component of an element '
                                        'having the chemical properties of the '
                                        'element.',
                          'parents': ['CHEBI:24431']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: invalid literal for int() with base 10: ''",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 23,
    'num_false_positives': 12,
    'num_true_negatives': 183686,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.6571428571428571,
    'recall': 1.0,
    'f1': 0.7931034482758621,
    'accuracy': 0.9999346835691075}