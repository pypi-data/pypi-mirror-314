"""
Classifies: CHEBI:33338 aryl group
"""
from rdkit import Chem

def is_aryl_group(smiles: str):
    """
    Determines if a molecule is an aryl group.

    An aryl group is a group derived from an arene by removal of a hydrogen atom
    from a ring carbon atom.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an aryl group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for aromatic rings
    aromatic_rings = [ring for ring in mol.GetRingInfo().AtomRings() if all(mol.GetAtomWithIdx(idx).GetIsAromatic() for idx in ring)]
    if not aromatic_rings:
        return False, "No aromatic rings found"

    # Check if there is an aromatic carbon attached to a non-hydrogen atom
    for ring in aromatic_rings:
        for atom_idx in ring:
            atom = mol.GetAtomWithIdx(atom_idx)
            if atom.GetSymbol() == 'C' and atom.GetIsAromatic():
                for neighbor in atom.GetNeighbors():
                    if neighbor.GetSymbol() != 'H':
                        return True, "Aromatic carbon attached to a non-hydrogen atom"

    return False, "No aromatic carbon attached to a non-hydrogen atom"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33338',
                          'name': 'aryl group',
                          'definition': 'A group derived from an arene by '
                                        'removal of a hydrogen atom from a '
                                        'ring carbon atom.',
                          'parents': ['CHEBI:33248']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: module 'rdkit.Chem.AllChem' has no attribute "
               "'IsAromaticRing'",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 76,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.4350282485875706}