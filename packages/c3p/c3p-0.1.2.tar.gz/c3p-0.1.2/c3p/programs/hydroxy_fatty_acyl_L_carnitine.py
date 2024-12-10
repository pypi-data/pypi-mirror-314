"""
Classifies: CHEBI:133449 hydroxy-fatty acyl-L-carnitine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_hydroxy_fatty_acyl_L_carnitine(smiles: str):
    """
    Determines if a molecule is a hydroxy-fatty acyl-L-carnitine.

    A hydroxy-fatty acyl-L-carnitine is an O-acylcarnitine in which the R group
    is a hydroxylated fatty acyl chain.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hydroxy-fatty acyl-L-carnitine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if molecule contains carnitine moiety
    carnitine_smarts = "[N+](C)(C)C[C@@H](CC([O-])=O)"
    carnitine_match = mol.GetSubstructMatches(Chem.MolFromSmarts(carnitine_smarts))
    if not carnitine_match:
        return False, "Molecule does not contain the carnitine moiety"

    # Find the acyl chain attached to the carnitine
    acyl_chain_atom_idx = mol.GetSubstructMatch(Chem.MolFromSmarts("OC(=O)"))[-1]
    if acyl_chain_atom_idx == -1:
        return False, "No acyl chain found"

    acyl_chain = Chem.Mol(mol.GetTopologicalFragmentAtomIndices(acyl_chain_atom_idx, includeonly=True))

    # Check if the acyl chain contains a hydroxyl group
    hydroxyl_smarts = "[OH]"
    hydroxyl_match = acyl_chain.GetSubstructMatches(Chem.MolFromSmarts(hydroxyl_smarts))
    if not hydroxyl_match:
        return False, "Acyl chain does not contain a hydroxyl group"

    # Check if the acyl chain is a fatty acyl chain
    fatty_acyl_smarts = "[CX3](=O)[C]"
    fatty_acyl_match = acyl_chain.GetSubstructMatches(Chem.MolFromSmarts(fatty_acyl_smarts))
    if not fatty_acyl_match:
        return False, "Acyl chain is not a fatty acyl chain"

    return True, "Molecule is a hydroxy-fatty acyl-L-carnitine"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:133449',
                          'name': 'hydroxy-fatty acyl-L-carnitine',
                          'definition': 'An O-acylcarnitine in which the R '
                                        'group is a hydroxylated fatty acyl '
                                        'chain.',
                          'parents': ['CHEBI:176910', 'CHEBI:75659']},
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
    'error': "'Mol' object has no attribute "
             "'GetTopologicalFragmentAtomIndices'",
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