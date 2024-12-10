"""
Classifies: CHEBI:176843 vitamin B12
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_vitamin_B12(smiles: str):
    """
    Determines if a molecule is a vitamin B12 or one of its vitamers.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a vitamin B12 vitamer, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a cobalt atom
    has_cobalt = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'Co':
            has_cobalt = True
            break

    if not has_cobalt:
        return False, "No cobalt atom found"

    # Check for the corrin ring system
    corrin_ring_atoms = []
    corrin_ring_bond_orders = []

    # Define the expected corrin ring atom symbols and bond orders
    expected_corrin_ring_atoms = ['C', 'C', 'C', 'N', 'C', 'C', 'C', 'N', 'C', 'C', 'C', 'N', 'C', 'C', 'C', 'N']
    expected_corrin_ring_bond_orders = [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1]

    # Find the corrin ring system
    for ring in mol.GetRingInfo().AtomRings():
        if len(ring) == 16:
            ring_atoms = [mol.GetAtomWithIdx(idx) for idx in ring]
            ring_bond_orders = [mol.GetBondBetweenAtoms(ring_atoms[i].GetIdx(), ring_atoms[(i + 1) % 16].GetIdx()).GetBondType() for i in range(16)]

            if [atom.GetSymbol() for atom in ring_atoms] == expected_corrin_ring_atoms and ring_bond_orders == expected_corrin_ring_bond_orders:
                corrin_ring_atoms = ring_atoms
                corrin_ring_bond_orders = ring_bond_orders
                break

    if not corrin_ring_atoms:
        return False, "No corrin ring system found"

    # Check for the presence of substituents characteristic of vitamin B12 vitamers
    substituents = []
    for atom in mol.GetAtoms():
        if atom not in corrin_ring_atoms:
            symbol = atom.GetSymbol()
            if symbol in ['N', 'O', 'C']:
                substituents.append(symbol)

    if 'N' in substituents and 'O' in substituents and 'C' in substituents:
        return True, "Molecule is a vitamin B12 vitamer"
    else:
        return False, "Substituents not characteristic of vitamin B12 vitamers"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:176843',
                          'name': 'vitamin B12',
                          'definition': 'Any member of a group of cobalamin '
                                        'vitamers that exhibit biological '
                                        'activity against vitamin B12 '
                                        'deficiency. Vitamin B12 deficiency is '
                                        'associated with low red blood cell '
                                        'count and anemia. The vitamers are '
                                        'found in foods such as cereals, meat, '
                                        'fish, and poultry. The vitamers '
                                        'include adenosylcobalamin, '
                                        'hydroxocobalamin, cyanocobalamin, '
                                        'aquacobalamin, nitritocobalamin and '
                                        'methylcobabalamin (also includes '
                                        'their ionized, salt and phosphate '
                                        'derivatives).',
                          'parents': ['CHEBI:75769']},
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
    'num_true_negatives': 183924,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945630012234}