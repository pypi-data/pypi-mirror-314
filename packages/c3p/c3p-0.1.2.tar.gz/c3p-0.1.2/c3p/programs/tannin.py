"""
Classifies: CHEBI:26848 tannin
"""
from rdkit import Chem
from rdkit.Chem import Descriptors

def is_tannin(smiles: str):
    """
    Determines if a molecule is a tannin.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a tannin, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of polyphenolic structure
    num_aromatic_rings = Chem.Descriptors.AromaticRingCount(mol)
    if num_aromatic_rings < 2:
        return False, "Not enough aromatic rings (polyphenolic structure)"

    # Check for the presence of hydroxyl (-OH) groups
    num_hydroxyls = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and atom.GetHybridization() == Chem.HybridizationType.SP3)
    if num_hydroxyls < 5:
        return False, "Not enough hydroxyl groups"

    # Check for the presence of ester or ether linkages
    num_esters = sum(1 for bond in mol.GetBonds() if bond.GetBondType() == Chem.BondType.ESTERS)
    num_ethers = sum(1 for bond in mol.GetBonds() if bond.GetBondType() == Chem.BondType.ETHER)
    if num_esters + num_ethers < 2:
        return False, "Not enough ester or ether linkages"

    # Check for the presence of glucosides (sugar moieties)
    num_sugar_rings = sum(1 for ring in mol.GetRingInfo().AtomRings() if len(ring) == 5 or len(ring) == 6)
    if num_sugar_rings > 0:
        return True, "Contains sugar moiety (glucoside)"

    # If all criteria are met, classify as a tannin
    return True, "Polyphenolic structure with hydroxyl groups and ester/ether linkages"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26848',
                          'name': 'tannin',
                          'definition': 'Any of a group of astringent '
                                        'polyphenolic vegetable principles or '
                                        'compounds, chiefly complex glucosides '
                                        'of catechol and pyrogallol.',
                          'parents': ['CHEBI:26195']},
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
    'error': "module 'rdkit.Chem.Descriptors' has no attribute "
             "'AromaticRingCount'",
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