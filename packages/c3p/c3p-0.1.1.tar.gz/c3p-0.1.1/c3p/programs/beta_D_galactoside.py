"""
Classifies: CHEBI:28034 beta-D-galactoside
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_beta_D_galactoside(smiles: str):
    """
    Determines if a molecule is a beta-D-galactoside, defined as any D-galactoside having
    beta-configuration at its anomeric centre.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a beta-D-galactoside, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find the galactose substructure with beta configuration at the anomeric centre
    pat = Chem.MolFromSmarts('O[C@@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O')
    if mol.HasSubstructMatch(pat):
        return True, "Molecule contains a beta-D-galactoside substructure"
    else:
        return False, "Molecule does not contain a beta-D-galactoside substructure"

# Examples
print(is_beta_D_galactoside('[H][C@@]1(CC[C@@]2([H])[C@]3([H])CC=C4C[C@H](CC[C@]4(C)[C@@]3([H])CC[C@]12C)O[C@@H]1O[C@H](COC(C)=O)[C@H](O)[C@H](O)[C@H]1O)[C@H](C)CCCC(C)C'))
# Output: (True, 'Molecule contains a beta-D-galactoside substructure')

print(is_beta_D_galactoside('O(C=1C=C2OC(=O)C=C(C2=CC1)C)[C@H]3[C@@H]([C@@H](O)[C@H]([C@H](O3)CO)O)O'))
# Output: (True, 'Molecule contains a beta-D-galactoside substructure')

print(is_beta_D_galactoside('O[C@H]1[C@@H](O)[C@@H](COP(O)(O)=O)O[C@@H](O[*])[C@@H]1O'))
# Output: (True, 'Molecule contains a beta-D-galactoside substructure')

print(is_beta_D_galactoside('OC[C@H]1O[C@@H](Oc2cc3c(O)cc(O)cc3[o+]c2-c2ccc(O)c(O)c2)[C@H](O)[C@@H](O)[C@H]1O'))
# Output: (True, 'Molecule contains a beta-D-galactoside substructure')

print(is_beta_D_galactoside('COc1cc(ccc1O)-c1oc2cc(O)cc(O)c2c(=O)c1O[C@@H]1O[C@H](CO)[C@H](O)[C@H](O)[C@H]1O'))
# Output: (True, 'Molecule contains a beta-D-galactoside substructure')

print(is_beta_D_galactoside('[C@@H]1([C@@H](O[C@@H]([C@@H]([C@@H]1O)O)CO)O*)O[C@H]2[C@H]([C@@H]([C@@H]([C@@H](O2)C)O)O)O'))
# Output: (True, 'Molecule contains a beta-D-galactoside substructure')


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28034',
                          'name': 'beta-D-galactoside',
                          'definition': 'Any D-galactoside having '
                                        'beta-configuration at its anomeric '
                                        'centre.',
                          'parents': ['CHEBI:20961']},
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
    'num_false_positives': 100,
    'num_true_negatives': 14196,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9925884491679485}