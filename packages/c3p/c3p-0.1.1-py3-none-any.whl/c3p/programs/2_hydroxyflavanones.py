"""
Classifies: CHEBI:141992 2-hydroxyflavanones
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_2_hydroxyflavanones(smiles: str):
    """
    Determines if a molecule is a 2-hydroxyflavanone.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 2-hydroxyflavanone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has a flavanone backbone
    flavanone_backbone = Chem.MolFromSmarts('C1C(C(=O)C2=C(C=C(C=C2)O)O)=CC(=C1)O')
    if mol.HasSubstructMatch(flavanone_backbone) is False:
        return False, "Molecule does not have a flavanone backbone"

    # Check if the molecule has a hydroxy group at position 2
    hydroxy_at_2 = Chem.MolFromSmarts('C1C(C(=O)C2=C(C=C(C=C2)O)O)=C[C@@](C(=C1)O)(O)')
    if mol.HasSubstructMatch(hydroxy_at_2):
        return True, "Molecule is a 2-hydroxyflavanone"
    else:
        return False, "Molecule does not have a hydroxy group at position 2"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:141992',
                          'name': '2-hydroxyflavanones',
                          'definition': 'Any hydroxyflavanone that has a '
                                        'hydroxy substituent at position 2.',
                          'parents': ['CHEBI:24697', 'CHEBI:38131']},
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
    'num_true_negatives': 183924,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945630012234}