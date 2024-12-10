"""
Classifies: CHEBI:21437 Mo-molybdopterin cofactor
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_Mo_molybdopterin_cofactor(smiles: str):
    """
    Determines if a molecule is a Mo-molybdopterin cofactor.

    A Mo-molybdopterin cofactor is defined as a molybdopterin cofactor in which
    the coordinated metal is a mononuclear molybdenum or molybdate species.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a Mo-molybdopterin cofactor, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a molybdenum atom
    has_mo = any(atom.GetSymbol() == 'Mo' for atom in mol.GetAtoms())
    if not has_mo:
        return False, "No molybdenum atom found"

    # Check for the presence of a molybdopterin scaffold
    molybdopterin_scaffold = Chem.MolFromSmarts('[#7]1[#6]2[#6]([#6]([#6]([#6]2[#7][#6]1[#7])[#6])[#7])[#6]')
    if mol.GetSubstructMatch(molybdopterin_scaffold) == []:
        return False, "Molybdopterin scaffold not found"

    # Check for coordination of molybdenum to the molybdopterin scaffold
    mo_atom = next((atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'Mo'), None)
    if mo_atom is None:
        return False, "No molybdenum atom found"

    scaffold_atoms = mol.GetSubstructMatch(molybdopterin_scaffold)
    for atom_idx in scaffold_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        if atom in mo_atom.GetNeighbors():
            return True, "Mo-molybdopterin cofactor identified"

    return False, "Molybdenum not coordinated to molybdopterin scaffold"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:21437',
                          'name': 'Mo-molybdopterin cofactor',
                          'definition': 'A molybdopterin cofactor in which the '
                                        'coordinated metal is a mononuclear '
                                        'molybdenum or molybdate species.',
                          'parents': ['CHEBI:25372', 'CHEBI:35202']},
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
    'num_true_negatives': 183922,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999945629421008}