"""
Classifies: CHEBI:22918 branched-chain amino acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_branched_chain_amino_acid(smiles: str):
    """
    Determines if a molecule is a branched-chain amino acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a branched-chain amino acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains the amino acid functional group
    has_amino_acid_group = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N':
            neighbors = [mol.GetAtomWithIdx(n).GetSymbol() for n in atom.GetNeighbors()]
            if 'C' in neighbors and 'H' in neighbors:
                has_amino_acid_group = True
                break

    if not has_amino_acid_group:
        return False, "Molecule does not contain an amino acid functional group"

    # Check if the carbon chain is branched
    is_branched = False
    for bond in mol.GetBonds():
        atom1 = mol.GetAtomWithIdx(bond.GetBeginAtomIdx())
        atom2 = mol.GetAtomWithIdx(bond.GetEndAtomIdx())
        if atom1.GetSymbol() == 'C' and atom2.GetSymbol() == 'C':
            if sum(1 for n in atom1.GetNeighbors() if mol.GetAtomWithIdx(n).GetSymbol() == 'C') > 2:
                is_branched = True
                break
            if sum(1 for n in atom2.GetNeighbors() if mol.GetAtomWithIdx(n).GetSymbol() == 'C') > 2:
                is_branched = True
                break

    if is_branched:
        return True, "Molecule is a branched-chain amino acid"
    else:
        return False, "Molecule is not a branched-chain amino acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22918',
                          'name': 'branched-chain amino acid',
                          'definition': 'Any  amino acid  in which the parent '
                                        'hydrocarbon chain has one or more '
                                        'alkyl substituents',
                          'parents': ['CHEBI:33709']},
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
    'recall': 0,
    'f1': 0,
    'accuracy': None}