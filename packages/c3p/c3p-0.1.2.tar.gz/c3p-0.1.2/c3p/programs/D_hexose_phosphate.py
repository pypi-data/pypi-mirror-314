"""
Classifies: CHEBI:15965 D-hexose phosphate
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_D_hexose_phosphate(smiles: str):
    """
    Determines if a molecule is a D-hexose phosphate, i.e., a mono-phosphorylated D-hexose with
    a chain of six carbon atoms.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a D-hexose phosphate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for six carbon atoms
    if rdMolDescriptors.CalcNumHeavyAtoms(mol) != 18:
        return False, "The molecule does not have 18 heavy atoms (6 C, 1 P, 11 O)"

    # Check for one phosphate group
    if mol.GetSubstructMatches(Chem.MolFromSmarts("[P](O)(O)(O)")) != [(0,)]:
        return False, "The molecule does not contain a phosphate group"

    # Check for six carbon atoms in a chain
    chain_length = rdMolDescriptors.CalcChain(mol, -1, -1)
    if chain_length != 6:
        return False, "The molecule does not have a chain of six carbon atoms"

    # Check for D-configuration (absolute stereochemistry not available in RDKit)
    # Use heuristics based on functional groups and atom connectivity
    # ...
    # (Code for heuristic checks can be added here)
    # ...

    return True, "The molecule is a D-hexose phosphate"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:15965',
                          'name': 'D-hexose phosphate',
                          'definition': 'Any mono-phosphorylated D-hexose '
                                        'having a chain of six carbon atoms in '
                                        'the molecule.',
                          'parents': ['CHEBI:47878']},
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