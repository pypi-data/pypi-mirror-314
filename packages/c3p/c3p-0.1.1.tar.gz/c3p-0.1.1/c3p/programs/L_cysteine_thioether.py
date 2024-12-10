"""
Classifies: CHEBI:27532 L-cysteine thioether
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_L_cysteine_thioether(smiles: str):
    """
    Determines if a molecule is an L-cysteine thioether.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an L-cysteine thioether, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of sulfur atom(s)
    if not any(atom.GetSymbol() == 'S' for atom in mol.GetAtoms()):
        return False, "No sulfur atom found"

    # Check for the presence of carboxyl group (-COOH)
    has_carboxyl = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            neighbors = [mol.GetAtomWithIdx(n).GetSymbol() for n in atom.GetNeighbors()]
            if 'O' in neighbors and 'O' in neighbors:
                has_carboxyl = True
                break

    if not has_carboxyl:
        return False, "No carboxyl group found"

    # Check for the presence of amino group (-NH2)
    has_amino = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N':
            neighbors = [mol.GetAtomWithIdx(n).GetSymbol() for n in atom.GetNeighbors()]
            if 'H' in neighbors and 'H' in neighbors:
                has_amino = True
                break

    if not has_amino:
        return False, "No amino group found"

    # Check if the sulfur atom is bonded to an aromatic ring or an aliphatic chain
    is_thioether = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'S':
            neighbors = [mol.GetAtomWithIdx(n) for n in atom.GetNeighbors()]
            for neighbor in neighbors:
                if neighbor.GetIsAromatic():
                    is_thioether = True
                    break
                elif neighbor.GetHybridization() == Chem.HybridizationType.SP3:
                    is_thioether = True
                    break

    if is_thioether:
        return True, "L-cysteine thioether"
    else:
        return False, "Not an L-cysteine thioether"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27532',
                          'name': 'L-cysteine thioether',
                          'definition': 'Any L-cysteine derivative obtained by '
                                        'conversion of the thiol group into a '
                                        'sulfide.',
                          'parents': ['CHEBI:16385', 'CHEBI:47910']},
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