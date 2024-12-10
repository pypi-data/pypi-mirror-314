"""
Classifies: CHEBI:18368 D-glucosyl-N-acylsphingosine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_D_glucosyl_N_acylsphingosine(smiles: str):
    """
    Determines if a molecule is a D-glucosyl-N-acylsphingosine (Sphingosine substituted at the 1-hydroxy group by a D-glucosyl group and at the 2-amino group by an acyl group).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a D-glucosyl-N-acylsphingosine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find the sphingosine backbone
    sphingosine_pattern = Chem.MolFromSmarts('[NH1][CH2][CH][CH][CH][CH][CH][CH][CH][CH][CH][CH][CH][CH][CH][CH][CH][CH]O')
    match = mol.GetSubstructMatches(sphingosine_pattern)
    if not match:
        return False, "Sphingosine backbone not found"

    # Check for D-glucosyl substituent at the 1-hydroxy position
    glucosyl_pattern = Chem.MolFromSmarts('OC[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O')
    match = mol.GetSubstructMatches(glucosyl_pattern)
    if not match:
        return False, "D-glucosyl group not found"

    # Check for acyl substituent at the 2-amino position
    acyl_pattern = Chem.MolFromSmarts('C(=O)')
    match = mol.GetSubstructMatches(acyl_pattern, maxMatches=1)
    if not match:
        return False, "Acyl group not found"

    acyl_atom = mol.GetAtomWithIdx(list(match)[0][0])
    if acyl_atom.GetTotalNumHs() != 0:
        return False, "Acyl group not attached to amino group"

    return True, "Molecule is a D-glucosyl-N-acylsphingosine"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18368',
                          'name': 'D-glucosyl-N-acylsphingosine',
                          'definition': 'Sphingosine substituted at the '
                                        '1-hydroxy group by a D-glucosyl group '
                                        'and at the 2-amino group by an acyl '
                                        'group.',
                          'parents': ['CHEBI:36500']},
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183920,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.999994562882977}