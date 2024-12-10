"""
Classifies: CHEBI:23775 dihydroxy-5beta-cholanic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_dihydroxy_5beta_cholanic_acid(smiles: str):
    """
    Determines if a molecule is a dihydroxy-5beta-cholanic acid, which is defined as a hydroxy-5beta-cholanic acid
    carrying two hydroxy groups at unspecified positions.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a dihydroxy-5beta-cholanic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule is a cholanic acid derivative
    is_cholanic_acid = AllChem.MolToSmiles(AllChem.RemoveHs(mol)) == 'C(C1CCC2C3CC(CC12)C4(C(CC3)CC(O)=O)CCC5(C)C(O)CCC45)C'
    if not is_cholanic_acid:
        return False, "Not a cholanic acid derivative"

    # Check if it has exactly two hydroxyl groups
    hydroxy_count = sum(atom.GetTotalNumHs(onlyExplicit=False) for atom in mol.GetAtoms())
    if hydroxy_count != 2:
        return False, "Does not have exactly two hydroxy groups"

    # Check if it has a 5-beta configuration
    ring_atoms = mol.GetRingInfo().AtomRings()[0]
    junc_atom = mol.GetAtomWithIdx(ring_atoms[5])
    neighbors = [mol.GetAtomWithIdx(n) for n in junc_atom.GetNeighbors()]
    methyl_groups = sum(atom.GetTotalNumHs(onlyExplicit=False) == 9 for atom in neighbors)
    if methyl_groups != 1:
        return False, "Does not have a 5-beta configuration"

    return True, "Molecule is a dihydroxy-5beta-cholanic acid"

# Example usage
smiles = "[H][C@]12CC[C@@]3([H])[C@]4([H])CC[C@]([H])([C@H](C)CCC(O)=O)[C@@]4(C)[C@@H](O)C[C@]3([H])[C@@]1(C)CC[C@@H](O)C2"
result, reason = is_dihydroxy_5beta_cholanic_acid(smiles)
print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23775',
                          'name': 'dihydroxy-5beta-cholanic acid',
                          'definition': 'A hydroxy-5beta-cholanic acid '
                                        'carrying two hydroxy groups at '
                                        'unspecified positions.',
                          'parents': ['CHEBI:24663', 'CHEBI:85184']},
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
    'error': "Can't kekulize mol.  Unkekulized atoms: 0 1 2 3 4 5 6 7 9 10 11 "
             '13 14 15 16 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 '
             '35 36 37 38 39 41 42 44 45 46 47 48 50 51 53 54 55 56 57 58 59 '
             '60 61 69 70 71 72 73 74 75 76 78 80 81 82 83 88 89',
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