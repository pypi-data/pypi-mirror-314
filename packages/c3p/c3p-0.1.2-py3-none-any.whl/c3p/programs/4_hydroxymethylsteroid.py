"""
Classifies: CHEBI:145951 4-hydroxymethylsteroid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_4_hydroxymethylsteroid(smiles: str):
    """
    Determines if a molecule is a 4-hydroxymethylsteroid (a steroid substituted with a hydroxymethyl group at position 4).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 4-hydroxymethylsteroid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find the steroid core
    steroid_core = AllChem.MurckoScaffold.GetScaffoldForMol(mol)
    if steroid_core is None:
        return False, "No steroid core found"

    # Check if the molecule contains a hydroxymethyl group
    hydroxymethyl_pattern = Chem.MolFromSmarts('CO')
    matches = mol.GetSubstructMatches(hydroxymethyl_pattern)
    if not matches:
        return False, "No hydroxymethyl group found"

    # Check if the hydroxymethyl group is attached to position 4 of the steroid core
    steroid_core_atoms = set(steroid_core.GetAtoms())
    for match in matches:
        atom = mol.GetAtomWithIdx(match)
        if atom.GetSymbol() == 'O':
            carbon_neighbor = atom.GetNeighbors()[0]
            if carbon_neighbor.GetIdx() not in steroid_core_atoms:
                return True, "4-hydroxymethylsteroid"

    return False, "Hydroxymethyl group not attached to position 4 of the steroid core"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:145951',
                          'name': '4-hydroxymethylsteroid',
                          'definition': 'Any steroid which is substituted by a '
                                        'hydroxymethyl group at position 4.',
                          'parents': ['CHEBI:15734', 'CHEBI:35341']},
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
    'success': False,
    'best': True,
    'error': "module 'rdkit.Chem.AllChem' has no attribute 'MurckoScaffold'",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}