"""
Classifies: CHEBI:25223 methanesulfonate ester
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_methanesulfonate_ester(smiles: str):
    """
    Determines if a molecule is a methanesulfonate ester.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a methanesulfonate ester, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all sulfur atoms
    sulfur_atoms = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == 'S']

    # Check if there is exactly one sulfur atom
    if len(sulfur_atoms) != 1:
        return False, "Molecule does not contain exactly one sulfur atom"

    sulfur_atom = mol.GetAtomWithIdx(sulfur_atoms[0])

    # Check if the sulfur atom has four neighbors
    if len(sulfur_atom.GetNeighbors()) != 4:
        return False, "Sulfur atom does not have four neighbors"

    # Check if one neighbor is an oxygen atom with a double bond
    has_double_bonded_oxygen = False
    for neighbor in sulfur_atom.GetNeighbors():
        if neighbor.GetSymbol() == 'O' and mol.GetBondBetweenAtoms(sulfur_atom.GetIdx(), neighbor.GetIdx()).GetBondType() == Chem.BondType.DOUBLE:
            has_double_bonded_oxygen = True
            break

    if not has_double_bonded_oxygen:
        return False, "Sulfur atom does not have a double-bonded oxygen neighbor"

    # Check if another neighbor is an oxygen atom with a single bond
    has_single_bonded_oxygen = False
    for neighbor in sulfur_atom.GetNeighbors():
        if neighbor.GetSymbol() == 'O' and mol.GetBondBetweenAtoms(sulfur_atom.GetIdx(), neighbor.GetIdx()).GetBondType() == Chem.BondType.SINGLE:
            has_single_bonded_oxygen = True
            break

    if not has_single_bonded_oxygen:
        return False, "Sulfur atom does not have a single-bonded oxygen neighbor"

    # Check if the remaining neighbors are carbon atoms
    remaining_neighbors = [neighbor for neighbor in sulfur_atom.GetNeighbors() if neighbor.GetSymbol() != 'O']
    if not all(neighbor.GetSymbol() == 'C' for neighbor in remaining_neighbors):
        return False, "Remaining neighbors of sulfur atom are not carbon atoms"

    return True, "Molecule is a methanesulfonate ester"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25223',
                          'name': 'methanesulfonate ester',
                          'definition': 'An organosulfonic ester resulting '
                                        'from the formal condensation of '
                                        'methanesulfonic acid with the hydroxy '
                                        'group of an alcohol, phenol, '
                                        'heteroarenol, or enol.',
                          'parents': ['CHEBI:48544', 'CHEBI:83347']},
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
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 6434,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.9846977811782709}