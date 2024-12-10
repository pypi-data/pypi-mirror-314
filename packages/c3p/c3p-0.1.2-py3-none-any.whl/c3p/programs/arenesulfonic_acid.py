"""
Classifies: CHEBI:33555 arenesulfonic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_arenesulfonic_acid(smiles: str):
    """
    Determines if a molecule is an arenesulfonic acid.

    Arenesulfonic acids are organic derivatives of sulfonic acid in which the sulfo group is linked directly to carbon of an aryl group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an arenesulfonic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find sulfonic acid groups
    sulfonic_acid_groups = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == 'S' and sum(1 for neighbor in atom.GetNeighbors() if neighbor.GetSymbol() == 'O') == 3]

    if not sulfonic_acid_groups:
        return False, "No sulfonic acid group found"

    # Check if sulfonic acid group is attached to an aromatic ring
    for idx in sulfonic_acid_groups:
        atom = mol.GetAtomWithIdx(idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetIsAromatic():
                return True, "Sulfonic acid group attached to an aromatic ring"

    return False, "Sulfonic acid group not attached to an aromatic ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33555',
                          'name': 'arenesulfonic acid',
                          'definition': 'Organic derivatives of sulfonic acid '
                                        'in which the sulfo group is linked '
                                        'directly to carbon of an aryl group.',
                          'parents': ['CHEBI:33551']},
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
    'num_true_positives': 14,
    'num_false_positives': 100,
    'num_true_negatives': 43945,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.12280701754385964,
    'recall': 1.0,
    'f1': 0.21875,
    'accuracy': 0.997730316166958}