"""
Classifies: CHEBI:28863 flavanones
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_flavanones(smiles: str):
    """
    Determines if a molecule is a flavanone (members of the class of flavans with a 3,4-dihydro-2-aryl-2H-1-benzopyran-4-one skeleton and its substituted derivatives).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a flavanone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of the 3,4-dihydro-2-aryl-2H-1-benzopyran-4-one skeleton
    skeleton = Chem.MolFromSmiles('O1C(CC(=O)C2=C1C=CC=C2)C3=CC=CC=C3')
    if mol.GetSubstructMatch(skeleton) == []:
        return False, "3,4-dihydro-2-aryl-2H-1-benzopyran-4-one skeleton not found"

    # Check for possible substituents
    substituents = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() != 'C' and atom.GetSymbol() != 'H' and atom.GetSymbol() != 'O':
            substituents.append(atom.GetSymbol())

    if len(substituents) > 0:
        return True, f"Flavanone with substituents: {', '.join(set(substituents))}"
    else:
        return True, "Unsubstituted flavanone"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28863',
                          'name': 'flavanones',
                          'definition': 'Members of the class of flavans with '
                                        'a '
                                        '3,4-dihydro-2-aryl-2H-1-benzopyran-4-one '
                                        'skeleton and its substituted '
                                        'derivatives.',
                          'parents': ['CHEBI:38672', 'CHEBI:3992']},
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
    'num_true_positives': 37,
    'num_false_positives': 100,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.27007299270072993,
    'recall': 1.0,
    'f1': 0.42528735632183906,
    'accuracy': 0.27007299270072993}