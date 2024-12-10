"""
Classifies: CHEBI:33704 alpha-amino acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_alpha_amino_acid(smiles: str):
    """
    Determines if a molecule is an alpha-amino acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an alpha-amino acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Identify the amino and carboxyl groups
    amino_groups = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == 'N' and atom.GetTotalNumHs() == 2]
    carboxyl_groups = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == 'C' and atom.GetTotalNumHs() == 0 and sum(bond.GetBondTypeAsDouble() == 2 for bond in atom.GetBonds()) == 2]

    if not amino_groups or not carboxyl_groups:
        return False, "No amino or carboxyl group found"

    # Check if amino group is alpha to carboxyl group
    for amino_idx in amino_groups:
        for carboxyl_idx in carboxyl_groups:
            amino_atom = mol.GetAtomWithIdx(amino_idx)
            carboxyl_atom = mol.GetAtomWithIdx(carboxyl_idx)
            path = Chem.GetShortestPath(mol, amino_idx, carboxyl_idx)
            if len(path) == 3 and mol.GetAtomWithIdx(path[1]).GetTotalNumHs() == 1:
                return True, "Alpha-amino acid identified"

    return False, "No alpha-amino acid found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33704',
                          'name': 'alpha-amino acid',
                          'definition': 'An amino acid in which the amino '
                                        'group is located on the carbon atom '
                                        'at the position alpha to the carboxy '
                                        'group.',
                          'parents': ['CHEBI:33709']},
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
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 100,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.0}