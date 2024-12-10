"""
Classifies: CHEBI:26177 polyene antibiotic
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_polyene_antibiotic(smiles: str):
    """
    Determines if a molecule is a polyene antibiotic.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a polyene antibiotic, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a conjugated polyene system
    conjugated_double_bonds = []
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.DOUBLE:
            begin_atom = mol.GetAtomWithIdx(bond.GetBeginAtomIdx())
            end_atom = mol.GetAtomWithIdx(bond.GetEndAtomIdx())
            if begin_atom.GetIsAromatic() or end_atom.GetIsAromatic():
                continue  # Skip aromatic bonds
            begin_double_bond_neighbors = [neighbor for neighbor in begin_atom.GetNeighbors() if neighbor.GetBondTypeWithAtom(begin_atom.GetIdx()) == Chem.BondType.DOUBLE]
            end_double_bond_neighbors = [neighbor for neighbor in end_atom.GetNeighbors() if neighbor.GetBondTypeWithAtom(end_atom.GetIdx()) == Chem.BondType.DOUBLE]
            if len(begin_double_bond_neighbors) > 1 or len(end_double_bond_neighbors) > 1:
                conjugated_double_bonds.append(bond)

    if len(conjugated_double_bonds) < 3:
        return False, "Not enough conjugated double bonds to form a polyene system"

    # Check for the presence of a lactone or lactam ring
    lactone_lactam_rings = [ring for ring in mol.GetRingInfo().AtomRings() if any(mol.GetAtomWithIdx(idx).GetSymbol() in ['O', 'N'] for idx in ring)]
    if not lactone_lactam_rings:
        return False, "No lactone or lactam ring found"

    # Check for the presence of a sugar moiety (optional)
    sugar_rings = [ring for ring in mol.GetRingInfo().AtomRings() if all(mol.GetAtomWithIdx(idx).GetSymbol() == 'O' for idx in ring)]
    if sugar_rings:
        return True, "Polyene antibiotic with a sugar moiety"

    return True, "Polyene antibiotic without a sugar moiety"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26177',
                          'name': 'polyene antibiotic',
                          'definition': 'A family of antibiotics containing a '
                                        'conjugated polyene moiety, usuallly '
                                        'isolated from some species of '
                                        'Streptomyces.',
                          'parents': ['CHEBI:33822']},
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
    'error': "'Atom' object has no attribute 'GetBondTypeWithAtom'",
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