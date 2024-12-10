"""
Classifies: CHEBI:33303 chalcogen
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_chalcogen(smiles: str):
    """
    Determines if a molecule is a chalcogen (Any p-block element belonging to the group 16 family of the periodic table).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a chalcogen, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if there is only one atom in the molecule
    if mol.GetNumAtoms() != 1:
        return False, "Molecule contains more than one atom"

    # Get the atomic number of the atom
    atom = mol.GetAtomWithIdx(0)
    atomic_number = atom.GetAtomicNum()

    # Check if the atomic number corresponds to a chalcogen element
    chalcogens = [8, 16, 34, 52, 84, 118]
    if atomic_number in chalcogens:
        element_symbol = atom.GetSymbol()
        return True, f"Molecule is a chalcogen element: {element_symbol}"
    else:
        return False, "Molecule is not a chalcogen element"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33303',
                          'name': 'chalcogen',
                          'definition': 'Any p-block element belonging to the '
                                        'group 16 family of the periodic '
                                        'table.',
                          'parents': ['CHEBI:33560']},
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
    'num_true_positives': 5,
    'num_false_positives': 52,
    'num_true_negatives': 183833,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.08771929824561403,
    'recall': 1.0,
    'f1': 0.16129032258064516,
    'accuracy': 0.9997172222524335}