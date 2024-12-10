"""
Classifies: CHEBI:33299 alkaline earth molecular entity
"""
from rdkit import Chem
from rdkit.Chem import Descriptors

def is_alkaline_earth_molecular_entity(smiles: str):
    """
    Determines if a molecule is an alkaline earth molecular entity.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is an alkaline earth molecular entity, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get the atomic numbers of all atoms in the molecule
    atom_nums = [atom.GetAtomicNum() for atom in mol.GetAtoms()]

    # Check if the molecule contains any alkaline earth metal atoms
    alkaline_earth_metals = [4, 12, 20, 38, 56, 88]
    if any(num in alkaline_earth_metals for num in atom_nums):
        alkaline_earth_symbols = [Chem.GetPeriodicTable().GetElementSymbol(num) for num in alkaline_earth_metals if num in atom_nums]
        reason = f"Molecule contains alkaline earth metal(s): {', '.join(alkaline_earth_symbols)}"
        return True, reason
    else:
        return False, "Molecule does not contain any alkaline earth metal atoms"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33299',
                          'name': 'alkaline earth molecular entity',
                          'definition': 'An alkaline earth molecular entity is '
                                        'a molecular entity containing one or '
                                        'more atoms of an alkaline earth '
                                        'metal.',
                          'parents': ['CHEBI:33674']},
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
    'num_true_positives': 16,
    'num_false_positives': 100,
    'num_true_negatives': 157870,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.13793103448275862,
    'recall': 1.0,
    'f1': 0.2424242424242424,
    'accuracy': 0.999367032521869}