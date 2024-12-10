"""
Classifies: CHEBI:137967 N(6)-acyl-L-lysine residue
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_N_6__acyl_L_lysine_residue(smiles: str):
    """
    Determines if a molecule is an N(6)-acyl-L-lysine residue, defined as an L-alpha-amino acid residue derived from any N(6)-acyl-L-lysine.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an N(6)-acyl-L-lysine residue, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a lysine residue
    lysine_pattern = Chem.MolFromSmarts('C(C(=O)N)CCC[NH3+]')
    if not mol.HasSubstructMatch(lysine_pattern):
        return False, "Not a lysine residue"

    # Check for acylation at the N(6) position
    acyl_pattern = Chem.MolFromSmarts('C(=O)NCC(C(=O)N)CCC[NH3+]')
    if not mol.HasSubstructMatch(acyl_pattern):
        return False, "Not acylated at the N(6) position"

    # Check for L-configuration at the alpha carbon
    alpha_carbon = None
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetDegree() == 3:
            neighbors = [mol.GetAtomWithIdx(n) for n in atom.GetNeighbors()]
            if len([n for n in neighbors if n.GetSymbol() == 'N']) == 1 and len([n for n in neighbors if n.GetSymbol() == 'O']) == 1:
                alpha_carbon = atom
                break

    if alpha_carbon is None:
        return False, "Unable to identify alpha carbon"

    if alpha_carbon.GetChiralTag() != Chem.ChiralType.CHI_TETRAHEDRAL_CCW:
        return False, "Not L-configuration at alpha carbon"

    return True, "Molecule is an N(6)-acyl-L-lysine residue"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:137967',
                          'name': 'N(6)-acyl-L-lysine residue',
                          'definition': 'An L-alpha-amino acid residue derived '
                                        'from any N(6)-acyl-L-lysine.',
                          'parents': ['CHEBI:83228']},
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
    'num_true_negatives': 183918,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945628238518}