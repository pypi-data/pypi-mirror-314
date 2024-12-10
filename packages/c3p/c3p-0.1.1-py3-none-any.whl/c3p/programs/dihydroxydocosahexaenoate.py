"""
Classifies: CHEBI:136528 dihydroxydocosahexaenoate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_dihydroxydocosahexaenoate(smiles: str):
    """
    Determines if a molecule is a dihydroxydocosahexaenoate, i.e., a hydroxy polyunsaturated fatty acid anion
    obtained by the deprotonation of the carboxy group of any dihydroxydocosahexaenoic acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a dihydroxydocosahexaenoate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for C22 molecule
    if mol.GetNumAtoms() != 22:
        return False, "The molecule is not a C22 compound"

    # Check for anion
    formal_charge = Descriptors.FormalCharge(mol)
    if formal_charge != -1:
        return False, "The molecule is not an anion"

    # Check for carboxylate group
    carboxylate_found = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetFormalCharge() == 0 and atom.GetTotalNumHs() == 0:
            neighbors = [mol.GetAtomWithIdx(neighbor_idx) for neighbor_idx in atom.GetNeighbors()]
            if len(neighbors) == 3 and all(neighbor.GetSymbol() == 'O' for neighbor in neighbors):
                carboxylate_found = True
                break

    if not carboxylate_found:
        return False, "No carboxylate group found"

    # Check for six double bonds
    num_double_bonds = Chem.rdMolDescriptors.CalcNumAromaticRings(mol)
    if num_double_bonds != 6:
        return False, "The molecule does not have six double bonds"

    # Check for two hydroxy groups
    num_hydroxy_groups = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetTotalNumHs() == 1:
            num_hydroxy_groups += 1

    if num_hydroxy_groups != 2:
        return False, "The molecule does not have two hydroxy groups"

    return True, "The molecule is a dihydroxydocosahexaenoate"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:136528',
                          'name': 'dihydroxydocosahexaenoate',
                          'definition': 'A hydroxy polyunsaturated fatty acid '
                                        'anion obtained by the deprotonation '
                                        'of the carboxy group of any '
                                        'dihydroxydocosahexaenoic acid.',
                          'parents': ['CHEBI:131864', 'CHEBI:131871']},
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
    'error': "module 'rdkit.Chem.Descriptors' has no attribute 'FormalCharge'",
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