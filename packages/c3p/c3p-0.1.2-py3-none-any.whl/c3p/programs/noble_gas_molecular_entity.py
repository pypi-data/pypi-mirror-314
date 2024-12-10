"""
Classifies: CHEBI:33583 noble gas molecular entity
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_noble_gas_molecular_entity(smiles: str):
    """
    Determines if a molecule is a noble gas molecular entity.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a noble gas molecular entity, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # List of noble gas atomic numbers
    noble_gas_nums = [2, 10, 18, 36, 54, 86]  # He, Ne, Ar, Kr, Xe, Rn

    # Get the atomic numbers of atoms in the molecule
    atom_nums = [atom.GetAtomicNum() for atom in mol.GetAtoms()]

    # Check if all atoms are noble gases
    all_noble_gases = all(num in noble_gas_nums for num in atom_nums)

    if all_noble_gases:
        # Check if the molecule has more than one atom
        if len(atom_nums) > 1:
            noble_gas_symbols = [Chem.GetPeriodicTable().GetElementSymbol(num) for num in atom_nums]
            return True, f"A molecular entity containing noble gas atoms: {', '.join(noble_gas_symbols)}"
        else:
            # Handle cases like [He] or [Rn]
            atom_symbol = Chem.GetPeriodicTable().GetElementSymbol(atom_nums[0])
            return False, f"Not a molecular entity, but a single atom: {atom_symbol}"
    else:
        return False, "Not a noble gas molecular entity"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33583',
                          'name': 'noble gas molecular entity',
                          'definition': 'A main group molecular entity '
                                        'containing one or more atoms of any '
                                        'noble gas.',
                          'parents': ['CHEBI:33579']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.3076923076923077 is too low.\n'
               "True positives: [('[He][He]', 'A molecular entity containing "
               "only noble gas atoms: He, He'), ('[He][He+]', 'A molecular "
               "entity containing only noble gas atoms: He, He')]\n"
               "False positives: [('[4He]', 'A molecular entity containing "
               "only noble gas atoms: He'), ('[6He]', 'A molecular entity "
               "containing only noble gas atoms: He'), ('[220Rn]', 'A "
               "molecular entity containing only noble gas atoms: Rn'), "
               "('[222Rn]', 'A molecular entity containing only noble gas "
               "atoms: Rn'), ('[3He]', 'A molecular entity containing only "
               "noble gas atoms: He'), ('[8He]', 'A molecular entity "
               "containing only noble gas atoms: He'), ('[219Rn]', 'A "
               "molecular entity containing only noble gas atoms: Rn'), "
               "('[Rn+]', 'A molecular entity containing only noble gas atoms: "
               "Rn'), ('[Rn]', 'A molecular entity containing only noble gas "
               "atoms: Rn')]\n"
               'False negatives: []',
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 0,
    'num_true_negatives': 183911,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 1.0,
    'recall': 1.0,
    'f1': 1.0,
    'accuracy': 1.0}