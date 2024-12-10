"""
Classifies: CHEBI:131878 cholanic acid anion
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_cholanic_acid_anion(smiles: str):
    """
    Determines if a molecule is a cholanic acid anion.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a cholanic acid anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for negative charge
    if Descriptors.GetFormalCharge(mol) != -1:
        return False, "Molecule does not have a negative formal charge"

    # Check for steroid skeleton
    skel = Chem.MolToSmiles(Chem.RemoveHs(mol), allBondsExplicit=True, allHsExplicit=True)
    if "C1(C2=CC3=CC=C4C5(C6=CC=C7C8(C9=CC%10C%11=C(C%12=C%13C%14=C(C(=O)O)C(CC%15C%16=C%17C(CC%18C%19=CC(=O)C%20=C%21C%22=CC%23=C%24C%25=C%26C%27=C%28C%29=C%30C%31=C%32C2)C%33)CC4)C9)C%34C%35=CC%36=C(C%37=C%38C%39=C%40C%41=C%42C%25(C)C%10=C5C%43C%44=C%45C=C%46C=C6C1" not in skel:
        return False, "Molecule does not have a cholanic acid skeleton"

    # Check for carboxylate group
    if not any(atom.GetSymbol() == 'O' and atom.GetFormalCharge() == -1 for atom in mol.GetAtoms()):
        return False, "Molecule does not contain a carboxylate group"

    return True, "Molecule is a cholanic acid anion"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131878',
                          'name': 'cholanic acid anion',
                          'definition': 'Any steroid acid anion based on a '
                                        'cholanic acid skeleton.',
                          'parents': ['CHEBI:36235']},
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
    'error': "module 'rdkit.Chem.Descriptors' has no attribute "
             "'GetFormalCharge'",
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