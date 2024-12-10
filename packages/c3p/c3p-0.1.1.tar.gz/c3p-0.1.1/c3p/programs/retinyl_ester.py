"""
Classifies: CHEBI:16179 retinyl ester
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_retinyl_ester(smiles: str):
    """
    Determines if a molecule is a retinyl ester.

    A retinyl ester is a carboxylic ester obtained by formal condensation of
    the hydroxy group of retinol with the carboxy group of any carboxylic acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a retinyl ester, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a retinol substructure
    retinol_smarts = 'C(=C)C=C(/C=C/C=C(C)/C=C/C(C)(C)CCCC(C)(C)O)'
    retinol_mol = Chem.MolFromSmarts(retinol_smarts)
    is_retinol = mol.HasSubstructMatch(retinol_mol)

    # Check for the presence of an ester group
    ester_smarts = 'C(=O)OC'
    ester_mol = Chem.MolFromSmarts(ester_smarts)
    is_ester = mol.HasSubstructMatch(ester_mol)

    if is_retinol and is_ester:
        return True, "Molecule is a retinyl ester"
    elif is_retinol:
        return False, "Molecule contains a retinol substructure but is not an ester"
    elif is_ester:
        return False, "Molecule is an ester but does not contain a retinol substructure"
    else:
        return False, "Molecule is neither a retinyl ester nor contains a retinol substructure or ester group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16179',
                          'name': 'retinyl ester',
                          'definition': 'A carboxylic ester obtained by formal '
                                        'condensation of the hydroxy group of '
                                        'retinol with the carboxy group of any '
                                        'carboxylic acid.',
                          'parents': ['CHEBI:26537', 'CHEBI:33308']},
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
    'num_true_negatives': 183919,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945628534145}