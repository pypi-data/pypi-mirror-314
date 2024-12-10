"""
Classifies: CHEBI:25275 methylaniline
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_methylaniline(smiles: str):
    """
    Determines if a molecule is a methylaniline (a substituted aniline carrying one or more methyl groups at unspecified positions).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a methylaniline, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains an aniline substructure
    aniline_pattern = Chem.MolFromSmarts('c1ccc(N)cc1')
    if not mol.HasSubstructMatch(aniline_pattern):
        return False, "Molecule does not contain an aniline substructure"

    # Check if the molecule contains at least one methyl group
    methyl_pattern = Chem.MolFromSmarts('C')
    if not any(mol.HasSubstructMatch(methyl_pattern, useChirality=False)):
        return False, "Molecule does not contain any methyl groups"

    # Check if the methyl groups are attached to the aniline substructure
    aniline_atoms = list(mol.GetSubstructMatch(aniline_pattern))
    methyl_groups = []
    for atom_idx in aniline_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetSymbol() == 'C' and sum(1 for bond in neighbor.GetBonds() if bond.GetBondType() == Chem.BondType.SINGLE) == 3:
                methyl_groups.append(neighbor.GetIdx())

    if not methyl_groups:
        return False, "Methyl groups are not attached to the aniline substructure"

    return True, f"Methylaniline with {len(set(methyl_groups))} methyl group(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25275',
                          'name': 'methylaniline',
                          'definition': 'A substituted aniline carrying one or '
                                        'more methyl groups at unspecified '
                                        'positions.',
                          'parents': ['CHEBI:48975']},
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
    'error': "'bool' object is not iterable",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}