"""
Classifies: CHEBI:25848 pantothenic acids
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_pantothenic_acids(smiles: str):
    """
    Determines if a molecule is a pantothenic acid, which is defined as a class of amides formed from pantoic acid and beta-alanine and its derivatives.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a pantothenic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find pantoic acid and beta-alanine substructures
    pantoic_acid_smarts = "[#6](-[#8])(-[#6])(-[#6])(-[#6](-[#6])=[#8])" # Pantoic acid substructure
    beta_alanine_smarts = "[#6](-[#6])(-[#6])(-[#8]-[#6](-[#6])=[#8])" # Beta-alanine substructure

    pantoic_acid_match = mol.GetSubstructMatches(Chem.MolFromSmarts(pantoic_acid_smarts))
    beta_alanine_match = mol.GetSubstructMatches(Chem.MolFromSmarts(beta_alanine_smarts))

    if not pantoic_acid_match or not beta_alanine_match:
        return False, "Missing pantoic acid or beta-alanine substructure"

    # Check for amide bond between pantoic acid and beta-alanine
    for p_idx in pantoic_acid_match:
        for b_idx in beta_alanine_match:
            p_atom = mol.GetAtomWithIdx(p_idx)
            b_atom = mol.GetAtomWithIdx(b_idx)
            if p_atom.GetBonds()[0].GetBondType() == Chem.BondType.AMIDE:
                if b_atom.GetBonds()[0].GetBondType() == Chem.BondType.AMIDE:
                    if p_atom.GetBonds()[0].GetOtherAtomIdx(p_idx) == b_idx:
                        return True, "Molecule is a pantothenic acid"

    return False, "No amide bond found between pantoic acid and beta-alanine substructures"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25848',
                          'name': 'pantothenic acids',
                          'definition': 'A class of amides formed from pantoic '
                                        'acid and beta-alanine and its '
                                        'derivatives.',
                          'parents': ['CHEBI:22823', 'CHEBI:37622']},
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
             '    Mol.GetAtomWithIdx(Mol, tuple)\n'
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