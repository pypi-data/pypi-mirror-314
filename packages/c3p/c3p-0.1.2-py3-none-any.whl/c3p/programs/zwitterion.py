"""
Classifies: CHEBI:27369 zwitterion
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_zwitterion(smiles: str):
    """
    Determines if a molecule is a zwitterion (a neutral compound having formal unit electrical charges of opposite sign on non-adjacent atoms).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a zwitterion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Calculate formal charges for each atom
    formal_charges = [atom.GetFormalCharge() for atom in mol.GetAtoms()]

    # Check if there are both positive and negative charges
    has_positive_charge = any(charge > 0 for charge in formal_charges)
    has_negative_charge = any(charge < 0 for charge in formal_charges)

    if not has_positive_charge or not has_negative_charge:
        return False, "No formal charges of opposite signs found"

    # Check if positive and negative charges are on adjacent atoms
    atoms_with_charge = [atom for atom in mol.GetAtoms() if atom.GetFormalCharge() != 0]
    for atom1 in atoms_with_charge:
        for atom2 in atoms_with_charge:
            if atom1.GetIdx() != atom2.GetIdx() and mol.GetBondBetweenAtoms(atom1.GetIdx(), atom2.GetIdx()) is not None:
                return False, "Charges are on adjacent atoms"

    return True, "Molecule is a zwitterion"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27369',
                          'name': 'zwitterion',
                          'definition': 'A neutral compound having formal unit '
                                        'electrical charges of opposite sign '
                                        'on non-adjacent atoms. Sometimes '
                                        'referred to as inner salts, dipolar '
                                        'ions (a misnomer).',
                          'parents': ['CHEBI:51151']},
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
    'num_true_positives': 302,
    'num_false_positives': 100,
    'num_true_negatives': 4787,
    'num_false_negatives': 10,
    'num_negatives': None,
    'precision': 0.7512437810945274,
    'recall': 0.967948717948718,
    'f1': 0.84593837535014,
    'accuracy': 0.9788420850163493}