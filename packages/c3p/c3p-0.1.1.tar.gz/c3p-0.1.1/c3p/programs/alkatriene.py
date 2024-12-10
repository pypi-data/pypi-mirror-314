"""
Classifies: CHEBI:33647 alkatriene
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_alkatriene(smiles: str):
    """
    Determines if a molecule is an alkatriene (acyclic branched or unbranched hydrocarbons having three carbon-carbon double bonds).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an alkatriene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule is acyclic
    if mol.GetRingInfo().NumRings() > 0:
        return False, "Molecule is cyclic"

    # Check if the molecule contains only C and H atoms
    if not all(atom.GetAtomicNum() in (1, 6) for atom in mol.GetAtoms()):
        return False, "Molecule contains atoms other than C and H"

    # Count the number of double bonds
    num_double_bonds = sum(bond.GetIsAromatic() == 0 and bond.GetBondType() == Chem.BondType.DOUBLE for bond in mol.GetBonds())

    # Check if the molecule has exactly three double bonds
    if num_double_bonds != 3:
        return False, f"Molecule does not have exactly 3 double bonds"

    # Check if the double bonds are non-cumulative
    double_bond_atoms = set()
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.DOUBLE:
            double_bond_atoms.update([bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()])

    if len(double_bond_atoms) != num_double_bonds * 2:
        return False, "Double bonds are cumulative or conjugated"

    return True, "Molecule is an alkatriene"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33647',
                          'name': 'alkatriene',
                          'definition': 'Acyclic branched or unbranched '
                                        'hydrocarbons having three '
                                        'carbon-carbon double bonds.',
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
               'Attempt failed: F1 score of 0.16 is too low.\n'
               "True positives: [('C(CC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)CCC', "
               "'Molecule is an alkatriene'), "
               "('C(CCCC/C=C\\\\C/C=C\\\\CCCCC)CCCCC=C', 'Molecule is an "
               "alkatriene')]\n"
               "False positives: [('C(CC)/C=C(/C=C(\\\\CC)/C=C/CC)\\\\C', "
               "'Molecule is an alkatriene'), "
               "('C(CCC=C)C/C=C\\\\C#CC#C\\\\C=C\\\\C', 'Molecule is an "
               "alkatriene'), ('CC(C)=CC\\\\C=C(\\\\C)C=C', 'Molecule is an "
               "alkatriene'), ('CC(=C/C=C/C(=C/C)/C)C', 'Molecule is an "
               "alkatriene'), ('C(CC/C=C/CC#CC#C/C=C\\\\C)CCC=C', 'Molecule is "
               "an alkatriene'), ('C(C)(C)(/C=C/C(C)=C)C=C', 'Molecule is an "
               "alkatriene'), ('C(C/C(=C/CC)/C)\\\\C=C(\\\\CCC=C(C)C)/C', "
               "'Molecule is an alkatriene'), ('CC(C)=CC\\\\C=C(/C)C=C', "
               "'Molecule is an alkatriene'), "
               "('C(=C\\\\C=C\\\\C(\\\\C)=C/C)(C)C', 'Molecule is an "
               "alkatriene'), ('C(CCC=C(C)C)(C/C=C/C(/C)=C/C)C', 'Molecule is "
               "an alkatriene'), ('C(C/C=C(/CC)\\\\C)/C(=C/CC=C(CC)CC)/C', "
               "'Molecule is an alkatriene'), ('C(C=C(C)C)(C(C)=C)C=C', "
               "'Molecule is an alkatriene'), "
               "('CC\\\\C=C\\\\C=C\\\\C#CC#C\\\\C=C\\\\C', 'Molecule is an "
               "alkatriene'), ('CC=CC#CC#CC#CC=CC=C', 'Molecule is an "
               "alkatriene'), ('C=C=C=C', 'Molecule is an alkatriene'), "
               "('CC(C)=CCCC(=C)C=C', 'Molecule is an alkatriene'), "
               "('C(CCC=C)C/C=C/C=C/C#CC#CC#CC', 'Molecule is an alkatriene'), "
               "('CC(=CCC=C(C=C)C)C', 'Molecule is an alkatriene'), "
               "('C(\\\\CC)(=C\\\\C(\\\\C)=C\\\\C)/C=C/CC', 'Molecule is an "
               "alkatriene'), ('C(C)(C)=C.C(C)(C=C)=C', 'Molecule is an "
               "alkatriene'), ('C(\\\\CC)(=C\\\\C(=C\\\\CC)\\\\C)/C=C/CC', "
               "'Molecule is an alkatriene')]\n"
               'False negatives: []',
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 20,
    'num_true_negatives': 183889,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.09090909090909091,
    'recall': 1.0,
    'f1': 0.16666666666666669,
    'accuracy': 0.9998912517467688}