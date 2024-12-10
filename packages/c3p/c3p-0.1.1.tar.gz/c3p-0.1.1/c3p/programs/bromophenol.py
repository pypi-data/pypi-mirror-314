"""
Classifies: CHEBI:33624 bromophenol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_bromophenol(smiles: str):
    """
    Determines if a molecule is a bromophenol (a phenol containing one or more covalently bonded bromine atoms).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a bromophenol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for phenol substructure
    phenol_pattern = Chem.MolFromSmarts('c1ccc(O)cc1')
    phenol_match = mol.GetSubstructMatches(phenol_pattern)
    if not phenol_match:
        return False, "No phenol substructure found"

    # Check for bromine atoms
    bromine_atoms = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetAtomicNum() == 35]
    if not bromine_atoms:
        return False, "No bromine atoms found"

    # Check if bromine atoms are covalently bonded to the phenol ring
    for phenol_ring in phenol_match:
        phenol_ring_atoms = set(phenol_ring)
        for bromine_idx in bromine_atoms:
            bromine_neighbors = set([neighbor.GetIdx() for neighbor in mol.GetAtomWithIdx(bromine_idx).GetNeighbors()])
            if bromine_neighbors.intersection(phenol_ring_atoms):
                return True, "Bromophenol found"

    return False, "Bromine atoms not covalently bonded to the phenol ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33624',
                          'name': 'bromophenol',
                          'definition': 'A halophenol that is any phenol '
                                        'containing one or more covalently '
                                        'bonded bromine atoms.',
                          'parents': ['CHEBI:37149', 'CHEBI:38856']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: 'int' object is not iterable",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 35702,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.9972069379660923}