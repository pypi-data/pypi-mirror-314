"""
Classifies: CHEBI:141131 acyl-AMP(1-)
"""
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors

def is_acyl_AMP_1_(smiles: str):
    """
    Determines if a molecule is an acyl-AMP(1-) ion, defined as an organophosphate oxoanion obtained
    by deprotonation of the phosphate OH group of any acyl-AMP; major species at pH 7.3.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an acyl-AMP(1-) ion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of phosphate group
    has_phosphate = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'P' and atom.GetFormalCharge() == 1:
            has_phosphate = True
            break

    if not has_phosphate:
        return False, "Molecule does not contain a phosphate group"

    # Check for the presence of an acyl group
    has_acyl = False
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.DOUBLE and bond.GetBeginAtom().GetSymbol() == 'C' and bond.GetEndAtom().GetSymbol() == 'O':
            has_acyl = True
            break

    if not has_acyl:
        return False, "Molecule does not contain an acyl group"

    # Check for the presence of an AMP moiety
    has_amp = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N' and atom.GetIsAromatic():
            neighbors = [mol.GetAtomWithIdx(n).GetSymbol() for n in atom.GetNeighbors()]
            if 'C' in neighbors and 'N' in neighbors and 'C' in neighbors:
                has_amp = True
                break

    if not has_amp:
        return False, "Molecule does not contain an AMP moiety"

    return True, "Molecule is an acyl-AMP(1-) ion"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:141131',
                          'name': 'acyl-AMP(1-)',
                          'definition': 'An organophosphate oxoanion obtained '
                                        'by deprotonation of the phosphate OH '
                                        'group of any acyl-AMP; major species '
                                        'at pH 7.3.',
                          'parents': ['CHEBI:58945']},
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
    'success': False,
    'best': True,
    'error': "name 'is_acyl_AMP_1__' is not defined",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}