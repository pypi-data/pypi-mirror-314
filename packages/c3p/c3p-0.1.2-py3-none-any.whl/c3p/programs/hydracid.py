"""
Classifies: CHEBI:33405 hydracid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hydracid(smiles: str):
    """
    Determines if a molecule is a hydracid, which contains hydrogen that is not bound to oxygen
    and produces a conjugate base by loss of positive hydrogen ion(s).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hydracid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for hydrogen atoms
    hydrogen_atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'H']
    if not hydrogen_atoms:
        return False, "No hydrogen atoms found"

    # Check if hydrogen is not bound to oxygen
    for h_atom in hydrogen_atoms:
        for neighbor in h_atom.GetNeighbors():
            if neighbor.GetSymbol() == 'O':
                return False, "Hydrogen atom is bound to oxygen"

    # Check if hydrogen can be removed to form a conjugate base
    conjugate_base = Chem.RemoveHs(mol)
    if not conjugate_base:
        return False, "Unable to form conjugate base by removing hydrogen"

    return True, "This molecule is a hydracid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33405',
                          'name': 'hydracid',
                          'definition': 'A hydracid is a compound which '
                                        'contains hydrogen that is not bound '
                                        'to oxygen, and which produces a '
                                        'conjugate base by loss of positive '
                                        'hydrogen ion(s) (hydrons).',
                          'parents': ['CHEBI:33608']},
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
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 0,
    'num_false_positives': 100,
    'num_true_negatives': 57822,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9982390718873007}