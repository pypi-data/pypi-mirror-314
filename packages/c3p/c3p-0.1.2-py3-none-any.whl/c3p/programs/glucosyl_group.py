"""
Classifies: CHEBI:24281 glucosyl group
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_glucosyl_group(smiles: str):
    """
    Determines if a molecule is a glucosyl group, which is a glycosyl group obtained by removing
    the hydroxy group from the hemiacetal function of a glucose and, by extension, of a lower
    oligosaccharide having glucose at the reducing end.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a glucosyl group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains a glucose substructure
    glucose_smarts = '[C@H]1([C@@H]([C@H]([C@@H]([C@@H]([C@@H](O1)O)O)O)O)O'
    glucose_match = mol.HasSubstructMatch(Chem.MolFromSmarts(glucose_smarts))

    if not glucose_match:
        return False, "The molecule does not contain a glucose substructure"

    # Check if the glucose substructure is at the reducing end
    reducing_end = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetDegree() == 1 and atom.IsInRing():
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'C' and neighbor.GetDegree() == 4:
                    reducing_end = True
                    break

    if not reducing_end:
        return False, "The glucose substructure is not at the reducing end"

    # Check if the hemiacetal hydroxyl group is removed
    hemiacetal_hydroxyl_removed = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetDegree() == 2 and atom.IsInRing():
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'C' and neighbor.GetDegree() == 4:
                    hemiacetal_hydroxyl_removed = True
                    break

    if not hemiacetal_hydroxyl_removed:
        return False, "The hemiacetal hydroxyl group is not removed"

    return True, "The molecule is a glucosyl group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24281',
                          'name': 'glucosyl group',
                          'definition': 'A glycosyl group obtained by removing '
                                        'the hydroxy group from the hemiacetal '
                                        'function of a glucose and, by '
                                        'extension, of a lower oligosaccharide '
                                        'having glucose at the reducing end.',
                          'parents': ['CHEBI:24403']},
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
    'error': 'Python argument types in\n'
             '    Mol.HasSubstructMatch(Mol, NoneType)\n'
             'did not match C++ signature:\n'
             '    HasSubstructMatch(RDKit::ROMol self, RDKit::MolBundle query, '
             'RDKit::SubstructMatchParameters params=True)\n'
             '    HasSubstructMatch(RDKit::ROMol self, RDKit::ROMol query, '
             'RDKit::SubstructMatchParameters params)\n'
             '    HasSubstructMatch(RDKit::ROMol self, RDKit::MolBundle query, '
             'bool recursionPossible=True, bool useChirality=False, bool '
             'useQueryQueryMatches=False)\n'
             '    HasSubstructMatch(RDKit::ROMol self, RDKit::ROMol query, '
             'bool recursionPossible=True, bool useChirality=False, bool '
             'useQueryQueryMatches=False)',
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