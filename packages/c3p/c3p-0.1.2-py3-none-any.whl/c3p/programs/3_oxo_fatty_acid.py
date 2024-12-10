"""
Classifies: CHEBI:134416 3-oxo fatty acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_3_oxo_fatty_acid(smiles: str):
    """
    Determines if a molecule is a 3-oxo fatty acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 3-oxo fatty acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find the carbonyl carbon atom
    carbonyl_carbon_idx = None
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetFormalCharge() == 0 and atom.GetTotalNumHs() == 0:
            neighbors = [neighbor.GetSymbol() for neighbor in atom.GetNeighbors()]
            if 'O' in neighbors and 'O' not in neighbors[neighbors.index('O'):]:
                carbonyl_carbon_idx = atom.GetIdx()
                break

    if carbonyl_carbon_idx is None:
        return False, "No carbonyl carbon found"

    # Check if the carbonyl carbon is at position 3
    carbonyl_carbon = mol.GetAtomWithIdx(carbonyl_carbon_idx)
    chain = Chem.Mol.GetAtomBFs(mol, Chem.AtomType.AtomBFType.longCode)
    chain_len = max(len(chain[carbonyl_carbon_idx]), chain[carbonyl_carbon_idx].count('3')) + 1
    if chain_len != 4:
        return False, "Carbonyl carbon is not at position 3"

    # Check if the molecule has a carboxyl group
    carboxyl_found = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetFormalCharge() == 0 and atom.GetTotalNumHs() == 0:
            neighbors = [neighbor.GetSymbol() for neighbor in atom.GetNeighbors()]
            if 'O' in neighbors and 'O' in neighbors[neighbors.index('O')+1:]:
                carboxyl_found = True
                break

    if not carboxyl_found:
        return False, "No carboxyl group found"

    return True, "The molecule is a 3-oxo fatty acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134416',
                          'name': '3-oxo fatty acid',
                          'definition': 'Any oxo fatty acid in which an oxo '
                                        'substituent is located at position 3.',
                          'parents': ['CHEBI:47881', 'CHEBI:59644']},
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
    'num_true_negatives': 183924,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945630012234}