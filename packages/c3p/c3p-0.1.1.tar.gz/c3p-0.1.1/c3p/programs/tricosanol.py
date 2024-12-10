"""
Classifies: CHEBI:197527 tricosanol
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_tricosanol(smiles: str):
    """
    Determines if a molecule is a tricosanol (a fatty alcohol with a hydroxy function
    at any position of an unbranched saturated chain of twenty-three carbon atoms).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a tricosanol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for a single hydroxyl group
    hydroxy_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')
    if hydroxy_count != 1:
        return False, "Molecule does not contain exactly one hydroxyl group"

    # Check for an unbranched alkyl chain of 23 carbon atoms
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count != 23:
        return False, "Molecule does not contain an alkyl chain of 23 carbon atoms"

    # Check if the alkyl chain is unbranched and saturated
    if rdMolDescriptors.CalcNumAliphaticRings(mol) > 0:
        return False, "Molecule contains a cyclic structure"
    if rdMolDescriptors.CalcNumAromaticRings(mol) > 0:
        return False, "Molecule contains an aromatic ring"
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            if atom.GetDegree() > 4:
                return False, "Molecule contains a branched alkyl chain"
            elif atom.GetDegree() == 4:
                neighbors = [n.GetSymbol() for n in atom.GetNeighbors()]
                if 'O' not in neighbors:
                    return False, "Molecule contains a branched alkyl chain"

    # Check if the hydroxyl group is attached to the carbon chain
    hydroxy_atom = next(atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')
    if hydroxy_atom.GetDegree() != 1:
        return False, "Hydroxyl group is not attached to the alkyl chain"

    return True, "Molecule is a tricosanol"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:197527',
                          'name': 'tricosanol',
                          'definition': 'A fatty alcohol consisting of a '
                                        'hydroxy function at any position of '
                                        'an unbranched saturated chain of '
                                        'twenty-three carbon atoms.',
                          'parents': [   'CHEBI:134179',
                                         'CHEBI:197528',
                                         'CHEBI:50584']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'True positives: []\n'
               'False positives: []\n'
               "False negatives: [('CCCCCCCCCCCCCCC(O)CCCCCCCC', 'Molecule "
               "contains a branched alkyl chain')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 6,
    'num_true_negatives': 183917,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.14285714285714285,
    'recall': 1.0,
    'f1': 0.25,
    'accuracy': 0.9999673778299732}