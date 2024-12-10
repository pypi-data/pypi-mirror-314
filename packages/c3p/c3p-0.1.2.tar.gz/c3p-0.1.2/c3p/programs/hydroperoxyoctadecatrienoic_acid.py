"""
Classifies: CHEBI:134615 hydroperoxyoctadecatrienoic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hydroperoxyoctadecatrienoic_acid(smiles: str):
    """
    Determines if a molecule is a hydroperoxyoctadecatrienoic acid.

    A hydroperoxyoctadecatrienoic acid is an octadecanoid that is any octadecatrienoic acid carrying
    a single hydroperoxy substituent (position unspecified).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hydroperoxyoctadecatrienoic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has 18 carbon atoms
    num_carbon_atoms = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if num_carbon_atoms != 18:
        return False, "Molecule does not have 18 carbon atoms"

    # Check if the molecule has 3 non-conjugated double bonds
    double_bond_pattern = Chem.MolFromSmarts('[C@H]=C')
    double_bond_matches = mol.GetSubstructMatches(double_bond_pattern)
    if len(double_bond_matches) != 3:
        return False, "Molecule does not have 3 non-conjugated double bonds"

    # Check if the molecule has a hydroperoxy group
    hydroperoxy_pattern = Chem.MolFromSmarts('OO[C]')
    hydroperoxy_matches = mol.GetSubstructMatches(hydroperoxy_pattern)
    if len(hydroperoxy_matches) != 1:
        return False, "Molecule does not have a single hydroperoxy group"

    # Check if the molecule has a carboxylic acid group
    carboxylic_acid_pattern = Chem.MolFromSmarts('C(=O)O')
    carboxylic_acid_matches = mol.GetSubstructMatches(carboxylic_acid_pattern)
    if len(carboxylic_acid_matches) != 1:
        return False, "Molecule does not have a carboxylic acid group"

    return True, "Molecule is a hydroperoxyoctadecatrienoic acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134615',
                          'name': 'hydroperoxyoctadecatrienoic acid',
                          'definition': 'A octadecanoid that is any '
                                        'octadecatrienoic acid carrying a '
                                        'single hydroperoxy substituent '
                                        '(position unspecified).',
                          'parents': [   'CHEBI:15904',
                                         'CHEBI:189832',
                                         'CHEBI:36326',
                                         'CHEBI:73155']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: Python argument types in\n'
               '    Mol.GetSubstructMatches(Mol, NoneType)\n'
               'did not match C++ signature:\n'
               '    GetSubstructMatches(RDKit::ROMol self, RDKit::MolBundle '
               'query, RDKit::SubstructMatchParameters params)\n'
               '    GetSubstructMatches(RDKit::ROMol self, RDKit::ROMol query, '
               'RDKit::SubstructMatchParameters params)\n'
               '    GetSubstructMatches(RDKit::ROMol self, RDKit::MolBundle '
               'query, bool uniquify=True, bool useChirality=False, bool '
               'useQueryQueryMatches=False, unsigned int maxMatches=1000)\n'
               '    GetSubstructMatches(RDKit::ROMol self, RDKit::ROMol query, '
               'bool uniquify=True, bool useChirality=False, bool '
               'useQueryQueryMatches=False, unsigned int maxMatches=1000)',
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 21,
    'num_true_negatives': 183899,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.045454545454545456,
    'recall': 1.0,
    'f1': 0.08695652173913045,
    'accuracy': 0.9998858205425155}