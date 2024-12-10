"""
Classifies: CHEBI:27306 vitamin B6
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_vitamin_B6(smiles: str):
    """
    Determines if a molecule is a member of the vitamin B6 group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a vitamin B6 compound, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for a pyridine ring
    pyridine_ring = False
    for ring in mol.GetRingInfo().AtomRings():
        atoms = [mol.GetAtomWithIdx(i) for i in ring]
        if len(ring) == 6 and sum(1 for atom in atoms if atom.GetAtomicNum() == 7) == 1:
            pyridine_ring = True
            break

    if not pyridine_ring:
        return False, "No pyridine ring found"

    # Check for allowed substituents
    allowed_substituents = [1, 6, 7, 8, 15, 16, 17]  # H, C, N, O, P, S, Cl
    substituents = set(atom.GetAtomicNum() for atom in mol.GetAtoms() if atom.GetAtomicNum() not in allowed_substituents)

    if substituents:
        return False, f"Disallowed substituents found: {', '.join(Chem.GetPeriodicTable().GetElementSymbol(sub) for sub in substituents)}"

    # Check for functional groups
    functional_groups = ['[OH]', 'C(=O)O', 'OP(=O)(O)O']
    has_functional_group = any(mol.HasSubstructMatch(Chem.MolFromSmarts(fg)) for fg in functional_groups)

    if has_functional_group:
        return True, "Vitamin B6 compound found"
    else:
        return False, "No vitamin B6 functional group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27306',
                          'name': 'vitamin B6',
                          'definition': 'Any member of the group of pyridines '
                                        'that exhibit biological activity '
                                        'against vitamin B6 deficiency. '
                                        'Vitamin B6 deficiency is associated '
                                        'with microcytic anemia, '
                                        'electroencephalographic '
                                        'abnormalities, dermatitis with '
                                        'cheilosis (scaling on the lips and '
                                        'cracks at the corners of the mouth) '
                                        'and glossitis (swollen tongue), '
                                        'depression and confusion, and '
                                        'weakened immune function. Vitamin B6 '
                                        'consists of the vitamers pyridoxine, '
                                        'pyridoxal, and pyridoxamine and their '
                                        "respective 5'-phosphate esters (and "
                                        'includes their corresponding ionized '
                                        'and salt forms).',
                          'parents': ['CHEBI:26421', 'CHEBI:75769']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: Python argument types in\n'
               '    Mol.HasSubstructMatch(Mol, NoneType)\n'
               'did not match C++ signature:\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::MolBundle '
               'query, RDKit::SubstructMatchParameters params=True)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::ROMol query, '
               'RDKit::SubstructMatchParameters params)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::MolBundle '
               'query, bool recursionPossible=True, bool useChirality=False, '
               'bool useQueryQueryMatches=False)\n'
               '    HasSubstructMatch(RDKit::ROMol self, RDKit::ROMol query, '
               'bool recursionPossible=True, bool useChirality=False, bool '
               'useQueryQueryMatches=False)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 1314,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.9293286219081273}