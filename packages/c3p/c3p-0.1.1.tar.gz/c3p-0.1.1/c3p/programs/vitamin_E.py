"""
Classifies: CHEBI:33234 vitamin E
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_vitamin_E(smiles: str):
    """
    Determines if a molecule is a member of the vitamin E class.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a vitamin E, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a chroman-6-ol core
    chroman_ring = Chem.MolFromSmiles('O1c2ccccc2CC1')
    if not mol.HasSubstructMatch(chroman_ring):
        return False, "No chroman-6-ol core found"

    # Check for the presence of a methyl group at position 2 of the chroman-6-ol core
    methyl_group = Chem.MolFromSmiles('C')
    atom_idx = mol.GetSubstructMatch(chroman_ring)[0]
    if not any(mol.GetAtomWithIdx(atom_idx).HasBondToAtom(mol.GetAtomWithIdx(neighbor.GetIdx())) and neighbor.IsInRing() and neighbor.GetIsAromatic() and neighbor.GetTotalNumHs() == 1 for neighbor in mol.GetAtomWithIdx(atom_idx).GetNeighbors()):
        return False, "No methyl group found at position 2 of the chroman-6-ol core"

    # Check for the presence of a saturated or triply-unsaturated hydrocarbon chain at position 2 of the chroman-6-ol core
    hydrocarbon_chain = Chem.MolFromSmiles('CCC(C)CCC=CCC=CCC=C')
    if not mol.HasSubstructMatch(hydrocarbon_chain):
        return False, "No saturated or triply-unsaturated hydrocarbon chain found at position 2 of the chroman-6-ol core"

    return True, "Molecule is a member of the vitamin E class"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33234',
                          'name': 'vitamin E',
                          'definition': 'Any member of a group of fat-soluble '
                                        'chromanols  that exhibit biological '
                                        'activity against vitamin E '
                                        'deficiency. The vitamers in this '
                                        'class consists of a chroman-6-ol core '
                                        'which is substituted at position 2 by '
                                        'a methyl group and (also at position '
                                        '2) either a saturated or a '
                                        'triply-unsaturated hydrocarbon chain '
                                        'consisting of three isoprenoid units. '
                                        'The major function of vitamin E is to '
                                        'act as a natural antioxidant by '
                                        'scavenging free radicals and '
                                        'molecular oxygen.',
                          'parents': ['CHEBI:23229']},
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
    'error': "'Atom' object has no attribute 'HasBondToAtom'",
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