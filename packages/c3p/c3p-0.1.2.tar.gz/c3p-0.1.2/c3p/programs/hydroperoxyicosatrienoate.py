"""
Classifies: CHEBI:131875 hydroperoxyicosatrienoate
"""
from rdkit import Chem

def is_hydroperoxyicosatrienoate(smiles: str):
    """
    Determines if a molecule is a hydroperoxyicosatrienoate anion.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a hydroperoxyicosatrienoate anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for a carboxylate anion group
    carboxylate_present = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == -1:
            neighbors = [mol.GetAtomWithIdx(n.GetIdx()).GetSymbol() for n in atom.GetNeighbors()]
            if 'C' in neighbors:
                carboxylate_present = True
                break

    if not carboxylate_present:
        return False, "No carboxylate anion group found"

    # Check for a hydroperoxy group
    hydroperoxy_present = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetTotalNumHs() == 1:
            neighbors = [mol.GetAtomWithIdx(n.GetIdx()).GetSymbol() for n in atom.GetNeighbors()]
            if 'O' in neighbors:
                hydroperoxy_present = True
                break

    if not hydroperoxy_present:
        return False, "No hydroperoxy group found"

    # Check for an icosanoid chain (20 carbon atoms)
    carbon_count = sum(atom.GetSymbol() == 'C' for atom in mol.GetAtoms())
    if carbon_count != 20:
        return False, "Molecule does not contain 20 carbon atoms"

    # Check for at least three double bonds
    double_bond_count = sum(bond.GetBondType() == Chem.BondType.DOUBLE for bond in mol.GetBonds())
    if double_bond_count < 3:
        return False, "Molecule does not contain at least three double bonds"

    return True, "Molecule is a hydroperoxyicosatrienoate anion"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131875',
                          'name': 'hydroperoxyicosatrienoate',
                          'definition': 'An icosanoid anion arising from '
                                        'deprotonation of the carboxylic acid '
                                        'function of any '
                                        'hydroperoxyicosatrienoic acid.',
                          'parents': [   'CHEBI:134019',
                                         'CHEBI:57560',
                                         'CHEBI:62937']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: Python argument types in\n'
               '    Mol.GetAtomWithIdx(Mol, Atom)\n'
               'did not match C++ signature:\n'
               '    GetAtomWithIdx(RDKit::ROMol {lvalue} self, unsigned int '
               'idx)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 41,
    'num_true_negatives': 183882,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.023809523809523808,
    'recall': 1.0,
    'f1': 0.046511627906976744,
    'accuracy': 0.9997770818381505}