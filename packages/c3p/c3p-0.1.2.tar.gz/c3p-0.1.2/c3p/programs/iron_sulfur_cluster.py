"""
Classifies: CHEBI:30408 iron-sulfur cluster
"""
from rdkit import Chem

def is_iron_sulfur_cluster(smiles: str):
    """
    Determines if a molecule is an iron-sulfur cluster.

    An iron-sulfur cluster is a unit comprising two or more iron atoms and bridging sulfur ligands.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an iron-sulfur cluster, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count the number of iron and sulfur atoms
    iron_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'Fe')
    sulfur_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'S')

    # Check if there are at least two iron atoms and one sulfur atom
    if iron_count < 2 or sulfur_count < 1:
        return False, "Not enough iron or sulfur atoms"

    # Check if there are sulfur atoms bridging iron atoms
    iron_atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'Fe']
    has_bridging_sulfur = False

    for iron_atom in iron_atoms:
        neighbors = [mol.GetAtomWithIdx(neighbor_idx) for neighbor_idx in iron_atom.GetNeighbors()]
        if any(neighbor.GetSymbol() == 'S' for neighbor in neighbors):
            sulfur_neighbors = [neighbor for neighbor in neighbors if neighbor.GetSymbol() == 'S']
            if any(sulfur_neighbor.GetDegree() > 2 for sulfur_neighbor in sulfur_neighbors):
                has_bridging_sulfur = True
                break

    if not has_bridging_sulfur:
        return False, "No bridging sulfur atoms found"

    return True, "Molecule is an iron-sulfur cluster"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:30408',
                          'name': 'iron-sulfur cluster',
                          'definition': 'An iron-sulfur cluster is a unit '
                                        'comprising two or more iron atoms and '
                                        'bridging sulfur ligands.',
                          'parents': ['CHEBI:25214', 'CHEBI:33892']},
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
    'error': 'Python argument types in\n'
             '    Mol.GetAtomWithIdx(Mol, Atom)\n'
             'did not match C++ signature:\n'
             '    GetAtomWithIdx(RDKit::ROMol {lvalue} self, unsigned int idx)',
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