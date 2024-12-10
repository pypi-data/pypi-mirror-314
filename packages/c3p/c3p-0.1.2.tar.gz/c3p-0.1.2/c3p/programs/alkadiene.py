"""
Classifies: CHEBI:33646 alkadiene
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_alkadiene(smiles: str):
    """
    Determines if a molecule is an alkadiene (acyclic branched or unbranched hydrocarbons having two carbon-carbon double bonds).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an alkadiene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule is acyclic
    if mol.HasSubstructMatch(Chem.MolFromSmarts('[r]')):
        return False, "Molecule is cyclic"

    # Check if the molecule consists of carbon and hydrogen atoms only
    atoms = [atom.GetSymbol() for atom in mol.GetAtoms()]
    if any(atom not in ['C', 'H'] for atom in atoms):
        return False, "Molecule contains atoms other than carbon and hydrogen"

    # Count the number of double bonds
    double_bonds = sum(1 for bond in mol.GetBonds() if bond.GetBondType() == Chem.BondType.DOUBLE)
    if double_bonds != 2:
        return False, f"Molecule has {double_bonds} double bonds, expected 2"

    # Check if the double bonds are separated by at least one carbon atom
    double_bond_atoms = [bond.GetBeginAtomIdx() for bond in mol.GetBonds() if bond.GetBondType() == Chem.BondType.DOUBLE]
    double_bond_atoms.extend([bond.GetEndAtomIdx() for bond in mol.GetBonds() if bond.GetBondType() == Chem.BondType.DOUBLE])
    distances = [Chem.GetDistanceMatrix(mol)[i, j] for i, j in zip(double_bond_atoms[:-1], double_bond_atoms[1:])]
    if any(distance < 2 for distance in distances):
        return False, "Double bonds are not separated by at least one carbon atom"

    return True, "Molecule is an alkadiene"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33646',
                          'name': 'alkadiene',
                          'definition': 'Acyclic branched or unbranched '
                                        'hydrocarbons having two carbon-carbon '
                                        'double bonds.',
                          'parents': ['CHEBI:33645']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.17391304347826084 is too low.\n'
               "True positives: [('C(CCCC=C)CCCC=C', 'Molecule is an "
               "alkadiene'), ('C(CC=CC)C=CC', 'Molecule is an alkadiene')]\n"
               "False positives: [('C(CC=C(C)C)/C(/C)=C\\\\C', 'Molecule is an "
               "alkadiene'), ('C(C/C=C/C(/C)=C/C)(C)C', 'Molecule is an "
               "alkadiene'), ('C(/C=C/C=C(C)C)(C)C', 'Molecule is an "
               "alkadiene'), ('C(CCCC(CCCC(C=C)=C)C)(CCCC(C)C)C', 'Molecule is "
               "an alkadiene'), ('C=C=C', 'Molecule is an alkadiene'), "
               "('C(CC(C)=C)CC=C', 'Molecule is an alkadiene'), "
               "('C(C#C)#CC=C=C', 'Molecule is an alkadiene'), "
               "('C(\\\\CC)(=C/CC=C(C)C)/C', 'Molecule is an alkadiene'), "
               "('C(CC=C(C)C)/C(/C)=C/C', 'Molecule is an alkadiene'), "
               "('[C@@H](CCC[C@@H](CCCC(C)C)C)(CCC/C(=C/CC/C=C(/CCC[C@@H](CCC[C@@H](CCCC(C)C)C)C)\\\\C)/C)C', "
               "'Molecule is an alkadiene'), ('C(=C/C=C/C)(C)C', 'Molecule is "
               "an alkadiene'), ('C(CC)C=C(C(C)=C)C', 'Molecule is an "
               "alkadiene'), ('C(C(C/C=C/C)=C)(C)C', 'Molecule is an "
               "alkadiene'), ('C(\\\\CC=C)(=C/CC)/C', 'Molecule is an "
               "alkadiene'), ('C=C[C@@](C)(CCC=C(C)C)[H]', 'Molecule is an "
               "alkadiene'), ('C(CC)/C(/C)=C/C=C', 'Molecule is an "
               "alkadiene'), ('C(C=C(C)C)(C)C=C', 'Molecule is an alkadiene'), "
               "('CCCC/C=C/C=C', 'Molecule is an alkadiene'), "
               "('CCC(=C)\\\\C=C/CC(C)C', 'Molecule is an alkadiene')]\n"
               'False negatives: []',
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 9,
    'num_true_negatives': 183898,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.18181818181818182,
    'recall': 1.0,
    'f1': 0.3076923076923077,
    'accuracy': 0.9999510627538619}