"""
Classifies: CHEBI:197480 icosanol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_icosanol(smiles: str):
    """
    Determines if a molecule is an icosanol (a fatty alcohol consisting of a hydroxy function at any position
    of an unbranched saturated chain of twenty carbon atoms).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an icosanol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count the number of atoms
    num_atoms = mol.GetNumAtoms()
    if num_atoms != 21:
        return False, "Molecule does not have 21 atoms"

    # Count the number of carbon and oxygen atoms
    num_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    num_oxygens = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')
    if num_carbons != 20 or num_oxygens != 1:
        return False, "Molecule does not have 20 carbon atoms and 1 oxygen atom"

    # Check for exactly one hydroxyl group
    num_hydroxyls = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and atom.GetTotalNumHs() == 1)
    if num_hydroxyls != 1:
        return False, "Molecule does not have exactly one hydroxyl group"

    # Check for an unbranched carbon chain
    carbon_chain = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == 'C']
    if len(carbon_chain) != 20:
        return False, "Molecule does not have an unbranched carbon chain of length 20"

    # Check for saturation and contiguous carbon chain
    chain_is_contiguous = True
    for i in range(len(carbon_chain) - 1):
        atom1 = mol.GetAtomWithIdx(carbon_chain[i])
        atom2 = mol.GetAtomWithIdx(carbon_chain[i + 1])
        if not mol.GetBondBetweenAtoms(atom1.GetIdx(), atom2.GetIdx()):
            chain_is_contiguous = False
            break

        bond = mol.GetBondBetweenAtoms(atom1.GetIdx(), atom2.GetIdx())
        if bond.GetBondType() != Chem.BondType.SINGLE:
            return False, "Molecule contains unsaturated bonds"

    if not chain_is_contiguous:
        return False, "Molecule does not have a contiguous unbranched carbon chain"

    return True, "Molecule is an icosanol"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:197480',
                          'name': 'icosanol',
                          'definition': 'A fatty alcohol consisting of a '
                                        'hydroxy function at any position of '
                                        'an unbranched saturated chain of '
                                        'twenty carbon atoms.',
                          'parents': [   'CHEBI:134179',
                                         'CHEBI:50584',
                                         'CHEBI:78139']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.6666666666666666 is too low.\n'
               "True positives: [('CCCCCCCCCCCCCCCC(O)CCCC', 'Molecule is an "
               "icosanol')]\n"
               "False positives: [('CC(C)CCCCCCCCCCCCCCCCCO', 'Molecule is an "
               "icosanol')]\n"
               'False negatives: []',
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 0,
    'num_true_negatives': 183925,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 1.0,
    'recall': 1.0,
    'f1': 1.0,
    'accuracy': 1.0}