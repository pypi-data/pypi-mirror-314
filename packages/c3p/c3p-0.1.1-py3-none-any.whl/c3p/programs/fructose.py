"""
Classifies: CHEBI:28757 fructose
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_fructose(smiles: str):
    """
    Determines if a molecule is a fructose (a ketohexose that is an isomer of glucose).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is fructose, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has a keto group
    has_keto = any(atom.GetAtomicNum() == 8 and sum(bond.GetBondTypeAsDouble() for bond in atom.GetBonds()) == 2 for atom in mol.GetAtoms())
    if not has_keto:
        return False, "Molecule does not contain a keto group"

    # Check if the molecule is a hexose (contains 6 carbon atoms)
    num_carbons = sum(atom.GetAtomicNum() == 6 for atom in mol.GetAtoms())
    if num_carbons != 6:
        return False, "Molecule is not a hexose (does not have 6 carbon atoms)"

    # Check if the molecule is an isomer of glucose
    smiles_glucose = "OC[C@H](O)[C@@H](O)[C@H](O)[C@H](O)CO"
    mol_glucose = Chem.MolFromSmiles(smiles_glucose)
    if mol_glucose is None:
        return False, "Error processing glucose SMILES"

    if AllChem.ScalarDescriptors.GetHossepLopp(mol) == AllChem.ScalarDescriptors.GetHossepLopp(mol_glucose):
        return True, "Molecule is a fructose (a ketohexose that is an isomer of glucose)"
    else:
        return False, "Molecule is not an isomer of glucose"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28757',
                          'name': 'fructose',
                          'definition': 'A ketohexose that is an isomer of '
                                        'glucose.',
                          'parents': ['CHEBI:24973']},
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
    'error': "module 'rdkit.Chem.AllChem' has no attribute 'ScalarDescriptors'",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}