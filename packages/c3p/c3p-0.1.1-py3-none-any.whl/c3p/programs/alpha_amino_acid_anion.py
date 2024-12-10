"""
Classifies: CHEBI:33558 alpha-amino-acid anion
"""
from rdkit import Chem
from rdkit.Chem import Descriptors

def is_alpha_amino_acid_anion(smiles: str):
    """
    Determines if the molecule is an alpha-amino-acid anion.

    An alpha-amino-acid anion is defined as an amino-acid anion obtained
    by deprotonation of any alpha-amino acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is an alpha-amino-acid anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has a carboxylate group
    carboxylate = Chem.MolFromSmarts('[C&D3]([O-])=O')
    if mol.HasSubstructMatch(carboxylate):
        # Check if the molecule has an alpha-amino group
        alpha_amino = Chem.MolFromSmarts('[N;H2&D2,D3]([C&D2,D3])([C&D1])=[C&D3]')
        if mol.HasSubstructMatch(alpha_amino):
            return True, "The molecule is an alpha-amino-acid anion"
        else:
            return False, "The molecule does not have an alpha-amino group"
    else:
        return False, "The molecule does not have a carboxylate group"

# Example usage
print(is_alpha_amino_acid_anion('NC(CCO)C([O-])=O'))  # (True, 'The molecule is an alpha-amino-acid anion')
print(is_alpha_amino_acid_anion('C(=O)([O-])C(CCCCCC)N'))  # (True, 'The molecule is an alpha-amino-acid anion')
print(is_alpha_amino_acid_anion('CSCCCC(N)C([O-])=O'))  # (True, 'The molecule is an alpha-amino-acid anion')
print(is_alpha_amino_acid_anion('[H]C(=N)N[C@@H](CCC([O-])=O)C([O-])=O'))  # (False, 'The molecule does not have an alpha-amino group')
print(is_alpha_amino_acid_anion('CC(=O)N[C@@H](CSC1=CC=CC=C1)C([O-])=O'))  # (True, 'The molecule is an alpha-amino-acid anion')


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33558',
                          'name': 'alpha-amino-acid anion',
                          'definition': 'An amino-acid anion obtained by '
                                        'deprotonation of any alpha-amino '
                                        'acid.',
                          'parents': ['CHEBI:37022']},
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
    'num_true_negatives': 183685,
    'num_false_negatives': 25,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9998639159544935}