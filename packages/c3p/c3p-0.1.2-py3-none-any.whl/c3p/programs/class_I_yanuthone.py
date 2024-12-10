"""
Classifies: CHEBI:133075 class I yanuthone
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_class_I_yanuthone(smiles: str):
    """
    Determines if a molecule is a Class I yanuthone, defined as:
    Any of the yanuthones whose 5,6-epoxycyclohex-2-en-1-one core is substituted at position 3 by
    a methyl group or its oxidised (hydroxymethyl or acyloxymethyl) derivatives. It is thought that
    the core may be derived from 6-methylsalicylic acid, resulting in a C7 scaffold through a
    decarboxylation.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a Class I yanuthone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of the 5,6-epoxycyclohex-2-en-1-one core
    core_smarts = '[C@]1(O)C=CC(=O)C2=C1C2(C)C'
    core_matches = mol.GetSubstructMatches(Chem.MolFromSmarts(core_smarts))

    if not core_matches:
        return False, "The 5,6-epoxycyclohex-2-en-1-one core is not present"

    # Check for substitution at position 3
    substituent_atoms = []
    for match in core_matches:
        atom_idx = match[-1]  # Index of the atom at position 3 (the methyl-substituted carbon)
        atom = mol.GetAtomWithIdx(atom_idx)
        substituent_atoms.extend([neighbor.GetSymbol() for neighbor in atom.GetNeighbors() if neighbor.GetIdx() not in match])

    if 'C' not in substituent_atoms:
        return False, "The core is not substituted at position 3 by a methyl group or its oxidised derivatives"

    # Check for the presence of hydroxymethyl or acyloxymethyl substituents
    oxidised_substituents = ['O', 'C(=O)O']
    oxidised_substituents_present = any(s in substituent_atoms for s in oxidised_substituents)

    if oxidised_substituents_present:
        return True, "Class I yanuthone with oxidised substituent at position 3"
    else:
        return True, "Class I yanuthone with methyl substituent at position 3"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:133075',
                          'name': 'class I yanuthone',
                          'definition': 'Any of the yanuthones whose '
                                        '5,6-epoxycyclohex-2-en-1-one core is '
                                        'substituted at position 3 by a methyl '
                                        'group or its oxidised (hydroxymethyl '
                                        'or acyloxymethyl) derivatives. It is '
                                        'thought that the core may be derived '
                                        'from 6-methylsalicylic acid, '
                                        'resulting in a C7 scaffold through a '
                                        'decarboxylation.',
                          'parents': ['CHEBI:133070']},
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
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183923,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945629716622}