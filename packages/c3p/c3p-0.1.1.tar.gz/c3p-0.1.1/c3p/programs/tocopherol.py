"""
Classifies: CHEBI:27013 tocopherol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_tocopherol(smiles: str):
    """
    Determines if a molecule is a tocopherol or tocotrienol.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a tocopherol or tocotrienol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the chroman-6-ol nucleus
    match = mol.GetSubstructMatches(Chem.MolFromSmarts('c1c(O)c2OCCc2cc1'))
    if not match:
        return False, "Chroman-6-ol nucleus not found"

    # Check for methyl group at position 2
    chroman_ring = mol.GetAtomWithIdx(match[0][1])
    if chroman_ring.GetNumExplicitHs() != 1:
        return False, "No methyl group at position 2"

    # Check for saturated hydrocarbon chain with three isoprenoid units
    chain_atoms = [a for a in mol.GetAtoms() if a.GetIdx() not in match[0]]
    chain_length = sum(1 for a in chain_atoms if a.GetHybridization() == Chem.HybridizationType.SP3)
    if chain_length != 16:
        return False, "Hydrocarbon chain does not have 16 carbon atoms"

    double_bonds = sum(1 for a in chain_atoms if a.GetHybridization() == Chem.HybridizationType.SP2)
    if double_bonds == 0:
        return True, "Tocopherol"
    elif double_bonds == 3:
        return True, "Tocotrienol"
    else:
        return False, "Hydrocarbon chain does not match tocopherol or tocotrienol"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27013',
                          'name': 'tocopherol',
                          'definition': 'A collective name for a group of '
                                        'closely related lipids that contain a '
                                        'chroman-6-ol nucleus substituted at '
                                        'position 2 by a methyl group and by a '
                                        'saturated hydrocarbon chain '
                                        'consisting of three isoprenoid units. '
                                        'They are designated as alpha-, beta-, '
                                        'gamma-, and delta-tocopherol '
                                        'depending on the number and position '
                                        'of additional methyl substituents on '
                                        'the aromatic ring. Tocopherols occur '
                                        'in vegetable oils and vegetable oil '
                                        'products, almost exclusively with '
                                        'R,R,R configuration. Tocotrienols '
                                        'differ from tocopherols only in '
                                        'having three double bonds in the '
                                        'hydrocarbon chain.',
                          'parents': ['CHEBI:39437']},
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
    'num_true_negatives': 183918,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999945628238518}