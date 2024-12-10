"""
Classifies: CHEBI:143016 ultra-long-chain primary fatty alcohol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_ultra_long_chain_primary_fatty_alcohol(smiles: str):
    """
    Determines if a molecule is an ultra-long-chain primary fatty alcohol.
    Ultra-long-chain primary fatty alcohols are defined as any primary fatty alcohol with a chain length greater than C27.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is an ultra-long-chain primary fatty alcohol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains an OH group
    oh_atom = None
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetHybridization() == Chem.HybridizationType.SP3:
            oh_atom = atom
            break

    if oh_atom is None:
        return False, "Molecule does not contain an OH group"

    # Check if the OH group is terminal
    if len(oh_atom.GetNeighbors()) != 1:
        return False, "OH group is not terminal"

    # Check if the molecule is a primary alcohol
    carbon_atom = oh_atom.GetNeighbors()[0]
    if carbon_atom.GetDegree() != 2:
        return False, "Not a primary alcohol"

    # Calculate the chain length
    chain_length = len(Chem.MolToSmiles(mol).split('.')[0]) - 1  # Subtract 1 to account for the OH group

    if chain_length > 27:
        return True, f"Ultra-long-chain primary fatty alcohol with chain length {chain_length}"
    else:
        return False, f"Chain length is {chain_length}, which is not greater than 27"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:143016',
                          'name': 'ultra-long-chain primary fatty alcohol',
                          'definition': 'Any primary fatty alcohol with a '
                                        'chain length greater than C27.',
                          'parents': ['CHEBI:142622', 'CHEBI:197505']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: module 'rdkit.Chem.rdMolDescriptors' has no "
               "attribute 'GetSMILESLength'",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 995,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.9087591240875912}