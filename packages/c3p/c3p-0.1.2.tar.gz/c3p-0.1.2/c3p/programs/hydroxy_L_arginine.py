"""
Classifies: CHEBI:24658 hydroxy-L-arginine
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hydroxy_L_arginine(smiles: str):
    """
    Determines if a molecule is a hydroxy-L-arginine.

    A hydroxy-L-arginine is defined as a hydroxy-amino acid that is L-arginine
    substituted by at least one hydroxy group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hydroxy-L-arginine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has an L-arginine substructure
    pattern = Chem.MolFromSmarts('NC(=[NH2+])NCCC[C@@H]([NH3+])C(=O)[O-]')
    matches = mol.GetSubstructMatches(pattern)

    if not matches:
        return False, "Not an L-arginine derivative"

    # Check for the presence of at least one hydroxy group
    has_hydroxy = False
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() == 8 and atom.GetTotalNumHs() > 0:
            if any(neighbor.GetAtomicNum() == 6 for neighbor in atom.GetNeighbors()):
                has_hydroxy = True
                break

    if has_hydroxy:
        return True, "Molecule is a hydroxy-L-arginine"
    else:
        return False, "No hydroxy group attached to carbon found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24658',
                          'name': 'hydroxy-L-arginine',
                          'definition': 'A hydroxy-amino acid that is '
                                        'L-arginine substituted by at least '
                                        'one hydroxy group.',
                          'parents': ['CHEBI:24662', 'CHEBI:83965']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.2222222222222222 is too low.\n'
               'True positives: '
               "[('O=C([O-])[C@@H]([NH3+])C[C@@H](CNC(=[NH2+])N)O', 'Molecule "
               "is a hydroxy-L-arginine')]\n"
               "False positives: [('NC(=[NH2+])NC(O)CC[C@H]([NH3+])C([O-])=O', "
               "'Molecule is a hydroxy-L-arginine'), "
               "('NC(=[NH2+])NCC[C@H](O)[C@H]([NH3+])C([O-])=O', 'Molecule is "
               "a hydroxy-L-arginine'), "
               "('C([C@H]([NH3+])C(=O)[O-])CCN(C(=[NH2+])NO)C', 'Molecule is a "
               "hydroxy-L-arginine'), "
               "('C(N(C(=[NH2+])NC)O)CC[C@@H](C(=O)[O-])[NH3+]', 'Molecule is "
               "a hydroxy-L-arginine'), "
               "('Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H](NC(=[NH2+])NCCC[C@H]([NH3+])C([O-])=O)[C@H](O)[C@@H]2O)[C@@H](O)[C@H]1O', "
               "'Molecule is a hydroxy-L-arginine'), "
               "('[H][C@]1(CNC(=[NH2+])N1)[C@H](O)[C@H]([NH3+])C([O-])=O', "
               "'Molecule is a hydroxy-L-arginine'), "
               "('[NH3+][C@@H](CCCNC(=[NH2+])NO)C([O-])=O', 'Molecule is a "
               "hydroxy-L-arginine')]\n"
               'False negatives: []',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 4,
    'num_true_negatives': 183921,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.2,
    'recall': 1.0,
    'f1': 0.33333333333333337,
    'accuracy': 0.9999782521231365}