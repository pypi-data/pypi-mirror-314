"""
Classifies: CHEBI:139477 mogroside
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_mogroside(smiles: str):
    """
    Determines if a molecule is a mogroside (a triterpenoid saponin in which the triterpenoid fragment can be any cucurbitane derivative).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a mogroside, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a cucurbitane core
    cucurbitane_core = '[C@@]12([C@](C3([C@@]([C@](CC3)(C1)C)(CC[C@@H](O)[C@H]2C)C)C)CC'
    cucurbitane_core_mol = Chem.MolFromSmarts(cucurbitane_core)
    if not mol.HasSubstructMatch(cucurbitane_core_mol):
        return False, "No cucurbitane core found"

    # Check for the presence of a triterpenoid saponin fragment
    saponin_fragment = '[C@H]([C@H](O)[C@@H](O)[C@H](O)O)[C@H](O)[C@H](O)CO'
    saponin_fragment_mol = Chem.MolFromSmarts(saponin_fragment)
    if not mol.HasSubstructMatch(saponin_fragment_mol):
        return False, "No triterpenoid saponin fragment found"

    return True, "Molecule is a mogroside (triterpenoid saponin with cucurbitane core)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:139477',
                          'name': 'mogroside',
                          'definition': 'A triterpenoid saponin in which the '
                                        'triterpenoid fragment can be any '
                                        'cucurbitane derivative.',
                          'parents': ['CHEBI:61778']},
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
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}