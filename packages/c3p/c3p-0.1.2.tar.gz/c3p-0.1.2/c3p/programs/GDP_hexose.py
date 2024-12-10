"""
Classifies: CHEBI:21167 GDP-hexose
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_GDP_hexose(smiles: str):
    """
    Determines if a molecule is a GDP-hexose (GDP-sugar with a hexosyl residue).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a GDP-hexose, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for GDP substructure
    gdp_pattern = Chem.MolFromSmarts('C1=NC2=NC(=NC2=N1)N')
    if not mol.HasSubstructMatch(gdp_pattern):
        return False, "GDP substructure not found"

    # Check for hexosyl residue
    hexose_pattern = Chem.MolFromSmarts('[C@H]1[C@H]([C@H]([C@@H]([C@H](O1)O)O)O)O')
    if not mol.HasSubstructMatch(hexose_pattern):
        return False, "Hexosyl residue not found"

    # Check for glycosidic bond between GDP and hexosyl residue
    glycosidic_bond_pattern = Chem.MolFromSmarts('C-O-C')
    if not mol.HasSubstructMatch(glycosidic_bond_pattern):
        return False, "Glycosidic bond between GDP and hexosyl residue not found"

    return True, "The molecule is a GDP-hexose"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:21167',
                          'name': 'GDP-hexose',
                          'definition': 'A GDP-sugar in which the sugar '
                                        'component is a hexosyl residue.',
                          'parents': ['CHEBI:21169']},
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
    'num_true_negatives': 183916,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999945627647254}