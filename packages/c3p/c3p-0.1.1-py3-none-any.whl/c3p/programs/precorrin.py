"""
Classifies: CHEBI:26228 precorrin
"""
from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator, AllChem

def is_precorrin(smiles: str):
    """
    Determines if a molecule is a precorrin, defined as any of the intermediates in the biosynthesis of vitamin B12 from uroporphyrinogen III that lie on the pathway before the formation of the first corrin macrocycle. The figure after 'precorrin' corresponds to the number of C-methyl groups introduced into the tetrapyrrole framework.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a precorrin, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Calculate the Morgan fingerprint
    morgan_fp = rdFingerprintGenerator.GetMorganFingerprintGenerator(radius=3, useBondTypes=True, useFeatures=True).GetFingerprint(mol)

    # Define the SMARTS patterns for precorrin structures
    precorrin_patterns = [
        "[#6]1(-[#6]-[#6]-[#6]-[#6]-1)(-[#6]-[#6](-[#6]-[#6]-[#6]-[#6]-[#6]-[#6]-1)(-[#6]-[#6]-[#6]-[#6]-1))",
        "[#6]1(-[#6]-[#6]-[#6]-[#6]-1)(-[#6]-[#6](-[#6]-[#6]-[#6]-[#6]-[#6]-[#6]-1)(-[#6]-[#6]-[#6]-[#6]-[#6]-1))",
        "[#6]1(-[#6]-[#6]-[#6]-[#6]-1)(-[#6]-[#6](-[#6]-[#6]-[#6]-[#6]-[#6]-[#6]-[#6]-1)(-[#6]-[#6]-[#6]-[#6]-[#6]-[#6]-1))",
        "[#6]1(-[#6]-[#6]-[#6]-[#6]-[#6]-1)(-[#6]-[#6](-[#6]-[#6]-[#6]-[#6]-[#6]-[#6]-[#6]-1)(-[#6]-[#6]-[#6]-[#6]-[#6]-[#6]-1))"
    ]

    # Check if any of the patterns match
    for pattern in precorrin_patterns:
        patt = Chem.MolFromSmarts(pattern)
        if mol.HasSubstructMatch(patt):
            num_methyl_groups = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C' and atom.GetTotalNumHs() == 3)
            return True, f"Precorrin with {num_methyl_groups} C-methyl groups"

    return False, "Not a precorrin structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26228',
                          'name': 'precorrin',
                          'definition': 'Any of the intermediates in the '
                                        'biosynthesis of vitamin B12 from '
                                        'uroporphyrinogen III that lie on the '
                                        'pathway before the formation of the '
                                        'first corrin macrocycle. The figure '
                                        "after 'precorrin' corresponds to the "
                                        'number of C-methyl groups introduced '
                                        'into the tetrapyrrole framework.',
                          'parents': ['CHEBI:33913']},
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
    'success': False,
    'best': True,
    'error': "module 'rdkit.Chem.rdFingerprintGenerator' has no attribute "
             "'GetMorganFingerprintGenerator'",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}