"""
Classifies: CHEBI:28868 fatty acid anion
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_fatty_acid_anion(smiles: str):
    """
    Determines if a molecule is a fatty acid anion.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a fatty acid anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for carboxylate group
    has_carboxylate = any(atom.GetFormalCharge() == -1 and atom.GetTotalNumHs() == 0
                          and sum(bond.GetBondTypeAsDouble() for bond in atom.GetBonds()) == 3
                          for atom in mol.GetAtoms())
    if not has_carboxylate:
        return False, "No carboxylate group found"

    # Check for carbon chain
    carbon_chain_length = rdMolDescriptors.CalcTPSA(mol) / 9.23
    if carbon_chain_length < 4:
        return False, "Carbon chain too short"

    return True, f"Fatty acid anion with carbon chain length {int(carbon_chain_length)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28868',
                          'name': 'fatty acid anion',
                          'definition': 'The conjugate base of a fatty acid, '
                                        'arising from deprotonation of the '
                                        'carboxylic acid group of the '
                                        'corresponding fatty acid.',
                          'parents': ['CHEBI:18059', 'CHEBI:35757']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: module 'rdkit.Chem.Descriptors' has no "
               "attribute 'WHDPNBWMLSJ1024'",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 100703,
    'num_false_negatives': 99,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 0.01,
    'f1': 0.009950248756218905,
    'accuracy': 0.9980278088857616}