"""
Classifies: CHEBI:145037 hydroperoxy fatty ester
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_hydroperoxy_fatty_ester(smiles: str):
    """
    Determines if a molecule is a hydroperoxy fatty ester, defined as any fatty acid ester
    carrying one or more hydroperoxy substituents.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hydroperoxy fatty ester, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains an ester group
    ester_pattern = Chem.MolFromSmarts('C(=O)OC')
    if not mol.HasSubstructMatch(ester_pattern):
        return False, "No ester group found"

    # Check if the molecule contains a hydroperoxy group
    hydroperoxy_pattern = Chem.MolFromSmarts('OO')
    if not mol.HasSubstructMatch(hydroperoxy_pattern):
        return False, "No hydroperoxy group found"

    # Check if the hydroperoxy group is attached to a fatty acid chain
    fatty_acid_pattern = Chem.MolFromSmarts('CCCCCCCCCCCCCCC')
    fatty_acid_match = mol.GetSubstructMatches(fatty_acid_pattern)

    if not fatty_acid_match:
        return False, "No fatty acid chain found"

    for match in fatty_acid_match:
        for atom_idx in match:
            atom = mol.GetAtomWithIdx(atom_idx)
            for neighbor in atom.GetNeighbors():
                if mol.HasSubstructMatch(Chem.MolFromSmiles(f'O[{neighbor.GetIdx()}]')):
                    hydroperoxy_count = sum(1 for neighbor in neighbor.GetNeighbors() if neighbor.GetSymbol() == 'O')
                    if hydroperoxy_count == 2:
                        return True, "Hydroperoxy fatty ester detected"

    return False, "No hydroperoxy group attached to fatty acid chain"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:145037',
                          'name': 'hydroperoxy fatty ester',
                          'definition': 'Any fatty acid ester carrying one or '
                                        'more hydroperoxy substituents.',
                          'parents': ['CHEBI:35748', 'CHEBI:61051']},
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