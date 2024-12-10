"""
Classifies: CHEBI:25408 monoterpene ketone
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_monoterpene_ketone(smiles: str):
    """
    Determines if a molecule is a monoterpene ketone.

    A monoterpene ketone is a terpene ketone derived from a monoterpene.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a monoterpene ketone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has a ketone group
    ketone_present = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetTotalNumHs() == 0:
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'C' and neighbor.GetTotalNumHs() == 0:
                    ketone_present = True
                    break
    if not ketone_present:
        return False, "No ketone group found"

    # Check if the molecule is a monoterpene
    mol_formula = AllChem.CalcMolFormula(mol)
    if mol_formula != 'C10H16O':
        return False, "Not a monoterpene (molecular formula is not C10H16O)"

    # Check if the molecule contains a ring
    ring_info = mol.GetRingInfo()
    if ring_info.NumRings() == 0:
        return False, "No ring found"

    # Check if the molecule is bicyclic
    if ring_info.NumRings() != 2:
        return False, "Not a bicyclic compound"

    # Check if the molecule has 4 double bonds (including the ketone)
    num_double_bonds = Descriptors.NumHeteroatomicBridges(mol)
    if num_double_bonds != 4:
        return False, "Incorrect number of double bonds"

    return True, "Molecule is a monoterpene ketone"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25408',
                          'name': 'monoterpene ketone',
                          'definition': 'A terpene ketone derived from a '
                                        'monoterpene.',
                          'parents': ['CHEBI:26872']},
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
    'success': False,
    'best': True,
    'error': "module 'rdkit.Chem.Descriptors' has no attribute "
             "'NumHeteroatomicBridges'",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}