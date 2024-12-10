"""
Classifies: CHEBI:133292 3-oxo fatty acid anion
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_3_oxo_fatty_acid_anion(smiles: str):
    """
    Determines if a molecule is a 3-oxo fatty acid anion, obtained by deprotonation of the carboxy group of any 3-oxo fatty acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a 3-oxo fatty acid anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has an anionic charge
    if Chem.GetFormalCharge(mol) != -1:
        return False, "Molecule does not have an anionic charge"

    # Find the carbonyl oxygen atom
    carbonyl_oxygen = None
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == 0 and atom.GetTotalNumHs() == 0:
            carbonyl_oxygen = atom
            break

    if carbonyl_oxygen is None:
        return False, "No carbonyl oxygen found"

    # Check if the carbonyl oxygen is attached to a carbon atom with a formal charge of 0
    carbonyl_carbon = None
    for neighbor in carbonyl_oxygen.GetNeighbors():
        if neighbor.GetSymbol() == 'C' and neighbor.GetFormalCharge() == 0:
            carbonyl_carbon = neighbor
            break

    if carbonyl_carbon is None:
        return False, "Carbonyl oxygen not attached to a neutral carbon"

    # Check if the carbon atom is part of a carboxylate group
    carboxylate_oxygen = None
    for neighbor in carbonyl_carbon.GetNeighbors():
        if neighbor.GetSymbol() == 'O' and neighbor.GetFormalCharge() == -1:
            carboxylate_oxygen = neighbor
            break

    if carboxylate_oxygen is None:
        return False, "No carboxylate group found"

    # Check if the carbon atom is the third carbon in the chain
    chain_length = 0
    current_atom = carbonyl_carbon
    while True:
        neighbors = [n for n in current_atom.GetNeighbors() if n.GetSymbol() == 'C' and n.GetFormalCharge() == 0]
        if len(neighbors) > 2:
            return False, "Carbon is not part of a linear chain"
        elif len(neighbors) == 2:
            chain_length += 1
            current_atom = [n for n in neighbors if n != current_atom][0]
        else:
            break

    if chain_length != 2:
        return False, "Carbonyl carbon is not the third carbon in the chain"

    return True, "Molecule is a 3-oxo fatty acid anion"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:133292',
                          'name': '3-oxo fatty acid anion',
                          'definition': 'An oxo fatty acid anion obtained by '
                                        'deprotonation of the carboxy group of '
                                        'any 3-oxo fatty acid.',
                          'parents': ['CHEBI:35973', 'CHEBI:59836']},
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
    'num_true_negatives': 183922,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945629421008}