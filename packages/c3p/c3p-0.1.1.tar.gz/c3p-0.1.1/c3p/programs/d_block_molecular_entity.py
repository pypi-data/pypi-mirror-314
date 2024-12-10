"""
Classifies: CHEBI:33676 d-block molecular entity
"""
from rdkit import Chem
from rdkit.Chem import Descriptors

# List of d-block elements
d_block_elements = ['Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg']

def is_d_block_molecular_entity(smiles: str):
    """
    Determines if a molecule is a d-block molecular entity.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a d-block molecular entity, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains any d-block element
    atoms = mol.GetAtoms()
    has_d_block_element = any(atom.GetSymbol() in d_block_elements for atom in atoms)

    if has_d_block_element:
        d_block_atoms = [atom.GetSymbol() for atom in atoms if atom.GetSymbol() in d_block_elements]
        reason = f"Molecule contains d-block element(s): {', '.join(d_block_atoms)}"
        return True, reason
    else:
        return False, "Molecule does not contain any d-block element"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33676',
                          'name': 'd-block molecular entity',
                          'definition': 'A d-block molecular entity is a '
                                        'molecular entity containing one or '
                                        'more atoms of a d-block element.',
                          'parents': ['CHEBI:33497']},
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
    'num_true_positives': 66,
    'num_false_positives': 100,
    'num_true_negatives': 68674,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.39759036144578314,
    'recall': 0.9428571428571428,
    'f1': 0.559322033898305,
    'accuracy': 0.9984893382139329}