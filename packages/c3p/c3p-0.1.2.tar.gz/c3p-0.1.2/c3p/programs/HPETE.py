"""
Classifies: CHEBI:24644 HPETE
"""
from rdkit import Chem
from rdkit.Chem import Descriptors

def is_HPETE(smiles: str):
    """
    Determines if a molecule is a mono-hydroperoxy (e)icosatetraenoic acid (HPETE).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a HPETE, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for exactly 20 carbon atoms
    if Descriptors.HeavyAtomCount(mol) != 22:
        return False, "Molecule does not have 22 heavy atoms (20 carbons)"

    # Check for exactly 4 double bonds
    if Descriptors.BondCount(mol, Descriptors.BondType.DOUBLE) != 4:
        return False, "Molecule does not have 4 double bonds"

    # Check for exactly 1 hydroperoxy group (-OO)
    hydroperoxy_count = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetTotalDegree() == 1:
            neighbor = atom.GetNeighbors()[0]
            if neighbor.GetSymbol() == 'O':
                hydroperoxy_count += 1

    if hydroperoxy_count != 1:
        return False, "Molecule does not have exactly 1 hydroperoxy group"

    # Check for exactly 1 carboxylic acid group (-COOH)
    carboxylic_count = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetTotalDegree() == 3:
            neighbors = atom.GetNeighbors()
            if sum(n.GetSymbol() == 'O' for n in neighbors) == 2 and sum(n.GetSymbol() == 'O' and n.GetTotalDegree() == 1 for n in neighbors) == 1:
                carboxylic_count += 1

    if carboxylic_count != 1:
        return False, "Molecule does not have exactly 1 carboxylic acid group"

    return True, "Molecule is a mono-hydroperoxy (e)icosatetraenoic acid (HPETE)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24644',
                          'name': 'HPETE',
                          'definition': 'Mono-hydroperoxy (e)icosatetraenoic '
                                        'acids (HPETEs) are the primary '
                                        'products of lipoxygenase-catalysed '
                                        'oxygenation of arachidonic acid.',
                          'parents': ['CHEBI:189832', 'CHEBI:23899']},
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
    'success': False,
    'best': True,
    'error': "module 'rdkit.Chem.Descriptors' has no attribute 'BondCount'",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}