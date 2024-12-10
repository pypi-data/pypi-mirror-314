"""
Classifies: CHEBI:139572 hexadecenoyl-CoA(4-)
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_hexadecenoyl_CoA_4__(smiles: str):
    """
    Determines if a molecule is a hexadecenoyl-CoA(4-), a long-chain fatty acyl-CoA in which the S-acyl moiety contains 16 carbons and 1 double bond.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hexadecenoyl-CoA(4-), False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains a CoA moiety
    CoA_substructure = Chem.MolFromSmarts('C(C(=O)NCCC(=O)NCCS)')
    if not mol.HasSubstructMatch(CoA_substructure):
        return False, "Molecule does not contain a CoA moiety"

    # Check if the molecule has an acyl chain with 16 carbons
    acyl_chain_length = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C' and atom.GetIsAromatic() is False)
    if acyl_chain_length != 16:
        return False, f"Acyl chain length is {acyl_chain_length}, not 16"

    # Check if the acyl chain has exactly one double bond
    num_double_bonds = Descriptors.NumHeteroCycles(mol)
    if num_double_bonds != 1:
        return False, f"Number of double bonds is {num_double_bonds}, not 1"

    # Check if the acyl chain is saturated except for the double bond
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.DOUBLE and bond.GetIsConjugated():
            continue
        elif bond.GetBondType() == Chem.BondType.TRIPLE:
            return False, "Acyl chain contains a triple bond"

    return True, "Molecule is a hexadecenoyl-CoA(4-)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:139572',
                          'name': 'hexadecenoyl-CoA(4-)',
                          'definition': 'A long-chain fatty acyl-CoA in which '
                                        'the S-acyl moiety contains 16 carbons '
                                        'and 1 double bond. Major species at '
                                        'pH 7.3.',
                          'parents': ['CHEBI:77331', 'CHEBI:83139']},
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
    'error': "module 'rdkit.Chem.Descriptors' has no attribute "
             "'NumHeteroCycles'",
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