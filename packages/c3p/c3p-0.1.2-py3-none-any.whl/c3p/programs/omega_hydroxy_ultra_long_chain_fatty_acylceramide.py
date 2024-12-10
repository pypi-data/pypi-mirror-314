"""
Classifies: CHEBI:144784 omega-hydroxy-ultra-long chain fatty acylceramide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_omega_hydroxy_ultra_long_chain_fatty_acylceramide(smiles: str):
    """
    Determines if a molecule is an omega-hydroxy-ultra-long chain fatty acylceramide.

    An omega-hydroxy-ultra-long chain fatty acylceramide is defined as a ceramide with no defined sphingoid base
    and an N-omega-hydroxyacyl chain length greater than C27.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is an omega-hydroxy-ultra-long chain fatty acylceramide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains an amide group
    has_amide = any(atom.GetSymbol() == 'N' and atom.GetDegree() == 3 for atom in mol.GetAtoms())
    if not has_amide:
        return False, "Molecule does not contain an amide group"

    # Find the amide nitrogen and its neighbors
    amide_nitrogen = None
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N' and atom.GetDegree() == 3:
            amide_nitrogen = atom
            break

    if amide_nitrogen is None:
        return False, "Failed to find amide nitrogen"

    amide_carbonyl = None
    amide_chain = None
    for neighbor in amide_nitrogen.GetNeighbors():
        if neighbor.GetSymbol() == 'O':
            continue
        elif neighbor.GetSymbol() == 'C' and neighbor.GetDegree() == 2:
            amide_carbonyl = neighbor
        else:
            amide_chain = neighbor

    if amide_carbonyl is None or amide_chain is None:
        return False, "Failed to identify amide carbonyl or chain"

    # Check if the amide chain is an ultra-long fatty acid chain
    chain_length = AllChem.CalcPrimiAlChainLength(mol, amide_chain.GetIdx())
    if chain_length < 28:
        return False, f"Chain length ({chain_length}) is not greater than C27"

    # Check if the chain has an omega-hydroxy group
    terminal_atom = AllChem.FindMolTerminalAtoms(mol, amide_chain.GetIdx())[-1]
    if terminal_atom.GetSymbol() != 'O' or terminal_atom.GetDegree() != 1:
        return False, "Terminal atom is not a hydroxy group"

    return True, "The molecule is an omega-hydroxy-ultra-long chain fatty acylceramide"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:144784',
                          'name': 'omega-hydroxy-ultra-long chain fatty '
                                  'acylceramide',
                          'definition': 'A ceramide with no defined sphingoid '
                                        'base and an N-omega-hydroxyacyl chain '
                                        'length greater than C27',
                          'parents': ['CHEBI:17761', 'CHEBI:50860']},
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
    'error': "module 'rdkit.Chem.AllChem' has no attribute "
             "'CalcPrimiAlChainLength'",
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