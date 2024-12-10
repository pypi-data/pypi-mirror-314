"""
Classifies: CHEBI:149742 N-(fatty acyl)-glycine(1-)
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_N__fatty_acyl__glycine_1__(smiles: str):
    """
    Determines if a molecule is an N-(fatty acyl)-glycine(1-).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an N-(fatty acyl)-glycine(1-), False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for presence of a carboxylate group
    carboxylate_present = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == -1:
            neighbor = atom.GetNeighbors()[0]
            if neighbor.GetSymbol() == 'C' and neighbor.GetFormalCharge() == 0:
                carboxylate_present = True
                break
    if not carboxylate_present:
        return False, "No carboxylate group found"

    # Check for presence of an amide group
    amide_present = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N' and atom.GetFormalCharge() == 0:
            neighbors = atom.GetNeighbors()
            if len(neighbors) == 2:
                if neighbors[0].GetSymbol() == 'C' and neighbors[1].GetSymbol() == 'C':
                    amide_present = True
                    break
    if not amide_present:
        return False, "No amide group found"

    # Check for the presence of a fatty acyl chain
    fatty_acyl_chain = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and len(atom.GetNeighbors()) == 2:
            neighbors = atom.GetNeighbors()
            if neighbors[0].GetSymbol() == 'C' and neighbors[1].GetSymbol() == 'C':
                fatty_acyl_chain = True
                break
    if not fatty_acyl_chain:
        return False, "No fatty acyl chain found"

    return True, "N-(fatty acyl)-glycine(1-)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:149742',
                          'name': 'N-(fatty acyl)-glycine(1-)',
                          'definition': 'an N-acyl-glycine where the fatty '
                                        'acyl chain is not specified, major '
                                        'species at pH 7.3.',
                          'parents': ['CHEBI:136716', 'CHEBI:57670']},
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
    'error': 'tuple index out of range',
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