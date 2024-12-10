"""
Classifies: CHEBI:17634 D-glucose
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_D_glucose(smiles: str):
    """
    Determines if a molecule is a D-glucose, i.e., a glucose with D-configuration.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a D-glucose, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains 6 carbon atoms and 1 oxygen atom
    num_carbon_atoms = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    num_oxygen_atoms = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')
    if num_carbon_atoms != 6 or num_oxygen_atoms != 1:
        return False, "Molecule does not have the correct number of carbon (6) and oxygen (1) atoms"

    # Get the list of SMILES for each stereoisomer
    isomers = AllChem.EnumerateStereoisomers(mol)
    isomers_smiles = [Chem.MolToSmiles(isomer) for isomer in isomers]

    # Check if any of the stereoisomers match the D-glucose configuration
    d_glucose_smiles = [
        'O[C@H]1[C@@H]([C@@H]([C@H]([C@@H](O1)O)O)O)O',  # D-glucopyranose
        'O1[C@@H]([C@H](O)[C@@H](O)C1O)[C@H](O)CO'       # D-glucofuranose
    ]
    if any(smiles in isomers_smiles for smiles in d_glucose_smiles):
        return True, "Molecule is a D-glucose"
    else:
        return False, "Molecule is not a D-glucose"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17634',
                          'name': 'D-glucose',
                          'definition': 'A glucose with D-configuration.',
                          'parents': ['CHEBI:17234', 'CHEBI:17608']},
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
    'num_true_negatives': 183925,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945630307842}