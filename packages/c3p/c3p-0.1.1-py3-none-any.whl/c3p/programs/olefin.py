"""
Classifies: CHEBI:33641 olefin
"""
from rdkit import Chem
from rdkit.Chem import rdchem

def is_olefin(smiles: str):
    """
    Determines if a molecule is an olefin (acyclic or cyclic hydrocarbons with one or more carbon-carbon double bonds, excluding aromatic compounds).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is an olefin, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains only carbon and hydrogen atoms
    allowed_atoms = {'C', 'H'}
    if any(atom.GetSymbol() not in allowed_atoms for atom in mol.GetAtoms()):
        return False, "Molecule contains atoms other than carbon and hydrogen"

    # Check if the molecule contains any aromatic rings
    aromatic_rings = [ring for ring in mol.GetRingInfo().AtomRings() if all(mol.GetAtomWithIdx(idx).GetIsAromatic() for idx in ring)]
    if aromatic_rings:
        return False, "Molecule contains aromatic rings"

    # Check if the molecule contains any carbon-carbon double bonds
    double_bonds = [bond for bond in mol.GetBonds() if bond.GetBondType() == Chem.BondType.DOUBLE]
    if not double_bonds:
        return False, "Molecule does not contain any carbon-carbon double bonds"

    # Check if the double bonds are between carbon atoms
    for bond in double_bonds:
        atom1 = mol.GetAtomWithIdx(bond.GetBeginAtomIdx())
        atom2 = mol.GetAtomWithIdx(bond.GetEndAtomIdx())
        if atom1.GetSymbol() != 'C' or atom2.GetSymbol() != 'C':
            return False, "Double bond not between carbon atoms"

    return True, "Molecule is an olefin"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33641',
                          'name': 'olefin',
                          'definition': 'Acyclic and cyclic hydrocarbons '
                                        'having one or more carbon-carbon '
                                        'double bonds, apart from the formal '
                                        'ones in aromatic compounds. The class '
                                        'olefins subsumes alkenes and '
                                        'cycloalkenes and the corresponding '
                                        'polyenes.',
                          'parents': ['CHEBI:24632', 'CHEBI:78840']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: 'Mol' object has no attribute "
               "'GetAromaticRings'",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 30,
    'num_false_positives': 100,
    'num_true_negatives': 35489,
    'num_false_negatives': 8,
    'num_negatives': None,
    'precision': 0.23076923076923078,
    'recall': 0.7894736842105263,
    'f1': 0.35714285714285715,
    'accuracy': 0.9969685912369832}