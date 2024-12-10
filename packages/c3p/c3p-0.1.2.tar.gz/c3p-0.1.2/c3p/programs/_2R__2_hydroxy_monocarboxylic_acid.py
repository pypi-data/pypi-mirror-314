"""
Classifies: CHEBI:17893 (2R)-2-hydroxy monocarboxylic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is__2R__2_hydroxy_monocarboxylic_acid(smiles: str):
    """
    Determines if a molecule is a (2R)-2-hydroxy monocarboxylic acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a (2R)-2-hydroxy monocarboxylic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains a carboxylic acid group
    if not any(atom.GetSymbol() == 'O' and atom.GetDegree() == 1 for atom in mol.GetAtoms()):
        return False, "No carboxylic acid group found"

    # Check if the molecule contains a hydroxyl group
    if not any(atom.GetSymbol() == 'O' and atom.GetDegree() == 2 for atom in mol.GetAtoms()):
        return False, "No hydroxyl group found"

    # Find the chiral center
    chiral_centers = Chem.FindMolChiralCenters(mol, includeUnspecified=True)
    if len(chiral_centers) != 1:
        return False, "Incorrect number of chiral centers"

    chiral_atom_idx = chiral_centers[0][0]
    chiral_atom = mol.GetAtomWithIdx(chiral_atom_idx)

    # Check if the chiral atom is carbon
    if chiral_atom.GetSymbol() != 'C':
        return False, "Chiral center is not a carbon atom"

    # Check if the chiral atom has both a hydroxy and a carboxyl group
    hydroxy_neighbor = None
    carboxyl_neighbor = None
    for neighbor in chiral_atom.GetNeighbors():
        if neighbor.GetSymbol() == 'O' and neighbor.GetDegree() == 2:
            hydroxy_neighbor = neighbor
        elif neighbor.GetSymbol() == 'O' and neighbor.GetDegree() == 1:
            carboxyl_neighbor = neighbor

    if hydroxy_neighbor is None or carboxyl_neighbor is None:
        return False, "Chiral center does not have both a hydroxy and a carboxyl group"

    # Check if the configuration is (2R)
    config = chiral_centers[0][1]
    if config != 'R':
        return False, "Configuration is not (2R)"

    return True, "The molecule is a (2R)-2-hydroxy monocarboxylic acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17893',
                          'name': '(2R)-2-hydroxy monocarboxylic acid',
                          'definition': 'A 2-hydroxy monocarboxylic acid '
                                        'having (2R)-configuration.',
                          'parents': ['CHEBI:49302']},
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
    'error': 'FindMolChiralCenters() got an unexpected keyword argument '
             "'includeUnspecified'",
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