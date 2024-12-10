"""
Classifies: CHEBI:147369 glucotetraose
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_glucotetraose(smiles: str):
    """
    Determines if a molecule is a glucotetraose (tetrasaccharide composed of 4 glucose moieties).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a glucotetraose, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count the number of glucose moieties
    glucose_count = 0
    for atom in mol.GetAtoms():
        if atom.GetProp('_ChemicalFormula') == 'C6H12O6':
            glucose_count += 1

    if glucose_count != 4:
        return False, f"Not a glucotetraose (contains {glucose_count} glucose moieties)"

    # Check if the moieties are connected
    patts = (
        '[OC]1[C@H]([C@@H]([C@H]([C@@H]([C@H]1O)O)O)O)O',
        '[OC]1[C@@H]([C@@H]([C@@H]([C@@H]([C@@H]1O)O)O)O)O'
    )
    is_connected = False
    for patt in patts:
        m = Chem.MolFromSmarts(patt)
        if m.HasSubstructMatch(mol):
            is_connected = True
            break

    if not is_connected:
        return False, "Glucose moieties are not connected"

    return True, "Molecule is a glucotetraose"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:147369',
                          'name': 'glucotetraose',
                          'definition': 'Any tetrasaccharide composed of 4 '
                                        'glucose moieties.',
                          'parents': ['CHEBI:24268', 'CHEBI:50126']},
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
    'success': False,
    'best': True,
    'error': "'_ChemicalFormula'",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}