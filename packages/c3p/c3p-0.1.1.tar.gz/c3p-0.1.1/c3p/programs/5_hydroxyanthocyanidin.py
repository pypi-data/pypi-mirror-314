"""
Classifies: CHEBI:140277 5-hydroxyanthocyanidin
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_5_hydroxyanthocyanidin(smiles: str):
    """
    Determines if a molecule is a 5-hydroxyanthocyanidin (an anthocyanidin cation with a hydroxy substituent at position 5).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 5-hydroxyanthocyanidin, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a cationic charge
    if not AllChem.ComputeMolFormula(mol).startswith('C'):
        return False, "Molecule is not a cation"

    # Find the anthocyanidin core structure
    anthocyanidin_core = Chem.MolFromSmarts('c1cc(O)c2c(c1)oc1cc(O)cc(O)c1c2O')
    if mol.GetSubstructMatch(anthocyanidin_core) == ():
        return False, "Molecule does not contain the anthocyanidin core structure"

    # Find the position of the hydroxy substituent
    hydroxy_pattern = Chem.MolFromSmarts('OC')
    for match in mol.GetSubstructMatches(hydroxy_pattern):
        atom = mol.GetAtomWithIdx(match[0])
        if atom.GetSymbol() == 'O':
            continue
        atom_idx = atom.GetIdx()
        ring_info = mol.GetRingInfo().IsBondInRingOfSize(atom_idx, 6)
        if ring_info:
            return True, f"Molecule is a 5-hydroxyanthocyanidin with a hydroxy substituent at position {ring_info}"

    return False, "Molecule does not contain a hydroxy substituent at position 5 of the anthocyanidin core"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:140277',
                          'name': '5-hydroxyanthocyanidin',
                          'definition': 'Any anthocyanidin cation that carries '
                                        'a hydroxy substituent at position 5.',
                          'parents': ['CHEBI:16366']},
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
    'error': "module 'rdkit.Chem.AllChem' has no attribute 'ComputeMolFormula'",
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