"""
Classifies: CHEBI:228172 fatty alcohol 25:0
"""
from rdkit import Chem
from rdkit.Chem import Descriptors

def is_fatty_alcohol_25_0(smiles: str):
    """
    Determines if a molecule is a fatty alcohol 25:0 (containing 25 carbon atoms).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a fatty alcohol 25:0, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a hydroxyl (-OH) group
    has_hydroxyl = any(atom.GetSymbol() == 'O' and atom.GetTotalDegree() == 2 for atom in mol.GetAtoms())
    if not has_hydroxyl:
        return False, "No hydroxyl group found"

    # Check if the molecule has exactly 25 carbon atoms
    num_carbon_atoms = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if num_carbon_atoms != 25:
        return False, f"Number of carbon atoms is not 25 (found {num_carbon_atoms})"

    # Check if the molecule is aliphatic (no rings)
    if Descriptors.Crippen.NumAromaticRings(mol) > 0:
        return False, "Molecule contains aromatic rings"

    # Check if the molecule is linear (no branching)
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and len(atom.GetNeighbors()) > 2:
            return False, "Molecule is branched"

    return True, "Molecule is a fatty alcohol 25:0"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:228172',
                          'name': 'fatty alcohol 25:0',
                          'definition': 'Any fatty alcohol containing 25 '
                                        'carbons.',
                          'parents': ['CHEBI:197504']},
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
    'error': "module 'rdkit.Chem.Descriptors' has no attribute 'Crippen'",
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