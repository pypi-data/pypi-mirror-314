"""
Classifies: CHEBI:31998 N-acylphytosphingosine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_N_acylphytosphingosine(smiles: str):
    """
    Determines if a molecule is an N-acylphytosphingosine (a ceramide that is phytosphingosine 
    having a fatty acyl group attached to the nitrogen).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an N-acylphytosphingosine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of phytosphingosine backbone
    phytosphingosine_backbone = Chem.MolFromSmiles('CCCCCCCCCCCCCCNC(CO)C(O)C(O)CCC=CCCCCCCCC')
    if not mol.HasSubstructMatch(phytosphingosine_backbone):
        return False, "Molecule does not contain the phytosphingosine backbone"

    # Check for the presence of an acyl group attached to the nitrogen
    acylated_nitrogen = Chem.MolFromSmiles('N(C(=O)C)')
    if not mol.HasSubstructMatch(acylated_nitrogen):
        return False, "Nitrogen is not N-acylated"

    # Check the length of the acyl chain
    acyl_chain_length = Descriptors.LipinskiHBACount(mol)
    if acyl_chain_length < 14 or acyl_chain_length > 32:
        return False, "Acyl chain length is not between 14 and 32 carbons"

    # Check for the presence of a galactosyl or lactosyl group
    galactosyl_group = Chem.MolFromSmiles('C(OC1C(C(C(C(O1)CO)O)O)O)O')
    lactosyl_group = Chem.MolFromSmiles('C(OC1C(C(C(C(O1)OC2C(C(C(C(O2)CO)O)O)O)O)O)O)O')
    if not (mol.HasSubstructMatch(galactosyl_group) or mol.HasSubstructMatch(lactosyl_group)):
        return False, "Molecule does not contain a galactosyl or lactosyl group"

    return True, "Molecule is an N-acylphytosphingosine"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:31998',
                          'name': 'N-acylphytosphingosine',
                          'definition': 'A ceramide that is phytosphingosine '
                                        'having a fatty acyl group attached to '
                                        'the nitrogen.',
                          'parents': ['CHEBI:139051']},
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
    'num_true_negatives': 183820,
    'num_false_negatives': 11,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999401624317987}