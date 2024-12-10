"""
Classifies: CHEBI:131879 cholanic acid conjugate anion
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_cholanic_acid_conjugate_anion(smiles: str):
    """
    Determines if a molecule is a cholanic acid conjugate anion.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a cholanic acid conjugate anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if molecule contains a carboxylate group
    carboxylate_found = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == -1:
            neighbors = [mol.GetAtomWithIdx(neighbor).GetSymbol() for neighbor in atom.GetNeighbors()]
            if 'C' in neighbors:
                carboxylate_found = True
                break

    if not carboxylate_found:
        return False, "No carboxylate group found"

    # Check if molecule contains a steroid scaffold
    ring_info = mol.GetRingInfo()
    steroid_scaffold = False
    for ring in ring_info.AtomRings():
        if len(ring) == 17:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetSymbol() == 'C' for atom in atoms):
                steroid_scaffold = True
                break

    if not steroid_scaffold:
        return False, "No steroid scaffold found"

    # Check for conjugation
    conjugated = False
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.SINGLE:
            atom1 = mol.GetAtomWithIdx(bond.GetBeginAtomIdx())
            atom2 = mol.GetAtomWithIdx(bond.GetEndAtomIdx())
            if atom1.GetSymbol() == 'N' and atom2.GetSymbol() == 'C':
                conjugated = True
                break

    if conjugated:
        return True, "Cholanic acid conjugate anion"
    else:
        return False, "Not a conjugated cholanic acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131879',
                          'name': 'cholanic acid conjugate anion',
                          'definition': 'An organic anion obtained by '
                                        'deprotonation of any cholanic acid '
                                        'conjugate.',
                          'parents': ['CHEBI:25696']},
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
    'error': 'Python argument types in\n'
             '    Mol.GetAtomWithIdx(Mol, Atom)\n'
             'did not match C++ signature:\n'
             '    GetAtomWithIdx(RDKit::ROMol {lvalue} self, unsigned int idx)',
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