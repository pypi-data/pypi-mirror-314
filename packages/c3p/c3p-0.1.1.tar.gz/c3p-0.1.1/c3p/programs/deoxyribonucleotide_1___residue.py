"""
Classifies: CHEBI:140284 deoxyribonucleotide(1-) residue
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_deoxyribonucleotide_1___residue(smiles: str):
    """
    Determines if a molecule is a deoxyribonucleotide(1-) residue.

    A deoxyribonucleotide(1-) residue is an organic anionic group obtained by deprotonation
    of the phosphate OH group of any deoxyribonucleotide residue, with major species at pH 7.3.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a deoxyribonucleotide(1-) residue, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a deoxyribose sugar
    deoxyribose = mol.GetSubstructMatches(Chem.MolFromSmarts('[C@H]2([C@@H]([C@H]([C@H](O2)O)O)O)CO'))
    if not deoxyribose:
        return False, "Molecule does not contain a deoxyribose sugar"

    # Check for the presence of a phosphate group
    phosphate = mol.GetSubstructMatches(Chem.MolFromSmarts('OP([O-])(=O)[O-]'))
    if not phosphate:
        return False, "Molecule does not contain a phosphate group"

    # Check for the presence of a nucleobase
    nucleobases = ['C1=NC(=O)NC(=O)N1', 'N1C=NC2=C1N=CN=C2N', 'N1C=NC(=O)NC1=O', 'C1=NC(=O)NC(=O)N1']
    has_nucleobase = False
    for smarts in nucleobases:
        if mol.HasSubstructMatch(Chem.MolFromSmarts(smarts)):
            has_nucleobase = True
            break
    if not has_nucleobase:
        return False, "Molecule does not contain a nucleobase"

    return True, "Molecule is a deoxyribonucleotide(1-) residue"

# Example usage
smiles = "N1([C@@H]2O[C@H](COP([O-])(*)=O)[C@H](C2)O*)C(NC(=O)C=C1)=O"
is_deoxyribo, reason = is_deoxyribonucleotide_1___residue(smiles)
print(is_deoxyribo, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:140284',
                          'name': 'deoxyribonucleotide(1-) residue',
                          'definition': 'An organic anionic group obtained by '
                                        'deprotonation of the phosphate OH '
                                        'group of any deoxyribonucleotide '
                                        'residue; major species at pH 7.3.',
                          'parents': ['CHEBI:64775']},
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
    'num_true_negatives': 183925,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945630307842}