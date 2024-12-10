"""
Classifies: CHEBI:18222 xylose
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_xylose(smiles: str):
    """
    Determines if a molecule is an xylose (an aldopentose).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an xylose, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has 5 carbon atoms
    if mol.GetNumAtoms() != 16:  # 5 carbons, 5 oxygens, 6 hydrogens
        return False, "Molecule does not have the correct number of atoms for xylose"

    # Check if the molecule has an aldehyde group
    aldehyde_atoms = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8 and atom.GetTotalNumHs() == 0]
    if len(aldehyde_atoms) != 1:
        return False, "Molecule does not contain a single aldehyde group"

    # Check if the molecule has 4 hydroxyl groups
    hydroxyl_atoms = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8 and atom.GetTotalNumHs() == 1]
    if len(hydroxyl_atoms) != 4:
        return False, "Molecule does not contain 4 hydroxyl groups"

    # Check if the molecule is pentose (5-membered ring)
    ring_info = mol.GetRingInfo()
    rings = ring_info.AtomRings()
    if not any(len(ring) == 5 for ring in rings):
        return False, "Molecule does not contain a 5-membered ring"

    # Check if the molecule is an aldose (aldehyde carbon is part of the ring)
    aldehyde_atom = mol.GetAtomWithIdx(aldehyde_atoms[0])
    ring_atoms = rings[0]  # Assuming only one ring
    if aldehyde_atom.GetIdx() not in ring_atoms:
        return False, "Aldehyde carbon is not part of the ring"

    return True, "Molecule is an xylose"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18222',
                          'name': 'xylose',
                          'definition': 'An aldopentose, found in the embryos '
                                        'of most edible plants and used in '
                                        'medicine to test for malabsorption by '
                                        'administration in water to the '
                                        'patient.',
                          'parents': ['CHEBI:33916']},
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
    'num_true_negatives': 183921,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.999994562912539}