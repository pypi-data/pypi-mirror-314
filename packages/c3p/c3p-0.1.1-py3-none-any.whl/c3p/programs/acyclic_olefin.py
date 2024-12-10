"""
Classifies: CHEBI:33645 acyclic olefin
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_acyclic_olefin(smiles: str):
    """
    Determines if a molecule is an acyclic olefin.
    Acyclic branched or unbranched hydrocarbons having one or more carbon-carbon double bond.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an acyclic olefin, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if molecule has only C and H atoms
    if not all(atom.GetSymbol() in ['C', 'H'] for atom in mol.GetAtoms()):
        return False, "Molecule contains non-hydrocarbon atoms"

    # Check if molecule has at least one double bond
    if not any(bond.GetBondType() == Chem.BondType.DOUBLE for bond in mol.GetBonds()):
        return False, "Molecule does not contain any double bonds"

    # Check if molecule is acyclic
    if mol.GetRingInfo().NumRings() > 0:
        return False, "Molecule is cyclic"

    # Check if molecule has at least one carbon-carbon double bond
    has_cc_double_bond = False
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.DOUBLE:
            atom1 = mol.GetAtomWithIdx(bond.GetBeginAtomIdx())
            atom2 = mol.GetAtomWithIdx(bond.GetEndAtomIdx())
            if atom1.GetSymbol() == 'C' and atom2.GetSymbol() == 'C':
                has_cc_double_bond = True
                break

    if not has_cc_double_bond:
        return False, "Molecule does not contain any carbon-carbon double bonds"

    return True, "Molecule is an acyclic olefin"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33645',
                          'name': 'acyclic olefin',
                          'definition': 'Acyclic branched or unbranched '
                                        'hydrocarbons having one or more '
                                        'carbon-carbon double bond.',
                          'parents': ['CHEBI:33641']},
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
    'num_true_positives': 14,
    'num_false_positives': 100,
    'num_true_negatives': 133574,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.12280701754385964,
    'recall': 1.0,
    'f1': 0.21875,
    'accuracy': 0.9992519897073784}