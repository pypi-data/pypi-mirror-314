"""
Classifies: CHEBI:138138 epoxy(hydroxy)icosatrienoic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_epoxy_hydroxy_icosatrienoic_acid(smiles: str):
    """
    Determines if a molecule is an epoxy(hydroxy)icosatrienoic acid.

    An epoxy(hydroxy)icosatrienoic acid is a nonclassic icosanoid that consists of any
    icosatrienoic acid carrying epoxy and hydroxy substituents.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an epoxy(hydroxy)icosatrienoic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of epoxy and hydroxy groups
    epoxy_count = sum(1 for atom in mol.GetAtoms() if atom.GetIsEpoxide())
    hydroxy_count = sum(1 for atom in mol.GetAtoms() if atom.GetHybridization() == Chem.HybridizationType.SP3 and atom.GetTotalNumHs() == 1)
    if epoxy_count == 0 or hydroxy_count == 0:
        return False, "Missing epoxy or hydroxy group"

    # Check for the presence of three double bonds
    double_bond_count = sum(1 for bond in mol.GetBonds() if bond.GetBondType() == Chem.BondType.DOUBLE)
    if double_bond_count != 3:
        return False, "Not an icosatrienoic acid (incorrect number of double bonds)"

    # Check for the presence of a carboxyl group
    carboxyl_count = sum(1 for atom in mol.GetAtoms() if atom.GetHybridization() == Chem.HybridizationType.SP2 and atom.GetTotalNumHs() == 0 and atom.GetTotalDegree() == 3)
    if carboxyl_count != 1:
        return False, "Not an icosatrienoic acid (missing or incorrect carboxyl group)"

    # Check for the correct number of carbon atoms
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if carbon_count != 20:
        return False, "Not an icosatrienoic acid (incorrect number of carbon atoms)"

    return True, "Molecule is an epoxy(hydroxy)icosatrienoic acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:138138',
                          'name': 'epoxy(hydroxy)icosatrienoic acid',
                          'definition': 'A nonclassic icosanoid that consists '
                                        'of any icosatrienoic acid carrying '
                                        'epoxy and hydroxy substituents.',
                          'parents': [   'CHEBI:140345',
                                         'CHEBI:15904',
                                         'CHEBI:61498',
                                         'CHEBI:61703',
                                         'CHEBI:73155']},
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
    'success': False,
    'best': True,
    'error': "'Atom' object has no attribute 'GetIsEpoxide'",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}