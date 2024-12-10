"""
Classifies: CHEBI:33235 tocotrienol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_tocotrienol(smiles: str):
    """
    Determines if a molecule is a tocotrienol.
    A tocotrienol is a tocol in which the hydrocarbon chain at position 2 contains three double bonds.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a tocotrienol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if molecule has a chroman ring system
    chroman_ring = mol.GetRingInfo().AtomRings()[0] if mol.GetRingInfo().AtomRings() else None
    if chroman_ring is None or len(chroman_ring) != 6:
        return False, "No chroman ring system found"

    # Find the chroman oxygen atom
    chroman_oxygen = [mol.GetAtomWithIdx(idx) for idx in chroman_ring if mol.GetAtomWithIdx(idx).GetSymbol() == 'O'][0]

    # Find the substituent at position 2
    substituent = [atom for atom in chroman_oxygen.GetNeighbors() if atom.GetIdx() not in chroman_ring][0]

    # Check if the substituent is an alkyl chain with three double bonds
    alkyl_chain = [substituent]
    current_atom = substituent
    double_bond_count = 0

    while current_atom.GetDegree() == 2:
        neighbors = [atom for atom in current_atom.GetNeighbors() if atom.GetIdx() != alkyl_chain[-1].GetIdx()]
        if len(neighbors) == 0:
            break
        alkyl_chain.append(neighbors[0])
        if neighbors[0].GetIsAromatic():
            return False, "Alkyl chain contains aromatic atoms"
        if sum(bond.GetBondType() == Chem.BondType.DOUBLE for bond in neighbors[0].GetBonds()) == 1:
            double_bond_count += 1
        current_atom = neighbors[0]

    if double_bond_count == 3:
        return True, "Molecule is a tocotrienol"
    else:
        return False, "Alkyl chain does not contain three double bonds"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33235',
                          'name': 'tocotrienol',
                          'definition': 'A tocol in which the hydrocarbon '
                                        'chain at position 2 contains three '
                                        'double bonds.',
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
    'success': False,
    'best': True,
    'error': 'list index out of range',
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