"""
Classifies: CHEBI:15778 N-acyl-D-amino acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_N_acyl_D_amino_acid(smiles: str):
    """
    Determines if a molecule is an N-acyl-D-amino acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an N-acyl-D-amino acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find amide N atom
    amide_N = None
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N' and atom.GetTotalNumHs() == 1:
            amide_N = atom
            break

    if amide_N is None:
        return False, "No amide N atom found"

    # Find carbonyl C atom
    carbonyl_C = None
    for neighbor in amide_N.GetNeighbors():
        if neighbor.GetSymbol() == 'C' and neighbor.GetTotalNumHs() == 0:
            carbonyl_C = neighbor
            break

    if carbonyl_C is None:
        return False, "No carbonyl C atom found"

    # Check for acyl group
    acyl_atoms = [carbonyl_C]
    for neighbor in carbonyl_C.GetNeighbors():
        if neighbor.GetIdx() != amide_N.GetIdx():
            acyl_atoms.append(neighbor)

    # Check for amino acid
    amino_acid_atoms = [amide_N]
    for neighbor in amide_N.GetNeighbors():
        if neighbor.GetIdx() != carbonyl_C.GetIdx():
            amino_acid_atoms.append(neighbor)

    # Check for D configuration
    chiral_centers = Chem.FindMolChiralCenters(mol, includeUnspec=True)
    is_d_config = False
    for chiral_center in chiral_centers:
        if chiral_center[0] in amino_acid_atoms:
            if chiral_center[2] == 'D':
                is_d_config = True
                break

    if not is_d_config:
        return False, "Amino acid is not in D configuration"

    return True, "Molecule is an N-acyl-D-amino acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:15778',
                          'name': 'N-acyl-D-amino acid',
                          'definition': 'Any N-acyl-amino acid in which the '
                                        'amino acid moiety has D '
                                        'configuration.',
                          'parents': ['CHEBI:51569', 'CHEBI:83812']},
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
    'error': 'FindMolChiralCenters() got an unexpected keyword argument '
             "'includeUnspec'",
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