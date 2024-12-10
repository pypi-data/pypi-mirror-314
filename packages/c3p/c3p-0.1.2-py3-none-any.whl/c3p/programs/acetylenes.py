"""
Classifies: CHEBI:33644 acetylenes
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_acetylenes(smiles: str):
    """
    Determines if a molecule is an acetylene (acyclic or cyclic hydrocarbon with one or more carbon-carbon triple bonds).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an acetylene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if molecule contains only C and H atoms
    atoms = [atom.GetSymbol() for atom in mol.GetAtoms()]
    if any(atom not in ['C', 'H'] for atom in atoms):
        return False, "Molecule contains atoms other than carbon and hydrogen"

    # Check for presence of at least one triple bond
    triple_bonds = sum(bond.GetBondType() == Chem.BondType.TRIPLE for bond in mol.GetBonds())
    if triple_bonds == 0:
        return False, "No carbon-carbon triple bonds found"

    # Check for cyclic or acyclic structure
    ring_info = mol.GetRingInfo()
    if ring_info.NumRings() > 0:
        return True, "Cyclic acetylene with side chain(s)" if len(atoms) > ring_info.NumRings() * 6 else "Cyclic acetylene"
    else:
        return True, "Acyclic (branched or unbranched) acetylene"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33644',
                          'name': 'acetylenes',
                          'definition': 'Acyclic (branched or unbranched) and '
                                        'cyclic (with or without side chain) '
                                        'hydrocarbons having one or more '
                                        'carbon-carbon triple bonds.',
                          'parents': ['CHEBI:24632', 'CHEBI:73474']},
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
    'num_true_positives': 2,
    'num_false_positives': 27,
    'num_true_negatives': 183882,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.06896551724137931,
    'recall': 1.0,
    'f1': 0.12903225806451613,
    'accuracy': 0.9998531898581379}