"""
Classifies: CHEBI:33662 annulene
"""
from rdkit import Chem
from rdkit.Chem import Descriptors

def is_annulene(smiles: str):
    """
    Determines if a molecule is an annulene (mancude monocyclic hydrocarbon without side chains of the general formula CnHn (n is an even number) or CnHn+1 (n is an odd number)).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an annulene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule is a monocycle
    if not mol.GetRingInfo().IsAtomInRingOfSize(0, mol.GetNumAtoms()):
        return False, "Not a monocycle"

    # Check if the molecule contains only C and H atoms
    elements = {atom.GetSymbol() for atom in mol.GetAtoms()}
    if elements != {'C', 'H'}:
        return False, "Molecule contains atoms other than C and H"

    # Count the number of carbon and hydrogen atoms
    num_c = sum(atom.GetSymbol() == 'C' for atom in mol.GetAtoms())
    num_h = sum(atom.GetSymbol() == 'H' for atom in mol.GetAtoms())

    # Check if the molecule satisfies the general formula
    if num_c % 2 == 0 and num_h != num_c:
        return False, "Does not satisfy the general formula for even number of carbons"
    elif num_c % 2 == 1 and num_h != num_c + 1:
        return False, "Does not satisfy the general formula for odd number of carbons"

    # Check if the molecule has any substituents
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetDegree() > 2:
            return False, "Molecule contains substituents"

    return True, f"Annulene with {num_c} carbon atoms"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33662',
                          'name': 'annulene',
                          'definition': 'A mancude monocyclic hydrocarbon '
                                        'without side chains of the general '
                                        'formula CnHn (n is an even number) or '
                                        'CnHn+1 (n is an odd number). In '
                                        'systematic nomenclature an annulene '
                                        'with seven or more carbon atoms may '
                                        'be named [n]annulene, where n is the '
                                        'number of carbon atoms.',
                          'parents': ['CHEBI:33664']},
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183925,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999945630307842}