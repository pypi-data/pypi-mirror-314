"""
Classifies: CHEBI:29017 1-acyl-sn-glycero-3-phosphoethanolamine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_1_acyl_sn_glycero_3_phosphoethanolamine(smiles: str):
    """
    Determines if a molecule is a 1-acyl-sn-glycero-3-phosphoethanolamine (a 1-O-acylglycerophosphoethanolamine having (R)-configuration).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 1-acyl-sn-glycero-3-phosphoethanolamine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of required substructures
    substructure_patterns = [
        '[R7]C(O)COP(OCCN)(O)=O',  # Glycerophosphoethanolamine moiety
        '[R8]OC(=O)'  # Acyl group
    ]

    matched_substructures = []
    for pattern in substructure_patterns:
        patt = Chem.MolFromSmarts(pattern)
        matches = mol.GetSubstructMatches(patt)
        if matches:
            matched_substructures.append(pattern)

    if len(matched_substructures) != len(substructure_patterns):
        return False, "Missing required substructures"

    # Check for (R)-configuration at the glycerol moiety
    chiral_centers = Chem.FindMolChiralUnspecifiedUnbrackedAtoms(mol, includeUnspecified=True)
    if not chiral_centers:
        return False, "No chiral centers found"

    # Determine the stereochemistry of the chiral center
    chiral_center_idx = chiral_centers[0]
    chiral_center = mol.GetAtomWithIdx(chiral_center_idx)
    if chiral_center.GetChiralTag() != Chem.ChiralType.CHI_TETRAHEDRAL_CCW:
        return False, "Incorrect stereochemistry at the chiral center"

    return True, "Molecule is a 1-acyl-sn-glycero-3-phosphoethanolamine"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:29017',
                          'name': '1-acyl-sn-glycero-3-phosphoethanolamine',
                          'definition': 'A 1-O-acylglycerophosphoethanolamine '
                                        'having (R)-configuration.',
                          'parents': ['CHEBI:55493']},
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
    'num_true_negatives': 183902,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999836872298198}