"""
Classifies: CHEBI:24838 inorganic phosphate
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_inorganic_phosphate(smiles: str):
    """
    Determines if a molecule is an inorganic phosphate (contains phosphate but no carbon).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an inorganic phosphate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if molecule contains a phosphate group
    has_phosphate = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'P':
            neighbors = atom.GetNeighbors()
            oxygens = [n for n in neighbors if n.GetSymbol() == 'O']
            if len(oxygens) >= 3:
                has_phosphate = True
                break

    if not has_phosphate:
        return False, "No phosphate group found"

    # Check if molecule contains carbon atoms
    has_carbon = any(atom.GetSymbol() == 'C' for atom in mol.GetAtoms())
    if has_carbon:
        return False, "Molecule contains carbon atoms"

    return True, "Inorganic phosphate"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24838',
                          'name': 'inorganic phosphate',
                          'definition': 'Any  phosphate that contains no '
                                        'carbon atom.',
                          'parents': ['CHEBI:24835', 'CHEBI:26020']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'True positives: []\n'
               "False positives: [('P(N)(=N)=N', 'Inorganic phosphate'), "
               "('NP(O)O', 'Inorganic phosphate'), ('NP(O)(O)=O', 'Inorganic "
               "phosphate'), ('[H]P([H])P([H])P([H])[H]', 'Inorganic "
               "phosphate')]\n"
               "False negatives: [('[Na+].OP(O)([O-])=O', 'No phosphate group "
               "found')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 87,
    'num_true_negatives': 183832,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.011363636363636364,
    'recall': 1.0,
    'f1': 0.02247191011235955,
    'accuracy': 0.999526968247064}