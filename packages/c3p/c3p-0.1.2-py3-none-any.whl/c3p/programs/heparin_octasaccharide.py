"""
Classifies: CHEBI:132215 heparin octasaccharide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from typing import Tuple

def is_heparin_octasaccharide(smiles: str) -> Tuple[bool, str]:
    """
    Determines if a molecule is a heparin octasaccharide, defined as any amino octasaccharide obtained
    by either chemical or enzymatic cleavage of the polymeric glycosaminoglycan heparin.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a heparin octasaccharide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count the number of atoms
    num_atoms = mol.GetNumAtoms()
    if num_atoms != 64:
        return False, f"Molecule contains {num_atoms} atoms, expected 64 for an octasaccharide"

    # Count the number of rings
    ring_info = mol.GetRingInfo()
    num_rings = len(ring_info.AtomRings())
    if num_rings != 8:
        return False, f"Molecule contains {num_rings} rings, expected 8 for an octasaccharide"

    # Check for the presence of sulfate groups
    sulfate_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == "S")
    if sulfate_count < 3:
        return False, "Molecule does not contain at least 3 sulfate groups, as expected for heparin"

    # Check for the presence of amino groups
    amino_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == "N")
    if amino_count < 2:
        return False, "Molecule does not contain at least 2 amino groups, as expected for heparin"

    return True, "The molecule is a heparin octasaccharide"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:132215',
                          'name': 'heparin octasaccharide',
                          'definition': 'Any amino octasaccharide obtained by '
                                        'either chemical or enzymatic cleavage '
                                        'of the polymeric glycosaminoglycan '
                                        'heparin.',
                          'parents': ['CHEBI:139173', 'CHEBI:71061']},
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
    'num_false_positives': 0,
    'num_true_negatives': 183924,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945630012234}