"""
Classifies: CHEBI:132950 tartrate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_tartrate(smiles: str):
    """
    Determines if a molecule is a tartrate, which is a dicarboxylic acid anion obtained by deprotonation
    of at least one of the carboxy groups of any tartaric acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a tartrate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for dicarboxylic acid
    num_carboxyl_groups = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and atom.GetTotalNumHs() == 0)
    if num_carboxyl_groups < 2:
        return False, "Not a dicarboxylic acid"

    # Check for at least one deprotonated carboxyl group
    num_deprotonated_carboxyl_groups = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == -1)
    if num_deprotonated_carboxyl_groups == 0:
        return False, "No deprotonated carboxyl groups"

    # Check for tartaric acid backbone
    num_chiral_centers = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C' and atom.GetChiralTag() != Chem.ChiralType.CHI_UNSPECIFIED)
    if num_chiral_centers != 2:
        return False, "Not a tartaric acid backbone"

    return True, "Molecule is a tartrate"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:132950',
                          'name': 'tartrate',
                          'definition': 'A dicarboxylic acid anion obtained by '
                                        'deprotonation of at least one of the '
                                        'carboxy groups of any tartaric acid.',
                          'parents': ['CHEBI:33798', 'CHEBI:35693']},
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
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 14836,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.9933052152373302}