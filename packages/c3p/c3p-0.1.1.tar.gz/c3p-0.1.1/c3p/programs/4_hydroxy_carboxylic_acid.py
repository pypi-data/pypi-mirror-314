"""
Classifies: CHEBI:13611 4-hydroxy carboxylic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_4_hydroxy_carboxylic_acid(smiles: str):
    """
    Determines if a molecule is a 4-hydroxy carboxylic acid.
    A 4-hydroxy carboxylic acid is defined as any hydroxy carboxylic acid
    which contains a hydroxy substituent gamma to a carboxy group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 4-hydroxy carboxylic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find carboxyl and hydroxyl groups
    carboxyl_atoms = []
    hydroxyl_atoms = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and sum(mol.GetAtomWithIdx(i).GetSymbol() == 'O' for i in atom.GetNeighbors()) == 1:
            carboxyl_atoms.append(atom.GetIdx())
        elif atom.GetSymbol() == 'O' and atom.GetNumExplicitNeighbors() == 1:
            hydroxyl_atoms.append(atom.GetIdx())

    if not carboxyl_atoms or not hydroxyl_atoms:
        return False, "No carboxyl or hydroxyl groups found"

    # Check distance between hydroxyl and carboxyl groups
    for carboxyl_idx in carboxyl_atoms:
        for hydroxyl_idx in hydroxyl_atoms:
            if mol.GetAtomWithIdx(hydroxyl_idx).GetShortestPathDistanceToAtom(carboxyl_idx) == 3:
                return True, "4-hydroxy carboxylic acid structure found"

    return False, "No 4-hydroxy carboxylic acid structure found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:13611',
                          'name': '4-hydroxy carboxylic acid',
                          'definition': 'Any hydroxy carboxylic acid which '
                                        'contains a hydroxy substituent gamma '
                                        'to a carboxy group.',
                          'parents': ['CHEBI:24669']},
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
    'error': 'Python argument types in\n'
             '    Mol.GetAtomWithIdx(Mol, Atom)\n'
             'did not match C++ signature:\n'
             '    GetAtomWithIdx(RDKit::ROMol {lvalue} self, unsigned int idx)',
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