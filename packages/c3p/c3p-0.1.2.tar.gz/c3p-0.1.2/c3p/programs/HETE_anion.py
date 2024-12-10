"""
Classifies: CHEBI:131858 HETE anion
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_HETE_anion(smiles: str):
    """
    Determines if a molecule is a HETE anion (an icosanoid anion arising from deprotonation of the carboxylic acid function of any hydroxyicosatetraenoic acid).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a HETE anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if molecule has 20 carbon atoms
    if mol.GetNumHeavyAtoms() != 21:
        return False, "Molecule does not have 20 carbon atoms"

    # Check for 4 double bonds
    if Descriptors.BondCount(mol, 'DOUBLE') != 4:
        return False, "Molecule does not have 4 double bonds"

    # Check for 1 hydroxyl group
    if Descriptors.Desc_Fingerprint(mol).GetBitFromIdx(38) != 1:
        return False, "Molecule does not have 1 hydroxyl group"

    # Check for 1 carboxylate anion
    if Descriptors.Desc_Fingerprint(mol).GetBitFromIdx(53) != 1:
        return False, "Molecule does not have 1 carboxylate anion"

    return True, "Molecule is a HETE anion"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131858',
                          'name': 'HETE anion',
                          'definition': 'An icosanoid anion arising from '
                                        'deprotonation of the carboxylic acid '
                                        'function of any '
                                        'hydroxyicosatetraenoic acid.',
                          'parents': [   'CHEBI:131871',
                                         'CHEBI:57560',
                                         'CHEBI:62937']},
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
    'error': "module 'rdkit.Chem.Descriptors' has no attribute 'BondCount'",
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