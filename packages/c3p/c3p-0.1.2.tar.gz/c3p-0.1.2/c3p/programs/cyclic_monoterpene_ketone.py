"""
Classifies: CHEBI:23446 cyclic monoterpene ketone
"""
from rdkit import Chem
from rdkit.Chem import Descriptors

def is_cyclic_monoterpene_ketone(smiles: str):
    """
    Determines if a molecule is a cyclic monoterpene ketone.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a cyclic monoterpene ketone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule is cyclic
    if not Chem.GetSSSR(mol):
        return False, "Not a cyclic molecule"

    # Check if the molecule contains a carbonyl group
    has_carbonyl = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and sum(bond.GetBondType() == Chem.BondType.DOUBLE for bond in atom.GetBonds()) == 1:
            has_carbonyl = True
            break
    if not has_carbonyl:
        return False, "No carbonyl group found"

    # Check if the molecule is a monoterpene
    num_carbon_atoms = sum(atom.GetSymbol() == 'C' for atom in mol.GetAtoms())
    if num_carbon_atoms != 10:
        return False, "Not a monoterpene (incorrect number of carbon atoms)"

    # If all conditions are met, it's a cyclic monoterpene ketone
    return True, "Cyclic monoterpene ketone"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23446',
                          'name': 'cyclic monoterpene ketone',
                          'definition': 'A cyclic terpene ketone in which the '
                                        'terpene specified is monoterpene.',
                          'parents': ['CHEBI:25408', 'CHEBI:36130']},
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
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 5396,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.9818082590503912}