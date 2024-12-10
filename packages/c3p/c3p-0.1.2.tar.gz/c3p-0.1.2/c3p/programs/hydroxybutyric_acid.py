"""
Classifies: CHEBI:24684 hydroxybutyric acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_hydroxybutyric_acid(smiles: str):
    """
    Determines if a molecule belongs to the class of hydroxybutyric acids.
    Hydroxybutyric acids are defined as compounds comprising a butyric acid core
    carrying at least one hydroxy substituent.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hydroxybutyric acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains a butyric acid core
    butyric_acid_core = Chem.MolFromSmiles('CCC(O)=O')
    if not mol.HasSubstructMatch(butyric_acid_core):
        return False, "Molecule does not contain a butyric acid core"

    # Check if the molecule has at least one hydroxy substituent
    hydroxy_pattern = Chem.MolFromSmarts('O')
    has_hydroxy = mol.HasSubstructMatch(hydroxy_pattern)

    if has_hydroxy:
        return True, "Molecule contains a butyric acid core with at least one hydroxy substituent"
    else:
        return False, "Molecule contains a butyric acid core but no hydroxy substituent"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24684',
                          'name': 'hydroxybutyric acid',
                          'definition': 'Any compound comprising a butyric '
                                        'acid core carrying at least one '
                                        'hydroxy substituent.',
                          'parents': ['CHEBI:24654']},
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
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 169,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.6296296296296297}