"""
Classifies: CHEBI:190295 inorganic calcium salt
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_inorganic_calcium_salt(smiles: str):
    """
    Determines if a molecule is an inorganic calcium salt (lacks C-H bonds).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an inorganic calcium salt, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if molecule contains calcium
    if 'Ca' not in set([atom.GetSymbol() for atom in mol.GetAtoms()]):
        return False, "Molecule does not contain calcium"

    # Check for presence of C-H bonds
    for bond in mol.GetBonds():
        atom1 = mol.GetAtomWithIdx(bond.GetBeginAtomIdx())
        atom2 = mol.GetAtomWithIdx(bond.GetEndAtomIdx())
        if atom1.GetSymbol() == 'C' and atom2.GetSymbol() == 'H' or atom2.GetSymbol() == 'C' and atom1.GetSymbol() == 'H':
            return False, "Molecule contains C-H bonds"

    return True, "Inorganic calcium salt"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:190295',
                          'name': 'inorganic calcium salt',
                          'definition': 'A calcium salt that lacks C-H bonds',
                          'parents': ['CHEBI:167164', 'CHEBI:24839']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.8,
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
    'num_true_positives': 1,
    'num_false_positives': 73,
    'num_true_negatives': 183850,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.013513513513513514,
    'recall': 1.0,
    'f1': 0.026666666666666665,
    'accuracy': 0.9996030969313412}