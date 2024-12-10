"""
Classifies: CHEBI:26987 threonine derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdqueries

def is_threonine_derivative(smiles: str):
    """
    Determines if a molecule is a threonine derivative.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a threonine derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for threonine substructure
    threonine_substructure = Chem.MolFromSmarts('C[C@H](N)[C@H](O)C(O)=O')
    if not mol.HasSubstructMatch(threonine_substructure):
        return False, "Molecule does not contain threonine substructure"

    # Check for modifications
    modified = False
    reason = ""

    # Check for modifications at the amino group
    amino_pattern = Chem.MolFromSmarts('N[!H]')
    if mol.HasSubstructMatch(amino_pattern):
        modified = True
        reason = "Modified at amino group"

    # Check for modifications at the carboxy group
    carboxy_pattern = Chem.MolFromSmarts('C(=O)O[!H]')
    if mol.HasSubstructMatch(carboxy_pattern):
        modified = True
        if reason:
            reason += ", "
        reason += "Modified at carboxy group"

    # Check for heteroatom replacement
    for atom in mol.GetAtoms():
        if atom.GetSymbol() not in ['C', 'N', 'O', 'H']:
            modified = True
            if reason:
                reason += ", "
            reason += f"Contains heteroatom {atom.GetSymbol()}"
            break

    if modified:
        return True, reason
    else:
        return False, "Unmodified threonine (not a derivative)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26987',
                          'name': 'threonine derivative',
                          'definition': 'An amino acid derivative resulting '
                                        'from reaction of threonine at the '
                                        'amino group or the carboxy group, or '
                                        'from the replacement of any hydrogen '
                                        'of threonine by a heteroatom. The '
                                        'definition normally excludes peptides '
                                        'containing threonine residues.',
                          'parents': ['CHEBI:83821']},
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
    'num_true_negatives': 121105,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9991502211075176}