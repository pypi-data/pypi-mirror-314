"""
Classifies: CHEBI:24346 phosphoglyceric acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_phosphoglyceric_acid(smiles: str):
    """
    Determines if a molecule is a phosphoglyceric acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a phosphoglyceric acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a carboxyl group
    carboxyl_groups = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == "O" and atom.IsInRingSize(0) and any(mol.GetAtomWithIdx(neighbor).GetSymbol() == "C" and mol.GetAtomWithIdx(neighbor).GetFormalCharge() == 0 and mol.GetAtomWithIdx(neighbor).GetIsAromatic() == False and len([neighbor_atom for neighbor_atom in mol.GetAtomWithIdx(neighbor).GetNeighbors() if mol.GetAtomWithIdx(neighbor_atom).GetSymbol() == "O" and mol.GetAtomWithIdx(neighbor_atom).GetFormalCharge() == 0]) == 2 for neighbor in atom.GetNeighbors())]
    if not carboxyl_groups:
        return False, "No carboxyl group found"

    # Check for the presence of a phosphate group
    phosphate_groups = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == "P" and atom.GetFormalCharge() == 0 and len([neighbor for neighbor in atom.GetNeighbors() if mol.GetAtomWithIdx(neighbor).GetSymbol() == "O" and mol.GetAtomWithIdx(neighbor).GetFormalCharge() == -1]) == 4]
    if not phosphate_groups:
        return False, "No phosphate group found"

    # Check if the phosphate group is connected to the carboxyl carbon
    carboxyl_carbon = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == "C" and atom.GetFormalCharge() == 0 and atom.GetIsAromatic() == False and len([neighbor for neighbor in atom.GetNeighbors() if mol.GetAtomWithIdx(neighbor).GetSymbol() == "O" and mol.GetAtomWithIdx(neighbor).GetFormalCharge() == 0]) == 2][0]
    phosphate_neighbors = [mol.GetAtomWithIdx(neighbor).GetSymbol() for neighbor in mol.GetAtomWithIdx(phosphate_groups[0]).GetNeighbors()]
    if "C" not in phosphate_neighbors:
        return False, "Phosphate group not connected to carboxyl carbon"

    return True, "Molecule is a phosphoglyceric acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24346',
                          'name': 'phosphoglyceric acid',
                          'definition': 'An aldonic acid phosphate where the '
                                        'aldonic acid component is glyceric '
                                        'acid.',
                          'parents': ['CHEBI:22300']},
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
    'num_true_negatives': 183924,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999945630012234}