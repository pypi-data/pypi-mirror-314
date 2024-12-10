"""
Classifies: CHEBI:22492 amino aldehyde
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_amino_aldehyde(smiles: str):
    """
    Determines if a molecule is an amino aldehyde (aldehyde with an amino group).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an amino aldehyde, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for aldehyde group
    has_aldehyde = any(atom.GetHybridization() == Chem.HybridizationType.SP2 and
                       atom.GetTotalNumHs() == 0 and
                       sum(n.GetTotalNumHs(True) for n in atom.GetNeighbors()) == 1
                       for atom in mol.GetAtoms())

    if not has_aldehyde:
        return False, "No aldehyde group found"

    # Check for amino group
    has_amino = any(atom.GetSymbol() == 'N' and
                    atom.GetTotalNumHs() == 2 and
                    sum(n.GetTotalNumHs(True) for n in atom.GetNeighbors()) == 3
                    for atom in mol.GetAtoms())

    if not has_amino:
        return False, "No amino group found"

    return True, "Molecule is an amino aldehyde"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22492',
                          'name': 'amino aldehyde',
                          'definition': 'Any aldehyde which contains an amino '
                                        'group.',
                          'parents': ['CHEBI:17478']},
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
    'num_true_negatives': 145789,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9993076975803687}