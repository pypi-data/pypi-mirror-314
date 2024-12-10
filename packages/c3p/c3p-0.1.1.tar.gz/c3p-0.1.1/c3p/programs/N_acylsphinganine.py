"""
Classifies: CHEBI:31488 N-acylsphinganine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors
from typing import Optional, Tuple

def is_N_acylsphinganine(smiles: str) -> Optional[Tuple[bool, str]]:
    """
    Determines if a molecule is an N-acylsphinganine.

    An N-acylsphinganine is a ceramide consisting of sphinganine, where one of the amino hydrogens
    is substituted by a fatty acyl group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        Optional[Tuple[bool, str]]: (is_N_acylsphinganine, reason)
            If the molecule is an N-acylsphinganine, returns (True, reason).
            If the molecule is not an N-acylsphinganine, returns (False, reason).
            If the SMILES string is invalid, returns None.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    # Find the sphinganine core
    sphinganine_core = Chem.MolFromSmiles('CCCCCCCCCCCCCCC[C@@H](O)[C@H](CO)N')
    if sphinganine_core is None:
        return None, "Failed to create sphinganine core"

    # Find the acyl group
    acyl_group = None
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N':
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'C' and neighbor.GetDegree() == 3:
                    acyl_group = Chem.MolFragmentToSmiles(mol, neighbor.GetNeighbors(), bondsToUse=[mol.GetBondBetweenAtoms(*pair) for pair in neighbor.GetNeighborPairs()])
                    break
            if acyl_group:
                break

    if acyl_group is None:
        return False, "No acyl group found"

    # Check if the molecule contains the sphinganine core
    match = mol.GetSubstructMatch(sphinganine_core)
    if not match:
        return False, "Sphinganine core not found"

    # Check if the acyl group is attached to the nitrogen of the sphinganine core
    acyl_attachment_atom = mol.GetAtomWithIdx(match[mol.GetSubstructMatch(sphinganine_core, Chem.MolFromSmarts('[N]'))[0]])
    for neighbor in acyl_attachment_atom.GetNeighbors():
        if neighbor.GetSmarts() == acyl_group:
            return True, f"N-acylsphinganine with acyl group {acyl_group}"

    return False, "Acyl group not attached to the nitrogen of the sphinganine core"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:31488',
                          'name': 'N-acylsphinganine',
                          'definition': 'A ceramide consisting of sphinganine '
                                        'in which one of the amino hydrogens '
                                        'is substituted by a fatty acyl group.',
                          'parents': ['CHEBI:139048', 'CHEBI:82829']},
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
    'error': "'Atom' object has no attribute 'GetNeighborPairs'",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}