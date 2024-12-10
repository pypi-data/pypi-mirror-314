"""
Classifies: CHEBI:33456 organoheteryl group
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_organoheteryl_group(smiles: str):
    """
    Determines if a molecule is an organoheteryl group (a univalent group containing carbon with its free valence at an atom other than carbon).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an organoheteryl group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for presence of a carbon atom
    has_carbon = any(atom.GetSymbol() == 'C' for atom in mol.GetAtoms())
    if not has_carbon:
        return False, "No carbon atoms found"

    # Check for the presence of an atom with a free valence
    for atom in mol.GetAtoms():
        if atom.GetNumRadicalElectrons() == 1:
            radicalSymbol = atom.GetSymbol()
            if radicalSymbol != 'C':
                return True, f"Organoheteryl group with free valence at {radicalSymbol}"

    return False, "No atom with a free valence found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33456',
                          'name': 'organoheteryl group',
                          'definition': 'A univalent group containing carbon '
                                        'which has its free valence at an atom '
                                        'other than carbon.',
                          'parents': ['CHEBI:51447']},
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
    'num_true_negatives': 158002,
    'num_false_negatives': 10,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9993042906294273}