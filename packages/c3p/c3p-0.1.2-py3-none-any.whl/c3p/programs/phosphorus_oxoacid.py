"""
Classifies: CHEBI:33457 phosphorus oxoacid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_phosphorus_oxoacid(smiles: str):
    """
    Determines if a molecule is a phosphorus oxoacid.

    A phosphorus oxoacid is a pnictogen oxoacid which contains phosphorus and oxygen,
    at least one hydrogen atom bound to oxygen, and forms an ion by the loss of one or more protons.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a phosphorus oxoacid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if molecule contains phosphorus and oxygen atoms
    atoms = [atom.GetSymbol() for atom in mol.GetAtoms()]
    if 'P' not in atoms or 'O' not in atoms:
        return False, "Molecule does not contain phosphorus and oxygen atoms"

    # Check if at least one oxygen atom is bound to a hydrogen atom
    has_ox_hydrogen = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O':
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'H':
                    has_ox_hydrogen = True
                    break
        if has_ox_hydrogen:
            break

    if not has_ox_hydrogen:
        return False, "No oxygen atom is bound to a hydrogen atom"

    # Check if molecule can be ionized by losing one or more protons
    proton_pattern = Chem.MolFromSmarts("[H+]")
    hits = mol.GetSubstructMatches(proton_pattern)
    if not hits:
        return False, "Molecule cannot form an ion by losing one or more protons"

    return True, "Molecule is a phosphorus oxoacid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33457',
                          'name': 'phosphorus oxoacid',
                          'definition': 'A pnictogen oxoacid which contains '
                                        'phosphorus and oxygen, at least one '
                                        'hydrogen atom bound to oxygen, and '
                                        'forms an ion by the loss of one or '
                                        'more protons.',
                          'parents': ['CHEBI:33408', 'CHEBI:36360']},
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
    'num_true_negatives': 183913,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999891254111953}