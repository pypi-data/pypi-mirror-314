"""
Classifies: CHEBI:21601 N-acetyl-D-hexosamine
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem import AllChem

def is_N_acetyl_D_hexosamine(smiles: str):
    """
    Determines if a molecule is an N-acetyl-D-hexosamine.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is an N-acetyl-D-hexosamine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of an N-acetyl group
    n_acetyl_pattern = Chem.MolFromSmarts('CC(=O)N')
    if not mol.HasSubstructMatch(n_acetyl_pattern):
        return False, "Molecule does not contain an N-acetyl group"

    # Check for the presence of a hexose ring
    hexose_ring_pattern = Chem.MolFromSmarts('C1OC(O)C(O)C(O)C(O)C1')
    if not mol.HasSubstructMatch(hexose_ring_pattern):
        return False, "Molecule does not contain a hexose ring"

    # Check for the D-configuration of the hexose
    d_config_pattern = Chem.MolFromSmarts('[C@H]1([C@@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H](O)O1)N')
    if not mol.HasSubstructMatch(d_config_pattern):
        return False, "Hexose does not have D-configuration"

    # Check for the pyranose form
    pyranose_pattern = Chem.MolFromSmarts('C1OCCCC1')
    if mol.HasSubstructMatch(pyranose_pattern):
        return True, "Molecule is an N-acetyl-D-hexosamine in the pyranose form"
    else:
        return True, "Molecule is an N-acetyl-D-hexosamine"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:21601',
                          'name': 'N-acetyl-D-hexosamine',
                          'definition': 'Any N-acetylhexosamine in which the '
                                        'hexosamine has D-configuration. The '
                                        'structure provided is an illustrative '
                                        'example of the pyranose form of an '
                                        'N-acetyl-D-hexosamine.',
                          'parents': ['CHEBI:7203']},
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
    'num_false_positives': 0,
    'num_true_negatives': 183924,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999945630012234}