"""
Classifies: CHEBI:26907 tetrahydrofolic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_tetrahydrofolic_acid(smiles: str) -> tuple[bool, str]:
    """
    Determines if a molecule is a tetrahydrofolic acid, which is defined as a group of heterocyclic compounds
    based on the 5,6,7,8-tetrahydropteroic acid skeleton conjugated with one or more L-glutamic acid units.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a tetrahydrofolic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains a tetrahydropteroic acid skeleton
    skeleton_smarts = '[#7]1([#6]([#7])([#6]([#7])([#6]([#7])([#6]1)))([#6]([#6]1=[#6]([#7])([#6]([#6]1)[#7])([#6]([#6]([#6]([#6]([#6]([#7])([#6]1=[#7]))([#6]1=[#7]))([#6]([#7])([#6]([#6]1)([#7])([#6]([#6]([#6]([#6]([#6]([#6])([#6])([#6]=[#6]))([#6]1=[#7]))([#7])([#6]1=[#6]([#7])([#6]([#6]1)[#7])([#6]([#6]([#8])([#6]))([#7]))([#6]=[#8]))([#7])([#6]([#6]([#6]([#8])([#8])([#8]))([#7])([#7]))([#6]([#6]([#6])([#6])([#6]([#8])([#8]))([#7])([#7]))'
    skeleton_match = mol.HasSubstructMatch(Chem.MolFromSmarts(skeleton_smarts))

    if not skeleton_match:
        return False, "Does not contain a tetrahydropteroic acid skeleton"

    # Check if the molecule contains a glutamic acid unit
    glutamic_smarts = '[#6]([#6]([#6]([#8])([#8]))([#7])([#6]([#6]([#8])([#8]))([#7]))'
    glutamic_match = mol.HasSubstructMatch(Chem.MolFromSmarts(glutamic_smarts))

    if not glutamic_match:
        return False, "Does not contain a glutamic acid unit"

    return True, "Molecule is a tetrahydrofolic acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26907',
                          'name': 'tetrahydrofolic acid',
                          'definition': 'A group of heterocyclic compounds '
                                        'based on the '
                                        '5,6,7,8-tetrahydropteroic acid '
                                        'skeleton conjugated with one or more '
                                        'L-glutamic acid units.',
                          'parents': ['CHEBI:37445']},
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