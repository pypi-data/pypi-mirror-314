"""
Classifies: CHEBI:22944 butanediols
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_butanediols(smiles: str):
    """
    Determines if a molecule is a butanediol or a derivative of a butanediol.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a butanediol or a derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has 4 carbon atoms
    if Descriptors.HeavyAtomCount(mol) != 6:
        return False, "Molecule does not have 6 heavy atoms (4 carbons + 2 oxygens)"

    # Check if the molecule has 2 oxygen atoms
    oxygen_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')
    if oxygen_count != 2:
        return False, "Molecule does not have 2 oxygen atoms"

    # Check if the oxygen atoms are part of alcohol groups
    alcohols = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and atom.GetTotalNumHs() == 1]
    if len(alcohols) != 2:
        return False, "Molecule does not have 2 alcohol groups"

    # Check if the alcohol groups are separated by 2 or 3 carbon atoms
    for alcohol1, alcohol2 in ((alcohols[0], alcohols[1]), (alcohols[1], alcohols[0])):
        path = Chem.GetShortestPath(mol, alcohol1.GetIdx(), alcohol2.GetIdx())
        if len(path) in [3, 4]:
            return True, "Molecule is a butanediol or a derivative"

    return False, "Molecule is not a butanediol or a derivative"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22944',
                          'name': 'butanediols',
                          'definition': 'A diol that is a butanediol or a '
                                        'derivative of a butanediol.',
                          'parents': ['CHEBI:23824']},
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
    'num_true_positives': 1,
    'num_false_positives': 9,
    'num_true_negatives': 183908,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.1,
    'recall': 1.0,
    'f1': 0.18181818181818182,
    'accuracy': 0.9999510651485989}