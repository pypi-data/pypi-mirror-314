"""
Classifies: CHEBI:25524 NAD(P)
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_NAD_P_(smiles: str):
    """
    Determines if a molecule is a NAD(P) coenzyme (NAD or NADP).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a NAD(P) coenzyme, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of the NAD(P) scaffold
    nadp_scaffold = Chem.MolFromSmiles('C1=NC(=NC(=N1)N)N')
    if mol.HasSubstructMatch(nadp_scaffold):
        # Check for the presence of the nicotinamide and ribose moieties
        nicotinamide = Chem.MolFromSmarts('c1ncc(C(=O)N)cn1')
        ribose = Chem.MolFromSmarts('OC(C(O)C(O)C(O)CO)n')
        if mol.HasSubstructMatch(nicotinamide) and mol.HasSubstructMatch(ribose):
            # Check for the presence of phosphate groups
            num_phosphates = len(mol.GetSubstructMatches(Chem.MolFromSmarts('OP(O)(=O)')))
            if num_phosphates == 1:
                return True, "Molecule is NAD"
            elif num_phosphates == 2:
                return True, "Molecule is NADP"
            else:
                return False, "Incorrect number of phosphate groups for NAD(P)"
        else:
            return False, "Missing nicotinamide or ribose moiety"
    else:
        return False, "Missing NAD(P) scaffold"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25524',
                          'name': 'NAD(P)',
                          'definition': 'A coenzyme that may be NAD or NADP.',
                          'parents': ['CHEBI:37007', 'CHEBI:61293']},
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183920,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.999994562882977}