"""
Classifies: CHEBI:136442 desulfoglucosinolic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_desulfoglucosinolic_acid(smiles: str):
    """
    Determines if a molecule is a desulfoglucosinolic acid.

    A desulfoglucosinolic acid is defined as a beta-D-thioglucoside formed by the formal condensation
    of the thiol group of an N-hydroxyimidothioate with beta-D-glucose.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a desulfoglucosinolic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a glucose moiety
    glucose_pattern = Chem.MolFromSmarts('OC[C@H]1O[C@@H](CO)[C@@H](O)[C@H](O)[C@H]1O')
    if not mol.HasSubstructMatch(glucose_pattern):
        return False, "Molecule does not contain a glucose moiety"

    # Check for the presence of an N-hydroxyimidothioate moiety
    imidothioate_pattern = Chem.MolFromSmarts('S(=NC)NO')
    if not mol.HasSubstructMatch(imidothioate_pattern):
        return False, "Molecule does not contain an N-hydroxyimidothioate moiety"

    # Check for the formal condensation of the thiol group of N-hydroxyimidothioate with glucose
    thiol_glucose_bond = None
    for bond in mol.GetBonds():
        atom1 = mol.GetAtomWithIdx(bond.GetBeginAtomIdx())
        atom2 = mol.GetAtomWithIdx(bond.GetEndAtomIdx())
        if atom1.GetSymbol() == 'S' and atom2.GetIsInRing() and atom2.GetIsInRingSize(6):
            thiol_glucose_bond = bond
            break

    if thiol_glucose_bond is None:
        return False, "N-hydroxyimidothioate moiety is not formally condensed with glucose"

    return True, "Molecule is a desulfoglucosinolic acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:136442',
                          'name': 'desulfoglucosinolic acid',
                          'definition': 'A beta-D-thioglucoside formed by the '
                                        'formal condensation of the thiol '
                                        'group of an N-hydroxyimidothioate '
                                        'with beta-D-glucose.',
                          'parents': ['CHEBI:136428', 'CHEBI:136440']},
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