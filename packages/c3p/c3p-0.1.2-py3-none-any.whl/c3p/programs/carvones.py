"""
Classifies: CHEBI:23048 carvones
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_carvones(smiles: str):
    """
    Determines if a molecule is a carvone (p-menthane monoterpenoid with the carvone skeleton).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a carvone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule is a monoterpenoid
    if AllChem.CalcNumAtomStoCacheMode(mol, 20, 16) > 10:
        return False, "Molecule is not a monoterpenoid"

    # Check if the molecule contains a p-menthane skeleton
    sssr = Chem.GetSymmSSSR(mol)
    p_menthane_present = False
    for ring in sssr:
        if len(ring) == 6:
            p_menthane_present = True
            break

    if not p_menthane_present:
        return False, "Molecule does not contain a p-menthane skeleton"

    # Check for the presence of the carvone skeleton
    carvone_skeleton = Chem.MolFromSmiles('C=C1CC[C@@H](CC1=O)C')
    if not mol.HasSubstructMatch(carvone_skeleton):
        return False, "Molecule does not contain the carvone skeleton"

    return True, "Molecule is a carvone"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23048',
                          'name': 'carvones',
                          'definition': 'Any p-menthane monoterpenoid having '
                                        'the carvone skeleton as part of its '
                                        'structure.',
                          'parents': ['CHEBI:25186']},
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
    'error': "module 'rdkit.Chem.AllChem' has no attribute "
             "'CalcNumAtomStoCacheMode'",
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