"""
Classifies: CHEBI:132539 fatty acid 20:4
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_fatty_acid_20_4(smiles: str):
    """
    Determines if a molecule is a polyunsaturated fatty acid with 20 carbons and 4 double bonds.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a fatty acid 20:4, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has a carboxylic acid group
    if not any(atom.GetSymbol() == 'O' and sum(mol.GetAtomWithIdx(i).GetTotalNumHs() for i in atom.GetNeighbors()) == 1 for atom in mol.GetAtoms()):
        return False, "No carboxylic acid group found"

    # Check if the molecule has 20 carbon atoms
    if Chem.MolFromSmiles(smiles).GetNumAtoms() != 22:
        return False, "Number of atoms is not 22 (expected for a 20 carbon fatty acid)"

    # Check if the molecule has 4 double bonds
    if Descriptors.NumHeteroatomicBridges(mol) != 4:
        return False, "Number of double bonds is not 4"

    return True, "Molecule is a polyunsaturated fatty acid with 20 carbons and 4 double bonds"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:132539',
                          'name': 'fatty acid 20:4',
                          'definition': 'Any polyunsaturated fatty acid '
                                        'containing 20 carbons and 4 double '
                                        'bonds.',
                          'parents': ['CHEBI:26208']},
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