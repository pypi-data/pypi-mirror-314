"""
Classifies: CHEBI:167057 monolysocardiolipin(2-)
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_monolysocardiolipin_2__(smiles: str):
    """
    Determines if a molecule is a monolysocardiolipin(2-), defined as 'The organophosphate oxoanion formed 
    from any monolysocardiolipin by deprotonation of the two phospho groups; principal species present at pH 7.3'.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a monolysocardiolipin(2-), False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of two phosphate groups
    phosphate_count = sum(atom.GetSymbol() == 'P' for atom in mol.GetAtoms())
    if phosphate_count != 2:
        return False, "Does not contain exactly two phosphate groups"

    # Check for the presence of two deprotonated phosphate groups
    deprotonated_phosphate_count = sum(atom.GetFormalCharge() == -1 for atom in mol.GetAtoms())
    if deprotonated_phosphate_count != 2:
        return False, "Does not contain exactly two deprotonated phosphate groups"

    # Check for the presence of a glycerol backbone
    glycerol_atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'C' and atom.GetDegree() == 3 and atom.GetTotalNumHs() == 1]
    if len(glycerol_atoms) != 2:
        return False, "Does not contain a glycerol backbone"

    # Check for the presence of a fatty acid chain
    fatty_acid_atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'C' and atom.GetDegree() == 1 and atom.GetTotalNumHs() == 3]
    if not fatty_acid_atoms:
        return False, "Does not contain a fatty acid chain"

    return True, "Molecule is a monolysocardiolipin(2-)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:167057',
                          'name': 'monolysocardiolipin(2-)',
                          'definition': 'The organophosphate oxoanion formed '
                                        'from any monolysocardiolipin by '
                                        'deprotonation of the two phospho '
                                        'groups; principal species present at '
                                        'pH 7.3',
                          'parents': ['CHEBI:76529']},
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
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183921,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.999994562912539}