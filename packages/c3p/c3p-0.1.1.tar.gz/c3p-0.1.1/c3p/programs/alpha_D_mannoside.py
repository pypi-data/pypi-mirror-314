"""
Classifies: CHEBI:27535 alpha-D-mannoside
"""
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors

def is_alpha_D_mannoside(smiles: str):
    """
    Determines if a molecule is an alpha-D-mannoside.

    An alpha-D-mannoside is defined as any mannoside in which the anomeric
    centre has alpha-configuration.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is an alpha-D-mannoside, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find the anomeric carbon
    anomeric_carbon = None
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetHybridization() == Chem.HybridizationType.SP2:
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'O' and neighbor.GetDegree() == 2:
                    anomeric_carbon = atom
                    break
            if anomeric_carbon:
                break

    if anomeric_carbon is None:
        return False, "No anomeric carbon found"

    # Check the stereochemistry of the anomeric carbon
    stereo = mol.GetAtomWithIdx(anomeric_carbon.GetIdx()).GetProp('_CIPCode')
    if stereo == 'R':
        alpha_anomer = True
    elif stereo == 'S':
        alpha_anomer = False
    else:
        return False, "Unable to determine stereochemistry of anomeric carbon"

    # Check for mannoside pattern
    mannoside_smarts = 'OC[C@H]1OC(O)[C@@H](O)[C@H](O)[C@@H]1O'
    mannoside_pattern = Chem.MolFromSmarts(mannoside_smarts)
    if mannoside_pattern is None:
        return False, "Error parsing SMARTS pattern"

    if mol.HasSubstructMatch(mannoside_pattern):
        if alpha_anomer:
            return True, "Molecule is an alpha-D-mannoside"
        else:
            return False, "Molecule is a beta-D-mannoside"
    else:
        return False, "Molecule does not contain a mannoside pattern"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27535',
                          'name': 'alpha-D-mannoside',
                          'definition': 'Any mannoside in which the anomeric '
                                        'centre has alpha-configuration.',
                          'parents': ['CHEBI:25169']},
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
    'error': "'_CIPCode'",
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