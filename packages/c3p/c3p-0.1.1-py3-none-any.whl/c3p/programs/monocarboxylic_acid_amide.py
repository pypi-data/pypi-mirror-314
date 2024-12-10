"""
Classifies: CHEBI:29347 monocarboxylic acid amide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_monocarboxylic_acid_amide(smiles: str):
    """
    Determines if a molecule is a monocarboxylic acid amide.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a monocarboxylic acid amide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get the amide groups
    amide_groups = [atom.GetIdx() for atom in mol.GetAtoms()
                    if atom.GetSymbol() == 'N' and atom.GetIsAromatic() == False and
                    sum(mol.GetAtomWithIdx(idx).GetTotalNumHs() for idx in atom.GetNeighbors()) >= 1]

    # Check if there is exactly one amide group
    if len(amide_groups) != 1:
        return False, "Does not contain exactly one amide group"

    amide_nitrogen = mol.GetAtomWithIdx(amide_groups[0])

    # Check if the amide is connected to a carbonyl group
    carbonyl_group = None
    for neighbor in amide_nitrogen.GetNeighbors():
        atom = mol.GetAtomWithIdx(neighbor)
        if atom.GetSymbol() == 'C' and atom.GetFormalCharge() == 0 and sum(mol.GetAtomWithIdx(idx).GetTotalNumHs() for idx in atom.GetNeighbors()) == 0:
            carbonyl_group = atom.GetIdx()
            break

    if carbonyl_group is None:
        return False, "Amide not connected to a carbonyl group"

    # Check if the carbonyl carbon is connected to a carboxyl group
    carboxyl_group = None
    for neighbor in mol.GetAtomWithIdx(carbonyl_group).GetNeighbors():
        atom = mol.GetAtomWithIdx(neighbor)
        if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == 0:
            carboxyl_group = atom.GetIdx()

    if carboxyl_group is None:
        return False, "Carbonyl carbon not connected to a carboxyl group"

    # Check if the carboxyl oxygen is connected to a carbon
    carboxyl_carbon = None
    for neighbor in mol.GetAtomWithIdx(carboxyl_group).GetNeighbors():
        atom = mol.GetAtomWithIdx(neighbor)
        if atom.GetSymbol() == 'C' and atom.GetIdx() != carbonyl_group:
            carboxyl_carbon = atom.GetIdx()
            break

    if carboxyl_carbon is None:
        return False, "Carboxyl oxygen not connected to a carbon"

    # Check if the carboxyl carbon is connected to at most one other carbon
    other_carbon_count = 0
    for neighbor in mol.GetAtomWithIdx(carboxyl_carbon).GetNeighbors():
        atom = mol.GetAtomWithIdx(neighbor)
        if atom.GetSymbol() == 'C' and atom.GetIdx() != carboxyl_group:
            other_carbon_count += 1
            if other_carbon_count > 1:
                return False, "Carboxyl carbon connected to more than one other carbon"

    return True, "Molecule is a monocarboxylic acid amide"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:29347',
                          'name': 'monocarboxylic acid amide',
                          'definition': 'A carboxamide derived from a '
                                        'monocarboxylic acid.',
                          'parents': ['CHEBI:37622']},
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