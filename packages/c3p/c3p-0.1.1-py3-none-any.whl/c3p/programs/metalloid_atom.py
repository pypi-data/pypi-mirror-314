"""
Classifies: CHEBI:137980 metalloid atom
"""
from rdkit import Chem

def is_metalloid_atom(smiles: str):
    """
    Determines if a SMILES string represents a metalloid atom.

    Args:
        smiles (str): SMILES string of the atom

    Returns:
        bool: True if the atom is a metalloid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    if mol.GetNumAtoms() != 1:
        return False, "SMILES string does not represent a single atom"

    atom = mol.GetAtomWithIdx(0)
    symbol = atom.GetSymbol()
    atomic_number = atom.GetAtomicNum()

    metalloids = ['B', 'Si', 'Ge', 'As', 'Sb', 'Te']
    less_common_metalloids = ['C', 'Al', 'Se', 'Po', 'At']

    if symbol in metalloids:
        return True, f"{symbol} is a metalloid atom"
    elif symbol in less_common_metalloids:
        if symbol == 'C':
            if atomic_number == 6:
                return False, f"{symbol} is not a metalloid atom"
            else:
                return True, f"{symbol}-{atomic_number} is sometimes considered a metalloid atom"
        elif symbol == 'Al':
            if atomic_number == 13:
                return False, f"{symbol} is not a metalloid atom"
            else:
                return True, f"{symbol}-{atomic_number} is sometimes considered a metalloid atom"
        elif symbol == 'Se':
            if atomic_number == 34:
                return False, f"{symbol} is not a metalloid atom"
            else:
                return True, f"{symbol}-{atomic_number} is sometimes considered a metalloid atom"
        elif symbol == 'Po':
            if atomic_number in [194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209]:
                return True, f"{symbol}-{atomic_number} is sometimes considered a metalloid atom"
            else:
                return False, f"{symbol}-{atomic_number} is not a metalloid atom"
        elif symbol == 'At':
            if atomic_number == 85:
                return True, f"{symbol} is sometimes considered a metalloid atom"
            else:
                return False, f"{symbol}-{atomic_number} is not a metalloid atom"
    else:
        return False, f"{symbol} is not a metalloid atom"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:137980',
                          'name': 'metalloid atom',
                          'definition': 'An atom of an element that exhibits '
                                        'properties that are between those of '
                                        'metals and nonmetals, or that has a '
                                        'mixture of them. The term generally '
                                        'includes boron, silicon, germanium, '
                                        'arsenic, antimony, and tellurium, '
                                        'while carbon, aluminium, selenium, '
                                        'polonium, and astatine are less '
                                        'commonly included.',
                          'parents': ['CHEBI:33250']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.0196078431372549 is too low.\n'
               "True positives: [('[32Si]', 'Si is a metalloid atom')]\n"
               "False positives: [('[H][Se+]([H])[H]', 'Se is sometimes "
               "considered a metalloid atom'), ('[205Po]', 'Po is sometimes "
               "considered a metalloid atom'), ('[Ge++]', 'Ge is a metalloid "
               "atom'), ('[H][As+][H]', 'As is a metalloid atom'), ('[10C]', "
               "'C is sometimes considered a metalloid atom'), ('[H][C--][H]', "
               "'C is sometimes considered a metalloid atom'), ('[Se+6]', 'Se "
               "is sometimes considered a metalloid atom'), ('[197Po]', 'Po is "
               "sometimes considered a metalloid atom'), ('[193Po]', 'Po is "
               "sometimes considered a metalloid atom'), ('[Se++]', 'Se is "
               "sometimes considered a metalloid atom'), "
               "('[H][B-]([H])([H])[H]', 'B is a metalloid atom'), ('[C+]', 'C "
               "is sometimes considered a metalloid atom'), ('[192Po]', 'Po is "
               "sometimes considered a metalloid atom'), ('[213Po]', 'Po is "
               "sometimes considered a metalloid atom'), ('[214Po]', 'Po is "
               "sometimes considered a metalloid atom'), ('[202Po]', 'Po is "
               "sometimes considered a metalloid atom'), ('[Si+4]', 'Si is a "
               "metalloid atom'), ('[13C]', 'C is sometimes considered a "
               "metalloid atom'), ('[H][As+]([H])([H])[H]', 'As is a metalloid "
               "atom'), ('[14C]', 'C is sometimes considered a metalloid "
               "atom'), ('[H][Al-]([H])([H])[H]', 'Al is sometimes considered "
               "a metalloid atom'), ('[At-]', 'At is sometimes considered a "
               "metalloid atom'), ('[198Po]', 'Po is sometimes considered a "
               "metalloid atom'), ('[Se+4]', 'Se is sometimes considered a "
               "metalloid atom'), ('[H][Sb+]([H])([H])[H]', 'Sb is a metalloid "
               "atom'), ('[28Al]', 'Al is sometimes considered a metalloid "
               "atom'), ('[212Po]', 'Po is sometimes considered a metalloid "
               "atom'), ('[Al-]', 'Al is sometimes considered a metalloid "
               "atom'), ('[H][Sb+]([H])[H]', 'Sb is a metalloid atom'), "
               "('[11C]', 'C is sometimes considered a metalloid atom'), "
               "('[211Po]', 'Po is sometimes considered a metalloid atom'), "
               "('[B+3]', 'B is a metalloid atom'), ('[Si+2]', 'Si is a "
               "metalloid atom'), ('[195Po]', 'Po is sometimes considered a "
               "metalloid atom'), ('[206Po]', 'Po is sometimes considered a "
               "metalloid atom'), ('[191Po]', 'Po is sometimes considered a "
               "metalloid atom'), ('[H][Sb]([H])[H]', 'Sb is a metalloid "
               "atom'), ('[As++][H]', 'As is a metalloid atom'), "
               "('[H][Si+]([H])[H]', 'Si is a metalloid atom'), ('[77Se]', 'Se "
               "is sometimes considered a metalloid atom'), "
               "('[H][Se]([H])[H]', 'Se is sometimes considered a metalloid "
               "atom'), ('[C-]', 'C is sometimes considered a metalloid "
               "atom'), ('[Te-][H]', 'Te is a metalloid atom'), ('[CH2]', 'C "
               "is sometimes considered a metalloid atom'), ('[H][B+][H]', 'B "
               "is a metalloid atom'), ('[B-]', 'B is a metalloid atom'), "
               "('[Si-]', 'Si is a metalloid atom'), ('[H][Sb-]([H])[H]', 'Sb "
               "is a metalloid atom'), ('[C+4]', 'C is sometimes considered a "
               "metalloid atom'), ('[Se-]', 'Se is sometimes considered a "
               "metalloid atom'), ('[H][Ge]([H])[H]', 'Ge is a metalloid "
               "atom'), ('[H][C+]([H])([H])[H]', 'C is sometimes considered a "
               "metalloid atom'), ('[H][Te+][H]', 'Te is a metalloid atom'), "
               "('[H][Te+]([H])[H]', 'Te is a metalloid atom'), ('[Se]', 'Se "
               "is sometimes considered a metalloid atom'), "
               "('[H][Te]([H])[H]', 'Te is a metalloid atom'), ('[B--][H]', 'B "
               "is a metalloid atom'), ('[H][Si]([H])([H])[H]', 'Si is a "
               "metalloid atom'), ('[H][Al+]([H])[H]', 'Al is sometimes "
               "considered a metalloid atom'), ('[H][Si]([H])[H]', 'Si is a "
               "metalloid atom'), ('[At]', 'At is sometimes considered a "
               "metalloid atom'), ('C[H]', 'C is sometimes considered a "
               "metalloid atom'), ('[B++][H]', 'B is a metalloid atom'), "
               "('[H][Sb]([H])([H])([H])[H]', 'Sb is a metalloid atom'), "
               "('[Te-]', 'Te is a metalloid atom'), ('[H][Si-]([H])[H]', 'Si "
               "is a metalloid atom'), ('[H][C-]([H])[H]', 'C is sometimes "
               "considered a metalloid atom'), ('[Sb+3]', 'Sb is a metalloid "
               "atom'), ('[190Po]', 'Po is sometimes considered a metalloid "
               "atom'), ('[H][Al-]([H])[H]', 'Al is sometimes considered a "
               "metalloid atom'), ('[H][B-][H]', 'B is a metalloid atom'), "
               "('[26Al]', 'Al is sometimes considered a metalloid atom'), "
               "('[Ge-4]', 'Ge is a metalloid atom'), ('[H][As]([H])[H]', 'As "
               "is a metalloid atom'), ('[Al+]', 'Al is sometimes considered a "
               "metalloid atom'), ('[As--][H]', 'As is a metalloid atom'), "
               "('[Al]', 'Al is sometimes considered a metalloid atom'), "
               "('[H][As][H]', 'As is a metalloid atom'), ('[218Po]', 'Po is "
               "sometimes considered a metalloid atom'), ('[Te+][H]', 'Te is a "
               "metalloid atom'), ('[H][Te][H]', 'Te is a metalloid atom'), "
               "('[194Po]', 'Po is sometimes considered a metalloid atom'), "
               "('[H]C([H])([H])[H]', 'C is sometimes considered a metalloid "
               "atom'), ('[Si-4]', 'Si is a metalloid atom'), ('[Se-2]', 'Se "
               "is sometimes considered a metalloid atom'), ('[H][Te-][H]', "
               "'Te is a metalloid atom'), ('[B-3]', 'B is a metalloid atom'), "
               "('[H][As+]([H])[H]', 'As is a metalloid atom'), "
               "('[H][Te-]([H])[H]', 'Te is a metalloid atom'), ('[12C]', 'C "
               "is sometimes considered a metalloid atom'), ('[As+5]', 'As is "
               "a metalloid atom'), ('[217Po]', 'Po is sometimes considered a "
               "metalloid atom'), ('[H][Po][H]', 'Po is sometimes considered a "
               "metalloid atom'), ('[C-4]', 'C is sometimes considered a "
               "metalloid atom'), ('[H][B-]([H])[H]', 'B is a metalloid "
               "atom'), ('[B][H]', 'B is a metalloid atom'), ('[203Po]', 'Po "
               "is sometimes considered a metalloid atom'), ('[Al+][H]', 'Al "
               "is sometimes considered a metalloid atom'), ('[201Po]', 'Po is "
               "sometimes considered a metalloid atom'), ('[H]B([H])[H]', 'B "
               "is a metalloid atom')]\n"
               'False negatives: []',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 67,
    'num_true_negatives': 183850,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.014705882352941176,
    'recall': 1.0,
    'f1': 0.028985507246376812,
    'accuracy': 0.9996357072173468}