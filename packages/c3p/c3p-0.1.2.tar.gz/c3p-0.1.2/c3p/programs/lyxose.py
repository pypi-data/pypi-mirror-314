"""
Classifies: CHEBI:25097 lyxose
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_lyxose(smiles: str):
    """
    Determines if a molecule is a lyxose (an aldopentose that occurs only rarely in nature).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a lyxose, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has 5 carbon atoms
    if mol.GetNumHeavyAtoms() != 15:
        return False, "Molecule does not have 15 atoms (5 carbon atoms)"

    # Check if the molecule has an aldehyde group
    aldehyde_atoms = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == 0 and sum(1 for bond in atom.GetBonds() if bond.GetBondType() == Chem.BondType.DOUBLE) == 1]
    if not aldehyde_atoms:
        return False, "Molecule does not have an aldehyde group"

    # Check if the molecule has 4 hydroxyl groups
    hydroxyl_atoms = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == 0 and sum(1 for bond in atom.GetBonds() if bond.GetBondType() == Chem.BondType.SINGLE) == 1]
    if len(hydroxyl_atoms) != 4:
        return False, "Molecule does not have 4 hydroxyl groups"

    # Check if the molecule has a ring structure
    ring_atoms = mol.GetRingInfo().AtomRings()
    if not ring_atoms:
        return False, "Molecule does not have a ring structure"

    return True, "Molecule is a lyxose"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25097',
                          'name': 'lyxose',
                          'definition': 'An aldopentose that occurs only '
                                        'rarely in nature.',
                          'parents': ['CHEBI:33916']},
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
    'num_false_positives': 47,
    'num_true_negatives': 183874,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9997390198018725}