"""
Classifies: CHEBI:25372 molybdopterin cofactor
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_molybdopterin_cofactor(smiles: str):
    """
    Determines if a molecule is a molybdopterin cofactor.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a molybdopterin cofactor, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a molybdenum atom
    if mol.HasSubstructMatch(Chem.MolFromSmarts("[Mo]")):
        # Check for the presence of a pterin ring
        pterin_ring = Chem.MolFromSmarts("c1nc2[nH]cnc2n[nH]1")
        if mol.HasSubstructMatch(pterin_ring):
            # Check for the presence of sulfur atoms coordinated to molybdenum
            mo_atom = next(atom for atom in mol.GetAtoms() if atom.GetSymbol() == "Mo")
            sulfur_neighbors = [nbr for nbr in mo_atom.GetNeighbors() if nbr.GetSymbol() == "S"]
            if len(sulfur_neighbors) >= 2:
                return True, "Molybdopterin cofactor with molybdenum and sulfur coordination"
            else:
                return False, "Missing sulfur coordination to molybdenum"
        else:
            return False, "Missing pterin ring"
    else:
        return False, "Missing molybdenum atom"

    return False, "Not a molybdopterin cofactor"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25372',
                          'name': 'molybdopterin cofactor',
                          'definition': 'A molybdopterin to which a metal or '
                                        'metal oxide is coordinated, and that '
                                        'acts as a prosthetic group.',
                          'parents': ['CHEBI:35203']},
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
    'num_false_positives': 0,
    'num_true_negatives': 183918,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999945628238518}