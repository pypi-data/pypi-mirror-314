"""
Classifies: CHEBI:33521 metal atom
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_metal_atom(smiles: str):
    """
    Determines if the given SMILES string represents a metal atom.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a metal atom, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    if mol.GetNumAtoms() != 1:
        return False, "Not a single atom"

    atom = mol.GetAtomWithIdx(0)
    symbol = atom.GetSymbol()
    atomic_number = atom.GetAtomicNum()

    # List of metal elements based on the IUPAC definition
    metal_elements = [
        'Li', 'Be', 'Na', 'Mg', 'Al', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
        'Ga', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Cs', 'Ba',
        'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta',
        'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U',
        'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt',
        'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og'
    ]

    if symbol in metal_elements:
        return True, f"{symbol} is a metal atom"
    else:
        return False, f"{symbol} is not a metal atom"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33521',
                          'name': 'metal atom',
                          'definition': 'An atom of an element that exhibits '
                                        'typical metallic properties, being '
                                        'typically shiny, with high electrical '
                                        'and thermal conductivity.',
                          'parents': ['CHEBI:33250']},
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
    'num_true_positives': 15,
    'num_false_positives': 100,
    'num_true_negatives': 109477,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.13043478260869565,
    'recall': 1.0,
    'f1': 0.23076923076923078,
    'accuracy': 0.9990875246368348}