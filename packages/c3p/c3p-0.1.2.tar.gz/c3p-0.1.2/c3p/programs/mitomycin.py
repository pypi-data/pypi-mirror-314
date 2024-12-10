"""
Classifies: CHEBI:25357 mitomycin
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_mitomycin(smiles: str):
    """
    Determines if a molecule is a mitomycin, a family of aziridine-containing natural products
    isolated from Streptomyces caespitosus or Streptomyces lavendulae.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a mitomycin, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of an aziridine ring
    aziridine_ring = AllChem.IsMoleculeReactiveWithSingleAzirineFormed(mol)
    if not aziridine_ring:
        return False, "No aziridine ring found"

    # Check for the presence of an amide functional group
    amide_groups = AllChem.GetMolAmides(mol)
    if not amide_groups:
        return False, "No amide functional group found"

    # Check for the presence of a carboxylic acid functional group
    carboxylic_acids = AllChem.GetMolCarboxylicAcids(mol)
    if not carboxylic_acids:
        return False, "No carboxylic acid functional group found"

    # Check for the presence of a secondary amine functional group
    sec_amines = AllChem.GetMolSecondaryAmines(mol)
    if not sec_amines:
        return False, "No secondary amine functional group found"

    return True, "The molecule is a mitomycin"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25357',
                          'name': 'mitomycin',
                          'definition': 'A family of aziridine-containing '
                                        'natural products isolated from '
                                        'Streptomyces caespitosus or '
                                        'Streptomyces lavendulae.',
                          'parents': [   'CHEBI:23003',
                                         'CHEBI:25830',
                                         'CHEBI:38303']},
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
    'error': "module 'rdkit.Chem.AllChem' has no attribute "
             "'IsMoleculeReactiveWithSingleAzirineFormed'",
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