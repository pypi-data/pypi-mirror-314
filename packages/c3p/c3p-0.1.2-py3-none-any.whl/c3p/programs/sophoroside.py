"""
Classifies: CHEBI:145470 sophoroside
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_sophoroside(smiles: str):
    """
    Determines if a molecule is a sophoroside (any glycoside of sophorose).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a sophoroside, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find sophorose moiety
    sophorose_smarts = "[C@H]1([C@@H](CO)[C@@H](O)[C@H](O)[C@H]1O)[C@@H](CO)[C@H](O)[C@@H](O)[C@H](O)[C@H](O)"
    sophorose_mol = Chem.MolFromSmarts(sophorose_smarts)
    if sophorose_mol is None:
        return None, None

    matches = mol.GetSubstructMatches(sophorose_mol)
    if not matches:
        return False, "No sophorose moiety found"

    # Check for glycosidic linkage
    for match in matches:
        for atom_idx in match:
            atom = mol.GetAtomWithIdx(atom_idx)
            if atom.GetSymbol() == 'O':
                neighbors = atom.GetNeighbors()
                if len(neighbors) > 1:
                    return True, "Sophoroside found"

    return False, "No glycosidic linkage found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:145470',
                          'name': 'sophoroside',
                          'definition': 'Any glycoside of sophorose '
                                        '(2-O-beta-D-glucopyranosyl-D-glucopyranose).',
                          'parents': ['CHEBI:24400', 'CHEBI:63353']},
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