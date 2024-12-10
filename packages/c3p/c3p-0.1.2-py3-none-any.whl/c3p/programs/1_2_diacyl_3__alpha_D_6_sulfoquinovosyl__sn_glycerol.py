"""
Classifies: CHEBI:32167 1,2-diacyl-3-(alpha-D-6-sulfoquinovosyl)-sn-glycerol
"""
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_1_2_diacyl_3__alpha_D_6_sulfoquinovosyl__sn_glycerol(smiles: str):
    """
    Determines if a molecule is a 1,2-diacyl-3-(alpha-D-6-sulfoquinovosyl)-sn-glycerol.

    A glycosylglycerol derivative in which the glycosyl moiety is alpha-D-6-sulfoquinovosyl attached at O-3,
    with O-1 and O-2 both acylated.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a 1,2-diacyl-3-(alpha-D-6-sulfoquinovosyl)-sn-glycerol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has a glycerol backbone
    glycerol_atoms = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and atom.GetTotalNumHs() == 1]
    if len(glycerol_atoms) != 3:
        return False, "Molecule does not have a glycerol backbone"

    # Check if the glycosyl moiety is alpha-D-6-sulfoquinovosyl
    sulfoquinovosyl_atoms = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == 'S' and atom.GetTotalNumHs() == 0]
    if len(sulfoquinovosyl_atoms) != 1:
        return False, "Molecule does not contain a sulfoquinovosyl moiety"

    sulfoquinovosyl_atom = mol.GetAtomWithIdx(sulfoquinovosyl_atoms[0])
    if len(sulfoquinovosyl_atom.GetNeighbors()) != 4:
        return False, "Sulfoquinovosyl moiety is not properly connected"

    # Check if the sulfoquinovosyl moiety is attached to the glycerol backbone at O-3
    sulfoquinovosyl_neighbor = [neighbor.GetIdx() for neighbor in sulfoquinovosyl_atom.GetNeighbors() if neighbor.GetIdx() in glycerol_atoms]
    if len(sulfoquinovosyl_neighbor) != 1:
        return False, "Sulfoquinovosyl moiety is not attached to the glycerol backbone at O-3"

    # Check if O-1 and O-2 are acylated
    acylated_atoms = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and atom.GetTotalNumHs() == 0 and atom.GetIdx() not in sulfoquinovosyl_neighbor]
    if len(acylated_atoms) != 2:
        return False, "O-1 and O-2 are not both acylated"

    return True, "Molecule is a 1,2-diacyl-3-(alpha-D-6-sulfoquinovosyl)-sn-glycerol"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:32167',
                          'name': '1,2-diacyl-3-(alpha-D-6-sulfoquinovosyl)-sn-glycerol',
                          'definition': 'A glycosylglycerol derivative in '
                                        'which the glycosyl moiety is '
                                        'alpha-D-6-sulfoquinovosyl attached at '
                                        'O-3, with O-1 and O-2 both acylated.',
                          'parents': ['CHEBI:63427']},
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
    'num_false_positives': 13,
    'num_true_negatives': 183921,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999238861554354}