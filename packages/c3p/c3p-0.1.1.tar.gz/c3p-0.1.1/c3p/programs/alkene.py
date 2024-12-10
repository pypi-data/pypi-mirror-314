"""
Classifies: CHEBI:32878 alkene
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_alkene(smiles: str):
    """
    Determines if a molecule is an alkene.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is an alkene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check if the molecule contains only C and H atoms
    atom_symbols = set(atom.GetSymbol() for atom in mol.GetAtoms())
    if atom_symbols != {'C', 'H'}:
        return False, "Molecule contains non-hydrocarbon atoms"
    
    # Count the number of double bonds
    double_bonds = sum(bond.GetBondType() == Chem.BondType.DOUBLE for bond in mol.GetBonds())
    
    # Check for the presence of at least one double bond
    if double_bonds == 0:
        return False, "Molecule does not contain any double bonds"
    elif double_bonds > 1:
        return False, "Molecule contains more than one double bond"
    
    # Check if the molecule is acyclic
    if Chem.Descriptors.IsRingPresent(mol):
        return False, "Molecule is cyclic"
    
    return True, "Molecule is an alkene"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:32878',
                          'name': 'alkene',
                          'definition': 'An acyclic branched or unbranched '
                                        'hydrocarbon having one carbon-carbon '
                                        'double bond and the general formula '
                                        'CnH2n. Acyclic branched or unbranched '
                                        'hydrocarbons having more than one '
                                        'double bond are alkadienes, '
                                        'alkatrienes, etc.',
                          'parents': ['CHEBI:33645']},
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
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183869,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999673691366417}