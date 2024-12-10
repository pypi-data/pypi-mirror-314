"""
Classifies: CHEBI:16197 N-acylsphingosine 1-phosphate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_N_acylsphingosine_1_phosphate(smiles: str):
    """
    Determines if a molecule is an N-acylsphingosine 1-phosphate.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an N-acylsphingosine 1-phosphate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has a phosphate group
    phosphate_present = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == "P" and atom.GetFormalCharge() == 0:
            phosphate_present = True
            break

    if not phosphate_present:
        return False, "No phosphate group found"

    # Check if the phosphate group is in the 1-position
    phosphate_atom = [a for a in mol.GetAtoms() if a.GetSymbol() == "P"][0]
    phosphate_idx = phosphate_atom.GetIdx()

    neighbors = [mol.GetAtomWithIdx(n) for n in phosphate_atom.GetNeighbors()]
    if len(neighbors) != 4:
        return False, "Phosphate group is not in the 1-position"

    carbon_neighbor = [n for n in neighbors if n.GetSymbol() == "C"][0]
    carbon_idx = carbon_neighbor.GetIdx()

    if len(carbon_neighbor.GetNeighbors()) != 4:
        return False, "Phosphate group is not in the 1-position"

    # Check if the nitrogen atom is acylated
    nitrogen_atom = [a for a in mol.GetAtoms() if a.GetSymbol() == "N"][0]
    nitrogen_idx = nitrogen_atom.GetIdx()

    acyl_group_present = False
    for neighbor in nitrogen_atom.GetNeighbors():
        neighbor_atom = mol.GetAtomWithIdx(neighbor)
        if neighbor_atom.GetSymbol() == "C" and neighbor_atom.GetDegree() == 3:
            acyl_group_present = True
            break

    if not acyl_group_present:
        return False, "No acyl group attached to the nitrogen atom"

    return True, "The molecule is an N-acylsphingosine 1-phosphate"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16197',
                          'name': 'N-acylsphingosine 1-phosphate',
                          'definition': 'A ceramide phosphate compound having '
                                        'the phosphate group in the 1-position '
                                        'and an unspecified acyl group atached '
                                        'to the nitrogen atom.',
                          'parents': ['CHEBI:13956']},
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