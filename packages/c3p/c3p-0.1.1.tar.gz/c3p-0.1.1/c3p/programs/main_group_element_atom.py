"""
Classifies: CHEBI:33318 main group element atom
"""
from rdkit import Chem

def is_main_group_element_atom(smiles: str):
    """
    Determines if a molecule represents a main group element atom.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a main group element atom, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has only one atom
    if mol.GetNumAtoms() != 1:
        return False, "Molecule contains more than one atom"

    atom = mol.GetAtomWithIdx(0)

    # Get the atomic number of the atom
    atomic_number = atom.GetAtomicNum()

    # Define the main group element atomic numbers
    main_group_elements = list(range(1, 119))
    transition_metals = list(range(21, 31)) + list(range(39, 49)) + list(range(71, 81)) + list(range(103, 113))
    inner_transition_metals = list(range(57, 71)) + list(range(89, 103))

    for element in transition_metals + inner_transition_metals:
        main_group_elements.remove(element)

    # Check if the atomic number is a main group element
    if atomic_number in main_group_elements:
        element_symbol = Chem.GetPeriodicTable().GetElementSymbol(atomic_number)
        if atom.HasProp('_MolFileChiralCode') and atom.HasProp('isotope'):
            isotope = atom.GetProp('isotope')
            return True, f"Main group element atom: {element_symbol}-{isotope}"
        elif atom.HasProp('isotope'):
            isotope = atom.GetProp('isotope')
            return True, f"Main group element atom: {element_symbol}-{isotope}"
        else:
            return True, f"Main group element atom: {element_symbol}"

    return False, "Atom does not belong to the main group elements"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33318',
                          'name': 'main group element atom',
                          'definition': 'An atom belonging to one of the main '
                                        'groups (found in the s- and p- '
                                        'blocks) of the periodic table.',
                          'parents': ['CHEBI:33250']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: list.remove(x): x not in list',
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 14,
    'num_false_positives': 100,
    'num_true_negatives': 71609,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.12280701754385964,
    'recall': 1.0,
    'f1': 0.21875,
    'accuracy': 0.9986057471104108}