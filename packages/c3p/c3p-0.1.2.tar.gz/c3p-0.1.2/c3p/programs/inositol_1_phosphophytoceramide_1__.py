"""
Classifies: CHEBI:139053 inositol-1-phosphophytoceramide(1-)
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_inositol_1_phosphophytoceramide_1__(smiles: str):
    """
    Determines if a molecule is an inositol-1-phosphophytoceramide(1-), defined as:
    'An inositol phosphoceramide(1-) obtained by deprotonation of the free phosphate OH group of any
    inositol-1-phosphophytoceramide; major species at pH 7.3.'

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an inositol-1-phosphophytoceramide(1-), False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for inositol ring
    inositol_ring = Chem.MolFromSmiles('C(C(C(C(C(C(O1)O)O)O)O)O)O1')
    if not mol.HasSubstructMatch(inositol_ring):
        return False, "Molecule does not contain an inositol ring"

    # Check for phosphate group
    phosphate_group = Chem.MolFromSmarts('OP(=O)([O-])[O-]')
    if not mol.HasSubstructMatch(phosphate_group):
        return False, "Molecule does not contain a phosphate group"

    # Check for deprotonation of the phosphate OH group
    # This is implicit in the SMARTS pattern for the phosphate group

    # Check for ceramide moiety
    ceramide_pattern = Chem.MolFromSmarts('CCCCCCC[C@@H](O)[C@@H](O)[C@H](NCC(=O)[*])COP')
    if not mol.HasSubstructMatch(ceramide_pattern):
        return False, "Molecule does not contain a ceramide moiety"

    return True, "Molecule is an inositol-1-phosphophytoceramide(1-)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:139053',
                          'name': 'inositol-1-phosphophytoceramide(1-)',
                          'definition': 'An inositol phosphoceramide(1-) '
                                        'obtained by deprotonation of the free '
                                        'phosphate OH group of any '
                                        'inositol-1-phosphophytoceramide; '
                                        'major species at pH 7.3.',
                          'parents': ['CHEBI:64916']},
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
    'num_true_negatives': 183927,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945630899048}