"""
Classifies: CHEBI:131867 hydroxydocosahexaenoate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_hydroxydocosahexaenoate(smiles: str):
    """
    Determines if a molecule is a hydroxydocosahexaenoate (a hydroxy polyunsaturated fatty acid anion obtained by the deprotonation of the carboxy group of any hydroxydocosahexaenoic acid).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hydroxydocosahexaenoate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for anionic charge
    charge = AllChem.GetFormalCharge(mol)
    if charge != -1:
        return False, "Molecule is not an anion"

    # Check for carboxylate group
    carboxylate_found = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == -1:
            carboxylate_found = True
            break
    if not carboxylate_found:
        return False, "No carboxylate group found"

    # Check for hydroxy group
    hydroxy_found = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == 0 and atom.GetHybridization() == Chem.HybridizationType.SP3:
            hydroxy_found = True
            break
    if not hydroxy_found:
        return False, "No hydroxy group found"

    # Check for polyunsaturated fatty acid chain
    num_double_bonds = Descriptors.NumHDonors(mol) + 1  # Carboxylate group contributes one double bond
    if num_double_bonds != 6:
        return False, "Incorrect number of double bonds for a docosahexaenoate"

    # Check for 22 carbon atoms
    if mol.GetNumAtoms() != 24:
        return False, "Incorrect number of atoms for a docosahexaenoate"

    return True, "Molecule is a hydroxydocosahexaenoate"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131867',
                          'name': 'hydroxydocosahexaenoate',
                          'definition': 'A hydroxy polyunsaturated fatty acid '
                                        'anion obtained by the deprotonation '
                                        'of the carboxy group of any '
                                        'hydroxydocosahexaenoic acid.',
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
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 0,
    'num_false_positives': 11,
    'num_true_negatives': 183914,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999347563694094}