"""
Classifies: CHEBI:16232 N(6)-acyl-L-lysine
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_N_6__acyl_L_lysine(smiles: str):
    """
    Determines if a molecule is an N(6)-acyl-L-lysine, defined as any N-acyl-L-alpha-amino acid
    that is L-lysine in which the N(6) amino group has been acylated.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an N(6)-acyl-L-lysine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a lysine residue
    lysine_pattern = Chem.MolFromSmarts('[N;H2][C;H2;@][C;H;@][C;H2][C;H2][C;H2][C;H][C;H3](=[O])[N;H3]')
    if not mol.HasSubstructMatch(lysine_pattern):
        return False, "Molecule does not contain a lysine residue"

    # Check for the acylation of the N(6) amino group
    n6_acyl_pattern = Chem.MolFromSmarts('[N;H2][C;H2;@][C;H;@][C;H2][C;H2][C;H2][C;H][C;H3](=[O])[N;H][C;H]')
    if not mol.HasSubstructMatch(n6_acyl_pattern):
        return False, "N(6) amino group is not acylated"

    # Check for the stereochemistry of the alpha-carbon
    chiral_centers = Chem.FindMolChiralCenters(mol, includeUnspec=True)
    if len(chiral_centers) != 1:
        return False, "Incorrect number of chiral centers"

    chiral_center = chiral_centers[0]
    if mol.GetAtomWithIdx(chiral_center).GetChiralTag() != Chem.ChiralType.CHI_TETRAHEDRAL_CCW:
        return False, "Incorrect stereochemistry at the alpha-carbon"

    return True, "Molecule is an N(6)-acyl-L-lysine"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16232',
                          'name': 'N(6)-acyl-L-lysine',
                          'definition': 'Any N-acyl-L-alpha-amino acid that is '
                                        'L-lysine in which the N(6) amino '
                                        'group has been acylated.',
                          'parents': ['CHEBI:25095', 'CHEBI:48927']},
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
    'num_true_negatives': 183924,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945630012234}