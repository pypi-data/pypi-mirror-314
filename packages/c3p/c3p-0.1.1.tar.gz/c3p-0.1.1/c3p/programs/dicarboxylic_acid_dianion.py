"""
Classifies: CHEBI:28965 dicarboxylic acid dianion
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_dicarboxylic_acid_dianion(smiles: str):
    """
    Determines if a molecule is a dicarboxylic acid dianion.

    A dicarboxylic acid dianion is a carboxylic acid dianion obtained by deprotonation
    of both carboxy groups of any dicarboxylic acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a dicarboxylic acid dianion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count the number of carboxylate groups
    carboxylates = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == -1:
            carboxylates += 1

    if carboxylates != 2:
        return False, "The molecule does not have exactly two carboxylate groups"

    # Check if the carboxylate groups are part of a dicarboxylic acid
    for bond in mol.GetBonds():
        a1 = bond.GetBeginAtom()
        a2 = bond.GetEndAtom()
        if a1.GetSymbol() == 'C' and a2.GetSymbol() == 'C':
            neighbors_a1 = [n.GetSymbol() for n in a1.GetNeighbors()]
            neighbors_a2 = [n.GetSymbol() for n in a2.GetNeighbors()]
            if 'O' in neighbors_a1 and 'O' in neighbors_a2:
                # Found a dicarboxylic acid
                return True, "The molecule is a dicarboxylic acid dianion"

    return False, "The molecule does not contain a dicarboxylic acid group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28965',
                          'name': 'dicarboxylic acid dianion',
                          'definition': 'A carboxylic acid dianion obtained by '
                                        'deprotonation of both carboxy groups '
                                        'of any dicarboxylic acid.',
                          'parents': ['CHEBI:35693', 'CHEBI:38716']},
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
    'num_true_positives': 16,
    'num_false_positives': 100,
    'num_true_negatives': 10435,
    'num_false_negatives': 22,
    'num_negatives': None,
    'precision': 0.13793103448275862,
    'recall': 0.42105263157894735,
    'f1': 0.20779220779220778,
    'accuracy': 0.9884611746902487}