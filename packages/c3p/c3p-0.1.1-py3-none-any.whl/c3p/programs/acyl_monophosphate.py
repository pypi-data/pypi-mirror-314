"""
Classifies: CHEBI:16826 acyl monophosphate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_acyl_monophosphate(smiles: str):
    """
    Determines if a molecule is an acyl monophosphate, defined as an organic phosphate
    ester or anhydride formed by condensation of phosphoric acid with a carboxylic acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an acyl monophosphate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a phosphate group
    phosphate_atoms = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == 'P']
    if not phosphate_atoms:
        return False, "No phosphorus atom found"

    # Check for the presence of a carbonyl group
    carbonyl_atoms = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == 'C' and sum(mol.GetAtomWithIdx(atom).GetTotalNumHs() for atom in mol.GetAtomWithIdx(atom).GetNeighbors()) == 0]
    if not carbonyl_atoms:
        return False, "No carbonyl group found"

    # Check if the phosphate group is connected to the carbonyl group
    for p_idx in phosphate_atoms:
        p_atom = mol.GetAtomWithIdx(p_idx)
        for neighbor in p_atom.GetNeighbors():
            if neighbor.GetIdx() in carbonyl_atoms:
                return True, "Molecule is an acyl monophosphate"

    return False, "Molecule does not meet the criteria for an acyl monophosphate"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16826',
                          'name': 'acyl monophosphate',
                          'definition': 'An organic phosphate ester or '
                                        'anhydride formed by condensation of '
                                        'phosphoric acid with a carboxylic '
                                        'acid.',
                          'parents': ['CHEBI:25703', 'CHEBI:37787']},
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