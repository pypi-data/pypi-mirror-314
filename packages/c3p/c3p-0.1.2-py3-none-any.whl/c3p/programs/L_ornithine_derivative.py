"""
Classifies: CHEBI:21368 L-ornithine derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_L_ornithine_derivative(smiles: str):
    """
    Determines if a molecule is an L-ornithine derivative.

    An L-ornithine derivative is defined as resulting from a reaction of L-ornithine at the
    amino group, the carboxy group or the side-chain amino group, or from the replacement of
    any hydrogen of L-ornithine by a heteroatom.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is an L-ornithine derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains the L-ornithine backbone
    ornithine_smarts = '[NH2][CH]([CH2][CH2][CH2][CH](N)[CH](O)=O)O'
    ornithine_match = mol.GetSubstructMatches(Chem.MolFromSmarts(ornithine_smarts))

    if not ornithine_match:
        return False, "The molecule does not contain the L-ornithine backbone"

    # Check for modifications at the amino, carboxy, or side-chain amino groups
    modified_groups = []
    for atom_idx in ornithine_match[0]:
        atom = mol.GetAtomWithIdx(atom_idx)
        if atom.GetSymbol() == 'N':
            if atom.GetTotalNumHs() < 2:
                modified_groups.append('amino')
        elif atom.GetSymbol() == 'O':
            if atom.GetTotalNumHs() < 1:
                modified_groups.append('carboxy')
        elif atom.GetSymbol() == 'C':
            neighbors = [mol.GetAtomWithIdx(neighbor_idx) for neighbor_idx in atom.GetNeighbors()]
            if any(neighbor.GetSymbol() == 'N' and neighbor.GetTotalNumHs() < 2 for neighbor in neighbors):
                modified_groups.append('side-chain amino')

    # Check for replacement of hydrogens with heteroatoms
    heteroatom_replacement = False
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() != 1 and atom.GetAtomicNum() != 6 and atom.GetAtomicNum() != 7 and atom.GetAtomicNum() != 8:
            heteroatom_replacement = True
            break

    if modified_groups or heteroatom_replacement:
        reason = "The molecule is an L-ornithine derivative with modifications: "
        if modified_groups:
            reason += ', '.join(modified_groups)
        if heteroatom_replacement:
            if modified_groups:
                reason += ', '
            reason += "heteroatom replacement"
        return True, reason
    else:
        return False, "The molecule is L-ornithine itself, not a derivative"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:21368',
                          'name': 'L-ornithine derivative',
                          'definition': 'An ornithine derivative resulting '
                                        'from reaction of L-ornithine at the '
                                        'amino group, the carboxy group or the '
                                        'side-chain amino group, or from the '
                                        'replacement of any hydrogen of '
                                        'L-ornithine by a heteroatom.',
                          'parents': ['CHEBI:25718']},
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
    'num_true_negatives': 183918,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999945628238518}