"""
Classifies: CHEBI:27288 vinca alkaloid
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem.rdMolDescriptors import GetMorganFingerprint

def is_vinca_alkaloid(smiles: str):
    """
    Determines if a molecule is a vinca alkaloid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a vinca alkaloid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for indole and indoline rings
    indole_pattern = Chem.MolFromSmarts('c1ccc2c(c1)ncn2')
    indoline_pattern = Chem.MolFromSmarts('C1C=CN2C=CC=CC2=C1')

    if not mol.HasSubstructMatch(indole_pattern) or not mol.HasSubstructMatch(indoline_pattern):
        return False, "Missing indole or indoline ring"

    # Check for dimer structure
    morgan_fingerprint = GetMorganFingerprint(mol, 2, useChiralityTypes=True)
    if morgan_fingerprint.GetLength() < 150:
        return False, "Not a dimer structure"

    # Check for alkaloid
    num_basic_atoms = rdMolDescriptors.CalcNumBasicAtoms(mol)
    if num_basic_atoms < 1:
        return False, "Not an alkaloid"

    # Check for vinca plant origin or synthetic analog
    vinca_pattern = Chem.MolFromSmarts('C(=O)OC.C(=O)OC')
    if mol.HasSubstructMatch(vinca_pattern):
        return True, "Vinca alkaloid (natural or semi-synthetic)"
    else:
        return True, "Synthetic vinca alkaloid analog"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27288',
                          'name': 'vinca alkaloid',
                          'definition': 'A group of indole-indoline dimers '
                                        'which are alkaloids obtained from the '
                                        'Vinca genus of plants, together with '
                                        'semi-synthetic and fully synthetic '
                                        'analogues.',
                          'parents': ['CHEBI:65323']},
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
    'num_true_negatives': 183912,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999891253520667}