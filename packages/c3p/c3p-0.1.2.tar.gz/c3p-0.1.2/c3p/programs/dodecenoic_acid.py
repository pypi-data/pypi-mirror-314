"""
Classifies: CHEBI:23867 dodecenoic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_dodecenoic_acid(smiles: str):
    """
    Determines if a molecule is a dodecenoic acid, which is a C12, straight-chain fatty acid carrying a double bond at any position.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a dodecenoic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has 12 carbon atoms
    if Descriptors.HeavyAtomCount(mol) != 13:  # 12 carbon atoms + 1 oxygen atom in the carboxylic acid group
        return False, "The molecule does not have 12 carbon atoms"

    # Check if the molecule has a carboxylic acid group
    carboxyl_smarts = Chem.MolFromSmarts('C(=O)O')
    if not mol.HasSubstructMatch(carboxyl_smarts):
        return False, "The molecule does not have a carboxylic acid group"

    # Check if the molecule has a double bond
    double_bond_smarts = Chem.MolFromSmarts('C=C')
    if not mol.HasSubstructMatch(double_bond_smarts):
        return False, "The molecule does not have a double bond"

    # Check if the molecule is a straight chain
    AllChem.EmbedMolecule(mol)
    AllChem.MMFFOptimizeMolecule(mol)
    conf = mol.GetConformer()
    atoms = [conf.GetAtomPosition(i) for i in range(mol.GetNumAtoms())]
    distances = [(atoms[i] - atoms[i+1]).Length() for i in range(len(atoms)-1)]
    if not all(d > 1.3 and d < 1.7 for d in distances):
        return False, "The molecule is not a straight chain"

    return True, "The molecule is a dodecenoic acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23867',
                          'name': 'dodecenoic acid',
                          'definition': 'A C12, straight-chain fatty acid '
                                        'carrying a double bond at any '
                                        'position.',
                          'parents': [   'CHEBI:25413',
                                         'CHEBI:59202',
                                         'CHEBI:59554']},
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
    'num_true_negatives': 183920,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.999994562882977}