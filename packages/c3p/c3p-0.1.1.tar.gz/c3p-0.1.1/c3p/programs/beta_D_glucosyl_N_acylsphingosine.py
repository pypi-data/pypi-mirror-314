"""
Classifies: CHEBI:22801 beta-D-glucosyl-N-acylsphingosine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_beta_D_glucosyl_N_acylsphingosine(smiles: str):
    """
    Determines if a molecule is a beta-D-glucosyl-N-acylsphingosine.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a beta-D-glucosyl-N-acylsphingosine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a glucosyl head group
    glucosyl_head = Chem.MolFromSmiles('O[C@@H]1[C@H](O)[C@H](O)[C@@H](O)[C@H](O)[C@H]1O')
    if not mol.HasSubstructMatch(glucosyl_head):
        return False, "No glucosyl head group found"

    # Check for beta configuration at the anomeric center
    anomeric_atom = mol.GetAtomWithIdx(0)
    if anomeric_atom.GetHybridization() != Chem.HybridizationType.SP3 or \
       anomeric_atom.GetTotalNumHs() != 0:
        return False, "Anomeric center is not in beta configuration"

    # Check for the presence of an acyl group
    acyl_group = Chem.MolFromSmiles('CC(=O)')
    if not mol.HasSubstructMatch(acyl_group):
        return False, "No acyl group found"

    # Check for the presence of a sphingosine chain
    sphingosine_chain = Chem.MolFromSmiles('C=CCCCCCCCCCCCC')
    if not mol.HasSubstructMatch(sphingosine_chain):
        return False, "No sphingosine chain found"

    return True, "Molecule is a beta-D-glucosyl-N-acylsphingosine"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22801',
                          'name': 'beta-D-glucosyl-N-acylsphingosine',
                          'definition': 'A D-glucosyl-N-acylsphingosine in '
                                        'which the glucosyl head group has '
                                        'beta-configuration at the anomeric '
                                        'centre.',
                          'parents': ['CHEBI:18368', 'CHEBI:83264']},
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
    'num_false_positives': 45,
    'num_true_negatives': 183878,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9997498966964616}