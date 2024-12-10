"""
Classifies: CHEBI:21752 N-methyl-L-alpha-amino acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_N_methyl_L_alpha_amino_acid(smiles: str):
    """
    Determines if a molecule is an N-methyl-L-alpha-amino acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an N-methyl-L-alpha-amino acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for L-configuration
    if not AllChem.GetMolStereoFlag(mol):
        return False, "Molecule does not contain stereochemistry information"

    chiral_centers = Chem.FindMolChiralUnspecifiedUnbrackedAtoms(mol)
    if len(chiral_centers) == 0:
        return False, "No chiral centers found"

    chiral_atom_idx = chiral_centers[0]
    chiral_atom = mol.GetAtomWithIdx(chiral_atom_idx)

    if chiral_atom.GetHybridization() != Chem.HybridizationType.SP3:
        return False, "Chiral center is not sp3 hybridized"

    neighbors = chiral_atom.GetNeighbors()
    if len(neighbors) != 3:
        return False, "Chiral center does not have 3 neighbors"

    # Check for amino acid backbone
    carboxyl_found = False
    amino_found = False
    for neighbor in neighbors:
        if neighbor.GetSymbol() == 'O' and neighbor.GetDegree() == 1:
            carboxyl_found = True
        elif neighbor.GetSymbol() == 'N':
            amino_found = True

    if not carboxyl_found or not amino_found:
        return False, "Amino acid backbone not found"

    # Check for N-methylation
    if amino_found:
        amino_atom = neighbors[neighbors.index(mol.GetAtomWithIdx(chiral_atom_idx))]
        methyl_groups = 0
        for methyl_neighbor in amino_atom.GetNeighbors():
            if methyl_neighbor.GetSymbol() == 'C' and methyl_neighbor.GetDegree() == 4:
                methyl_groups += 1

        if methyl_groups == 0:
            return False, "Amino group is not N-methylated"
        elif methyl_groups > 1:
            return True, f"N-{methyl_groups}-methyl-L-alpha-amino acid"
        else:
            return True, "N-methyl-L-alpha-amino acid"

    return False, "Molecule is not an N-methyl-L-alpha-amino acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:21752',
                          'name': 'N-methyl-L-alpha-amino acid',
                          'definition': 'An non-proteinogenic L-alpha-amino '
                                        'acid in which the amino group bears '
                                        'one or more methyl groups.',
                          'parents': ['CHEBI:21760', 'CHEBI:83822']},
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
    'success': False,
    'best': True,
    'error': "module 'rdkit.Chem.AllChem' has no attribute 'GetMolStereoFlag'",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}