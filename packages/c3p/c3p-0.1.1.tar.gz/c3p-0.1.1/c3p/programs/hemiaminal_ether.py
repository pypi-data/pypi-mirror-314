"""
Classifies: CHEBI:141498 hemiaminal ether
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hemiaminal_ether(smiles: str):
    """
    Determines if a molecule is a hemiaminal ether.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a hemiaminal ether, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find the nitrogen atoms
    nitrogen_atoms = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == 'N']

    # Check if there is at least one nitrogen atom
    if not nitrogen_atoms:
        return False, "No nitrogen atoms found"

    # Check if the nitrogen atom is connected to an oxygen and two carbons
    for nitrogen_idx in nitrogen_atoms:
        nitrogen_atom = mol.GetAtomWithIdx(nitrogen_idx)
        neighbors = [mol.GetAtomWithIdx(neighbor.GetIdx()) for neighbor in nitrogen_atom.GetNeighbors()]

        if len(neighbors) != 3:
            continue

        oxygen_neighbors = [neighbor for neighbor in neighbors if neighbor.GetSymbol() == 'O']
        carbon_neighbors = [neighbor for neighbor in neighbors if neighbor.GetSymbol() == 'C']

        if len(oxygen_neighbors) == 1 and len(carbon_neighbors) == 2:
            # Check if the oxygen is connected to a carbon
            oxygen_idx = oxygen_neighbors[0].GetIdx()
            oxygen_atom = mol.GetAtomWithIdx(oxygen_idx)
            oxygen_neighbors = [mol.GetAtomWithIdx(neighbor.GetIdx()) for neighbor in oxygen_atom.GetNeighbors()]
            carbon_neighbors_of_oxygen = [neighbor for neighbor in oxygen_neighbors if neighbor.GetSymbol() == 'C']

            if carbon_neighbors_of_oxygen:
                return True, "Molecule is a hemiaminal ether"

    return False, "Molecule is not a hemiaminal ether"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:141498',
                          'name': 'hemiaminal ether',
                          'definition': 'An organic amino compound that is a '
                                        'hemiaminal in which the hydrogen atom '
                                        'of the hydroxy group has been '
                                        'replaced by an organyl group. General '
                                        "formula: R2C(OR')NR2 ( R =/= H ). "
                                        'Also known as alpha-amino ethers.',
                          'parents': ['CHEBI:36963', 'CHEBI:50047']},
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
    'num_false_positives': 100,
    'num_true_negatives': 52888,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9980939440261186}