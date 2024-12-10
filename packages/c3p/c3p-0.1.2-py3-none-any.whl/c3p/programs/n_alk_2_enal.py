"""
Classifies: CHEBI:13757 n-alk-2-enal
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_n_alk_2_enal(smiles: str):
    """
    Determines if a molecule is an n-alk-2-enal, which is an enal obtained by formal dehydrogenation
    across positions 2 and 3 of any n-alkanal.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an n-alk-2-enal, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for an aldehyde group
    aldehyde_atoms = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8 and atom.GetTotalNumHs() == 1]
    if len(aldehyde_atoms) != 1:
        return False, "Molecule does not contain exactly one aldehyde group"
    aldehyde_idx = aldehyde_atoms[0]

    # Check for a carbon-carbon double bond
    double_bonds = [bond for bond in mol.GetBonds() if bond.GetBondType() == Chem.BondType.DOUBLE]
    if len(double_bonds) != 1:
        return False, "Molecule does not contain exactly one carbon-carbon double bond"
    double_bond = double_bonds[0]
    double_bond_atoms = [double_bond.GetBeginAtomIdx(), double_bond.GetEndAtomIdx()]

    # Check if the double bond is between C2 and C3
    aldehyde_atom = mol.GetAtomWithIdx(aldehyde_idx)
    aldehyde_neighbors = [atom.GetIdx() for atom in aldehyde_atom.GetNeighbors()]
    if double_bond_atoms[0] in aldehyde_neighbors and double_bond_atoms[1] in aldehyde_neighbors:
        return True, "Molecule is an n-alk-2-enal"
    else:
        return False, "Double bond is not between C2 and C3 relative to the aldehyde group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:13757',
                          'name': 'n-alk-2-enal',
                          'definition': 'An enal obtained by formal '
                                        'dehydrogenation across positions 2 '
                                        'and 3 of any n-alkanal',
                          'parents': ['CHEBI:51688']},
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
    'num_true_negatives': 183922,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945629421008}