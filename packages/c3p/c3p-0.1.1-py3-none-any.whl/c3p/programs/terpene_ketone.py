"""
Classifies: CHEBI:26872 terpene ketone
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors, rdFMCS

def is_terpene_ketone(smiles: str):
    """
    Determines if a molecule is a terpene ketone (any terpenoid containing a keto group).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a terpene ketone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains a keto group
    has_keto = any(atom.GetSymbol() == 'O' and atom.GetDegree() == 1 and
                   atom.GetTotalNumHs() == 0 for atom in mol.GetAtoms())
    if not has_keto:
        return False, "No keto group found"

    # Check if the molecule is a terpenoid
    terpenoid_patterns = [Chem.MolFromSmiles('C=CC(C)C'),  # isoprene unit
                          Chem.MolFromSmiles('CC(C)=C')]
    is_terpenoid = any(mol.HasSubstructMatch(pattern) for pattern in terpenoid_patterns)

    if not is_terpenoid:
        return False, "Not a terpenoid"

    return True, "Terpene ketone"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26872',
                          'name': 'terpene ketone',
                          'definition': 'Any terpenoid which contains a keto '
                                        'group.',
                          'parents': ['CHEBI:17087', 'CHEBI:26873']},
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
    'num_true_positives': 16,
    'num_false_positives': 100,
    'num_true_negatives': 634,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.13793103448275862,
    'recall': 0.8,
    'f1': 0.2352941176470588,
    'accuracy': 0.8620689655172413}