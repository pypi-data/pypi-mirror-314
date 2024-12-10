"""
Classifies: CHEBI:27208 unsaturated fatty acid
"""
from rdkit import Chem
from rdkit.Chem import MolFromSmiles, Descriptors

def is_unsaturated_fatty_acid(smiles: str):
    """
    Determines if a molecule is an unsaturated fatty acid (contains at least one C=C or C#C bond).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is an unsaturated fatty acid, False otherwise
        str: Reason for classification
    """
    mol = MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if molecule contains a carboxylic acid group
    if not any(atom.GetSymbol() == 'O' and atom.GetDegree() == 1 for atom in mol.GetAtoms()):
        return False, "No carboxylic acid group found"

    # Check if molecule contains at least one C=C or C#C bond
    unsaturated = False
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.DOUBLE or bond.GetBondType() == Chem.BondType.TRIPLE:
            begin_atom = mol.GetAtomWithIdx(bond.GetBeginAtomIdx())
            end_atom = mol.GetAtomWithIdx(bond.GetEndAtomIdx())
            if begin_atom.GetSymbol() == 'C' and end_atom.GetSymbol() == 'C':
                unsaturated = True
                break

    if unsaturated:
        return True, "Molecule contains at least one C=C or C#C bond"
    else:
        return False, "No C=C or C#C bonds found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27208',
                          'name': 'unsaturated fatty acid',
                          'definition': 'Any fatty acid containing at least '
                                        'one C=C or C#C bond.',
                          'parents': ['CHEBI:35366']},
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
    'num_true_positives': 105,
    'num_false_positives': 100,
    'num_true_negatives': 230,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.5121951219512195,
    'recall': 0.9813084112149533,
    'f1': 0.6730769230769231,
    'accuracy': 0.7665903890160183}