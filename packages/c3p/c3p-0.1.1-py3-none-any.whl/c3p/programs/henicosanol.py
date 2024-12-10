"""
Classifies: CHEBI:197490 henicosanol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_henicosanol(smiles: str):
    """
    Determines if a molecule is a henicosanol (a fatty alcohol consisting of a hydroxy function
    at any position of an unbranched saturated chain of twenty-one carbon atoms).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a henicosanol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for exactly 21 carbon atoms
    if sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C') != 21:
        return False, "Molecule does not have 21 carbon atoms"

    # Check for exactly one oxygen atom
    oxygen_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')
    if oxygen_count != 1:
        return False, "Molecule does not have exactly one oxygen atom"

    # Check for one hydroxy group
    hydroxy_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and atom.GetTotalNumHs() == 1)
    if hydroxy_count != 1:
        return False, "Molecule does not have exactly one hydroxy group"

    # Check for an unbranched chain
    is_unbranched = True
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and len(atom.GetNeighbors()) > 2:
            is_unbranched = False
            break

    if not is_unbranched:
        return False, "Molecule is not an unbranched chain"

    # Check for saturation
    if not AllChem.EmbedMolecule(mol):
        return False, "Failed to embed molecule"

    if not AllChem.MMFFSanitizeMolecule(mol):
        return False, "Failed to sanitize molecule"

    is_saturated = AllChem.CalcNumRotatableBonds(mol) == 0
    if not is_saturated:
        return False, "Molecule is not saturated"

    return True, "Molecule is a henicosanol"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:197490',
                          'name': 'henicosanol',
                          'definition': 'A fatty alcohol consisting of a '
                                        'hydroxy function at any position of '
                                        'an unbranched saturated chain of '
                                        'twenty-one carbon atoms.',
                          'parents': [   'CHEBI:134179',
                                         'CHEBI:197491',
                                         'CHEBI:50584']},
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