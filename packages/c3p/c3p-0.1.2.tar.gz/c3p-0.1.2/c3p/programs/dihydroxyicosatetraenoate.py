"""
Classifies: CHEBI:131877 dihydroxyicosatetraenoate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_dihydroxyicosatetraenoate(smiles: str):
    """
    Determines if a molecule is a dihydroxyicosatetraenoate (an unsaturated fatty acid anion arising from deprotonation of the carboxylic acid function of any dihydroxyicosatetraenoic acid).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a dihydroxyicosatetraenoate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for carboxylate anion
    if not any(atom.GetFormalCharge() == -1 and atom.GetSymbol() == 'O' for atom in mol.GetAtoms()):
        return False, "No carboxylate anion found"

    # Check for 20 carbon atoms
    if mol.GetNumHeavyAtoms() != 22:
        return False, "Does not have 20 carbon atoms"

    # Check for 4 double bonds
    if Descriptors.NumHBD(mol) != 2:
        return False, "Does not have 2 hydroxyl groups"

    # Check for 4 double bonds
    if Descriptors.BondCount(mol, Descriptors.BondType.DOUBLE) != 4:
        return False, "Does not have 4 double bonds"

    return True, "Molecule is a dihydroxyicosatetraenoate"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131877',
                          'name': 'dihydroxyicosatetraenoate',
                          'definition': 'An unsaturated fatty acid anion '
                                        'arising from deprotonation of the '
                                        'carboxylic acid function of any '
                                        'dihydroxyicosatetraenoic acid.',
                          'parents': ['CHEBI:131871', 'CHEBI:62937']},
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
    'error': "module 'rdkit.Chem.Descriptors' has no attribute 'NumHBD'",
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