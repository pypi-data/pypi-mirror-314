"""
Classifies: CHEBI:15732 phosphonoacetic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_phosphonoacetic_acid(smiles: str):
    """
    Determines if a molecule is a phosphonoacetic acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a phosphonoacetic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find phosphorous atoms
    p_atoms = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == 'P']

    if len(p_atoms) == 0:
        return False, "No phosphorous atom found"
    elif len(p_atoms) > 1:
        return False, "Multiple phosphorous atoms found"

    p_atom_idx = p_atoms[0]
    p_atom = mol.GetAtomWithIdx(p_atom_idx)

    # Check for phosphonate group
    if p_atom.GetTotalNumHs() > 0:
        return False, "Phosphorous atom has hydrogen atoms attached"

    # Check for carboxymethyl substituent
    carboxymethyl_found = False
    for neighbor in p_atom.GetNeighbors():
        if neighbor.GetSymbol() == 'C':
            adj_atoms = [mol.GetAtomWithIdx(n.GetIdx()) for n in neighbor.GetNeighbors()]
            if any(a.GetSymbol() == 'O' and a.GetTotalNumHs() == 0 for a in adj_atoms):
                carboxymethyl_found = True
                break

    if not carboxymethyl_found:
        return False, "No carboxymethyl group attached to phosphorous"

    return True, "The molecule is a phosphonoacetic acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:15732',
                          'name': 'phosphonoacetic acid',
                          'definition': 'A member of the class of phosphonic '
                                        'acids that is phosphonic acid in '
                                        'which the hydrogen attached to the '
                                        'phosphorous is replaced by a '
                                        'carboxymethyl group.',
                          'parents': ['CHEBI:25384', 'CHEBI:26069']},
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
    'num_false_positives': 35,
    'num_true_negatives': 183883,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.999804261658665}