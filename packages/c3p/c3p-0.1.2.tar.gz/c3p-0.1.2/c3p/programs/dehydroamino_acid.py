"""
Classifies: CHEBI:23591 dehydroamino acid
"""
from rdkit import Chem

def is_dehydroamino_acid(smiles: str):
    """
    Determines if a molecule is a dehydroamino acid, which is defined as an amino acid derivative
    that is an amino acid whose side-chain has undergone formal dehydrogenation.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a dehydroamino acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of an amino group
    amino_group = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N' and atom.GetTotalNumHs() == 2:
            amino_group = True
            break

    if not amino_group:
        return False, "No amino group found"

    # Check for the presence of a carboxylic acid group
    carboxylic_acid = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetDegree() == 3:
            neighbors = [mol.GetAtomWithIdx(nbr.GetIdx()).GetSymbol() for nbr in atom.GetNeighbors()]
            if 'O' in neighbors and 'O' in neighbors:
                carboxylic_acid = True
                break

    if not carboxylic_acid:
        return False, "No carboxylic acid group found"

    # Check for the presence of an alkene (double bond)
    alkene = False
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.DOUBLE:
            alkene = True
            break

    if not alkene:
        return False, "No alkene (double bond) found"

    return True, "The molecule is a dehydroamino acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23591',
                          'name': 'dehydroamino acid',
                          'definition': 'An amino acid derivative that is an '
                                        'amino acid whose side-chain has '
                                        'undergone formal dehydrogenation.',
                          'parents': ['CHEBI:83821']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: Python argument types in\n'
               '    Mol.GetAtomWithIdx(Mol, Atom)\n'
               'did not match C++ signature:\n'
               '    GetAtomWithIdx(RDKit::ROMol {lvalue} self, unsigned int '
               'idx)',
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 473,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.8257839721254355}