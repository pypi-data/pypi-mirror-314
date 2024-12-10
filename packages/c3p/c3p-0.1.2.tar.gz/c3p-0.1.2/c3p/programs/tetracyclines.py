"""
Classifies: CHEBI:26895 tetracyclines
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_tetracyclines(smiles: str):
    """
    Determines if a molecule is a tetracycline.

    Tetracyclines are a subclass of polyketides having an octahydrotetracene-2-carboxamide
    skeleton, substituted with many hydroxy and other groups.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a tetracycline, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of the tetracycline scaffold
    scaffold = Chem.MolFromSmiles('C1=CC2=C(C=C1)C3=C(C(=O)C4=C3C(=CC(=C4)O)O)C(=O)C2=C(C(=O)N)O')
    matches = mol.GetSubstructMatches(scaffold, useChirality=True)

    if not matches:
        return False, "Tetracycline scaffold not found"

    # Check for the presence of hydroxy and amino groups
    hydroxy_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and atom.GetIsAromatic() == False)
    amino_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'N' and atom.GetIsAromatic() == False)

    if hydroxy_count < 1 or amino_count < 1:
        return False, "Insufficient hydroxy or amino groups"

    # Check for the presence of substituents
    substituents = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() not in ['C', 'O', 'N', 'H']:
            substituents.append(atom.GetSymbol())

    if substituents:
        return True, f"Tetracycline with substituents: {', '.join(set(substituents))}"
    else:
        return True, "Unsubstituted tetracycline"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26895',
                          'name': 'tetracyclines',
                          'definition': 'A subclass of polyketides having an '
                                        'octahydrotetracene-2-carboxamide '
                                        'skeleton, substituted with many '
                                        'hydroxy and other groups.',
                          'parents': ['CHEBI:26188']},
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
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183858,
    'num_false_negatives': 7,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999619285889103}