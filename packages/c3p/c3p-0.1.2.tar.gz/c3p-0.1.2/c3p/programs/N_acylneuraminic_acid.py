"""
Classifies: CHEBI:16498 N-acylneuraminic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_N_acylneuraminic_acid(smiles: str):
    """
    Determines if a molecule is an N-acylneuraminic acid.

    N-acylneuraminic acids are defined as neuraminic acids carrying an N-acyl substituent.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an N-acylneuraminic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Identify the neuraminic acid core
    neuraminic_acid_core_smarts = "[C@](C([O-])=O)(O)[C@H](O)[C@H](O)[C@H](O)[C@H](NC(=O))"
    neuraminic_acid_core = mol.GetSubstructMatches(Chem.MolFromSmarts(neuraminic_acid_core_smarts))

    if not neuraminic_acid_core:
        return False, "Molecule does not contain the neuraminic acid core"

    # Check for an N-acyl substituent
    n_acyl_smarts = "[CH3][CX3](=[OX1])"
    n_acyl = mol.GetSubstructMatches(Chem.MolFromSmarts(n_acyl_smarts))

    if not n_acyl:
        return False, "Molecule does not contain an N-acyl substituent"

    # Check if the N-acyl substituent is attached to the nitrogen of the neuraminic acid core
    core_n_idx = neuraminic_acid_core[0][-1]
    for acyl_idx in n_acyl:
        acyl_atom = mol.GetAtomWithIdx(acyl_idx)
        if acyl_atom.GetNeighbors()[0].GetIdx() == core_n_idx:
            return True, "Molecule is an N-acylneuraminic acid"

    return False, "N-acyl substituent is not attached to the neuraminic acid core"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16498',
                          'name': 'N-acylneuraminic acid',
                          'definition': 'Any neuraminic acid carrying an '
                                        'N-acyl substituent.',
                          'parents': ['CHEBI:26667']},
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
    'num_true_negatives': 183917,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945627942888}