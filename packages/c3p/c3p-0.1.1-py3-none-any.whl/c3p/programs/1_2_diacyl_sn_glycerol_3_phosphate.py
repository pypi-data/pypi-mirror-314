"""
Classifies: CHEBI:29089 1,2-diacyl-sn-glycerol 3-phosphate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_1_2_diacyl_sn_glycerol_3_phosphate(smiles: str):
    """
    Determines if a molecule is a 1,2-diacyl-sn-glycerol 3-phosphate.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 1,2-diacyl-sn-glycerol 3-phosphate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for a phosphate group
    if not any(atom.GetSymbol() == 'P' for atom in mol.GetAtoms()):
        return False, "No phosphate group found"

    # Find the phosphate atom
    phosphate_atom = next((atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'P'), None)
    if phosphate_atom is None:
        return False, "No phosphate group found"

    # Check for three oxygen atoms bonded to the phosphate atom
    phosphate_neighbors = phosphate_atom.GetNeighbors()
    if len([neighbor for neighbor in phosphate_neighbors if neighbor.GetSymbol() == 'O']) != 3:
        return False, "Incorrect number of oxygen atoms bonded to phosphate atom"

    # Find the glycerol backbone
    glycerol_atoms = []
    for neighbor in phosphate_neighbors:
        if neighbor.GetSymbol() == 'O':
            for bonded_atom in neighbor.GetNeighbors():
                if bonded_atom.GetSymbol() == 'C':
                    glycerol_atoms.append(bonded_atom)

    if len(glycerol_atoms) != 3:
        return False, "Incorrect glycerol backbone structure"

    # Check for acyl groups at positions 1 and 2
    acyl_groups = []
    for atom in glycerol_atoms:
        for neighbor in atom.GetNeighbors():
            if neighbor.GetSymbol() == 'O' and len(neighbor.GetNeighbors()) == 2:
                acyl_atom = neighbor.GetNeighbors()[1]
                if acyl_atom.GetSymbol() == 'C':
                    acyl_groups.append(acyl_atom)

    if len(acyl_groups) != 2:
        return False, "Incorrect number of acyl groups at positions 1 and 2"

    return True, "Molecule is a 1,2-diacyl-sn-glycerol 3-phosphate"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:29089',
                          'name': '1,2-diacyl-sn-glycerol 3-phosphate',
                          'definition': 'An sn-glycerol 3-phosphate compound '
                                        'having unspecified O-acyl groups at '
                                        'the 1- and 2-positions.',
                          'parents': ['CHEBI:16337', 'CHEBI:26706']},
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
    'num_false_positives': 39,
    'num_true_negatives': 183445,
    'num_false_negatives': 45,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9995423066654316}