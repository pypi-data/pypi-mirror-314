"""
Classifies: CHEBI:24862 iodoamino acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_iodoamino_acid(smiles: str):
    """
    Determines if a molecule is an iodoamino acid (an amino acid containing at least one iodo substituent).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an iodoamino acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains an amino group
    has_amino_group = any(atom.GetSymbol() == 'N' and
                          sum(atom.GetTotalNumHs() for atom in atom.GetNeighbors()) == 2
                          for atom in mol.GetAtoms())
    if not has_amino_group:
        return False, "Molecule does not contain an amino group"

    # Check if the molecule contains a carboxyl group
    has_carboxyl_group = any(atom.GetSymbol() == 'C' and atom.GetFormalCharge() == 0 and
                             sum(neighbor.GetSymbol() == 'O' for neighbor in atom.GetNeighbors()) == 2
                             for atom in mol.GetAtoms())
    if not has_carboxyl_group:
        return False, "Molecule does not contain a carboxyl group"

    # Check if the molecule contains at least one iodine atom
    has_iodine = any(atom.GetSymbol() == 'I' for atom in mol.GetAtoms())
    if not has_iodine:
        return False, "Molecule does not contain any iodine atoms"

    return True, "Molecule is an iodoamino acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24862',
                          'name': 'iodoamino acid',
                          'definition': 'An amino acid containing at least one '
                                        'iodo substituent.',
                          'parents': ['CHEBI:24470', 'CHEBI:37142']},
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
    'num_false_positives': 18,
    'num_true_negatives': 183904,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9998966958999146}