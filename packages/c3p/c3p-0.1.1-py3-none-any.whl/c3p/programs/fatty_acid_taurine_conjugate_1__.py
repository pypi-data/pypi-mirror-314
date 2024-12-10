"""
Classifies: CHEBI:132040 fatty acid-taurine conjugate(1-)
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_fatty_acid_taurine_conjugate_1__(smiles: str):
    """
    Determines if a molecule is a fatty acid-taurine conjugate(1-) anion.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a fatty acid-taurine conjugate(1-) anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a taurine substructure
    taurine_substructure = Chem.MolFromSmarts('C(C(=O)N)CS([O-])(=O)=O')
    if not mol.HasSubstructMatch(taurine_substructure):
        return False, "Molecule does not contain the taurine substructure"

    # Check for the presence of a fatty acid chain
    fatty_acid_substructure = Chem.MolFromSmarts('CCCCCCCCCCCCCCCCCCCCCCC')
    if not mol.HasSubstructMatch(fatty_acid_substructure):
        return False, "Molecule does not contain a fatty acid chain"

    # Check for the presence of a single negative charge
    formal_charge = Descriptors.FormalCharge(mol)
    if formal_charge != -1:
        return False, "Molecule does not have a single negative charge"

    return True, "Molecule is a fatty acid-taurine conjugate(1-) anion"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:132040',
                          'name': 'fatty acid-taurine conjugate(1-)',
                          'definition': 'An organosulfonate oxoanion obtained '
                                        'by deprotonation of the sulfonate '
                                        'group of any fatty acid-taurine '
                                        'conjugate; major species at pH 7.3.',
                          'parents': ['CHEBI:134249']},
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
    'num_true_negatives': 183922,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945629421008}