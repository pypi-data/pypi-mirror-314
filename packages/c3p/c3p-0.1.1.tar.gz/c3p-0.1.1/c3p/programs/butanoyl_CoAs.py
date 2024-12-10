"""
Classifies: CHEBI:22954 butanoyl-CoAs
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_butanoyl_CoAs(smiles: str):
    """
    Determines if a molecule is a butanoyl-CoA or a substituted derivative.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a butanoyl-CoA or a substituted derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find the CoA substructure
    coa_pattern = Chem.MolFromSmarts('CSCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(=O)(O)OP(=O)(O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12')
    match = mol.GetSubstructMatches(coa_pattern)

    if not match:
        return False, "CoA substructure not found"

    # Find the butanoyl group
    butanoyl_pattern = Chem.MolFromSmarts('CCC(=O)')
    match = mol.GetSubstructMatches(butanoyl_pattern)

    if not match:
        return False, "Butanoyl group not found"

    # Check if the butanoyl group is connected to the CoA substructure
    butanoyl_atom_idx = match[0][2]
    coa_atom_idx = match[0][0]

    if not mol.GetBondBetweenAtoms(butanoyl_atom_idx, coa_atom_idx):
        return False, "Butanoyl group not connected to CoA substructure"

    # Check for substituents on the butanoyl group
    butanoyl_atom = mol.GetAtomWithIdx(butanoyl_atom_idx)
    substituents = []
    for neighbor in butanoyl_atom.GetNeighbors():
        if neighbor.GetIdx() != match[0][1]:
            substituents.append(neighbor.GetSymbol())

    if substituents:
        return True, f"Substituted butanoyl-CoA with substituents: {', '.join(set(substituents))}"
    else:
        return True, "Unsubstituted butanoyl-CoA"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22954',
                          'name': 'butanoyl-CoAs',
                          'definition': 'Any short-chain fatty acyl-CoA in '
                                        'which the acyl group specified is '
                                        'butanoyl or its substituted '
                                        'derivative.',
                          'parents': ['CHEBI:61905']},
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
    'num_true_negatives': 183925,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999945630307842}