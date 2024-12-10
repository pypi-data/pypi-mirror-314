"""
Classifies: CHEBI:139065 mannosylinositol-1-phosphodihydroceramide(1-)
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_mannosylinositol_1_phosphodihydroceramide_1__(smiles: str):
    """
    Determines if a molecule is a mannosylinositol-1-phosphodihydroceramide(1-).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a mannosylinositol-1-phosphodihydroceramide(1-), False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of mannosylinositol and ceramide fragments
    mannosylinositol_fragment = None
    ceramide_fragment = None

    for fragment in Chem.GetMolFrags(mol):
        fragment_mol = Chem.MolFromSmarts(fragment)
        if fragment_mol:
            if Chem.MolToSmiles(fragment_mol) == 'OC1C(O)C(O)C(OC2C(CO)C(O)C(O)C(O)C2O)C(COP(=O)(O)[O-])C1O':
                mannosylinositol_fragment = fragment_mol
            elif Chem.MolToSmiles(fragment_mol) == 'CCCCCCCCCCCCCCCCCCC(=O)NC':
                ceramide_fragment = fragment_mol

    if not mannosylinositol_fragment or not ceramide_fragment:
        return False, "Missing mannosylinositol or ceramide fragment"

    # Check if the fragments are connected
    for bond in mol.GetBonds():
        atom1 = bond.GetBeginAtom()
        atom2 = bond.GetEndAtom()
        if atom1.GetIdx() in mannosylinositol_fragment.GetAtoms() and atom2.GetIdx() in ceramide_fragment.GetAtoms():
            return True, "Mannosylinositol-1-phosphodihydroceramide(1-)"

    return False, "Mannosylinositol and ceramide fragments not connected"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:139065',
                          'name': 'mannosylinositol-1-phosphodihydroceramide(1-)',
                          'definition': 'An mannosylinositol '
                                        'phosphoceramide(1-) obtained by '
                                        'deprotonation of the free phosphate '
                                        'OH group of any '
                                        'mannosylinositol-1-phosphodihydroceramide; '
                                        'major species at pH 7.3.',
                          'parents': ['CHEBI:64997']},
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
    'error': 'No registered converter was able to produce a C++ rvalue of type '
             'std::__1::basic_string<wchar_t, std::__1::char_traits<wchar_t>, '
             'std::__1::allocator<wchar_t> > from this Python object of type '
             'tuple',
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