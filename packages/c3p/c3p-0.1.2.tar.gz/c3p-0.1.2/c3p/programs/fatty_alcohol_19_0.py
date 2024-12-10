"""
Classifies: CHEBI:197469 fatty alcohol 19:0
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_fatty_alcohol_19_0(smiles: str):
    """
    Determines if a molecule is a fatty alcohol 19:0 (containing 19 carbon atoms and an alcohol group).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a fatty alcohol 19:0, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of an alcohol group (-OH)
    alcohol_atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and
                     atom.GetTotalNumHs() == 1]
    if not alcohol_atoms:
        return False, "Molecule does not contain an alcohol group (-OH)"

    # Check if the alcohol group is connected to a carbon chain of 19 atoms
    for alcohol_atom in alcohol_atoms:
        carbon_chain = set()
        carbon_chain.add(alcohol_atom.GetIdx())
        dfs_traversal(mol, alcohol_atom, carbon_chain)
        if len(carbon_chain) == 20:  # Including the alcohol oxygen
            carbon_count = sum(1 for idx in carbon_chain if mol.GetAtomWithIdx(idx).GetSymbol() == 'C')
            if carbon_count == 19:
                return True, "Molecule is a fatty alcohol 19:0"

    return False, "Alcohol group is not connected to a carbon chain of 19 atoms"

def dfs_traversal(mol, atom, visited):
    """
    Performs a depth-first search (DFS) traversal of the molecular graph starting from the given atom.

    Args:
        mol (Mol): RDKit molecule object
        atom (Atom): Starting atom for the DFS traversal
        visited (set): Set of visited atom indices
    """
    visited.add(atom.GetIdx())
    for neighbor in atom.GetNeighbors():
        if neighbor.GetIdx() not in visited:
            dfs_traversal(mol, neighbor, visited)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:197469',
                          'name': 'fatty alcohol 19:0',
                          'definition': 'Any fatty alcohol containing 19 '
                                        'carbons.',
                          'parents': ['CHEBI:17135']},
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
               "False negatives: [('CCCCCCCCCCCCCCCCCC(C)O', 'Molecule does "
               "not contain an alcohol group (-OH)')]",
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 17,
    'num_true_negatives': 183908,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.05555555555555555,
    'recall': 1.0,
    'f1': 0.10526315789473684,
    'accuracy': 0.99990757152333}