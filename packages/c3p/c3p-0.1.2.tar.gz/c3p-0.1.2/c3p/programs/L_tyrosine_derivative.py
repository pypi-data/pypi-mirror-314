"""
Classifies: CHEBI:27177 L-tyrosine derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem import rdmolops

def is_L_tyrosine_derivative(smiles: str):
    """
    Determines if a molecule is an L-tyrosine derivative.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an L-tyrosine derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains the L-tyrosine scaffold
    tyrosine_scaffold = Chem.MolFromSmiles('N[C@@H](Cc1ccc(O)cc1)C(O)=O')
    if mol.GetSubstructMatch(tyrosine_scaffold) == []:
        return False, "Molecule does not contain the L-tyrosine scaffold"

    # Check for modifications at the amino group, carboxy group, or hydrogen replacement
    modified = False
    reason = []

    # Check for modifications at the amino group
    amino_group = Chem.MolFromSmiles('N')
    amino_group_match = mol.GetSubstructMatches(amino_group)
    if amino_group_match:
        amino_group_atom = mol.GetAtomWithIdx(amino_group_match[0][0])
        if not list(amino_group_atom.GetNeighbors())[0].GetSymbol() == 'H':
            modified = True
            reason.append("Modified at amino group")

    # Check for modifications at the carboxy group
    carboxy_group = Chem.MolFromSmiles('C(O)=O')
    carboxy_group_match = mol.GetSubstructMatches(carboxy_group)
    if carboxy_group_match:
        carboxy_group_atom = mol.GetAtomWithIdx(carboxy_group_match[0][0])
        neighbors = list(carboxy_group_atom.GetNeighbors())
        if any(neighbor.GetSymbol() != 'O' and neighbor.GetSymbol() != 'H' for neighbor in neighbors):
            modified = True
            reason.append("Modified at carboxy group")

    # Check for hydrogen replacement by heteroatoms
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetTotalNumHs() < atom.GetImplicitValence():
            modified = True
            reason.append("Hydrogen replaced by heteroatom")
            break

    if modified:
        return True, ", ".join(reason)
    else:
        return False, "Unmodified L-tyrosine"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27177',
                          'name': 'L-tyrosine derivative',
                          'definition': 'A proteinogenic amino acid derivative '
                                        'resulting from reaction of L-tyrosine '
                                        'at the amino group or the carboxy '
                                        'group, or from the replacement of any '
                                        'hydrogen of L-tyrosine by a '
                                        'heteroatom.',
                          'parents': [   'CHEBI:62761',
                                         'CHEBI:83811',
                                         'CHEBI:84144']},
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
    'num_true_positives': 5,
    'num_false_positives': 100,
    'num_true_negatives': 21,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 1.0,
    'f1': 0.0909090909090909,
    'accuracy': 0.20634920634920634}