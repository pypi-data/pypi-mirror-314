"""
Classifies: CHEBI:177898 omega-carboxy-(fatty acyl)-CoA(5-)
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_omega_carboxy__fatty_acyl__CoA_5__(smiles: str):
    """
    Determines if a molecule is an omega-carboxy-(fatty acyl)-CoA(5-).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an omega-carboxy-(fatty acyl)-CoA(5-), False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of CoA
    has_coa = 'CoA' in Chem.MolToSmiles(mol, isomericSmiles=True)
    if not has_coa:
        return False, "Molecule does not contain CoA"

    # Check for negative charges
    charge = AllChem.GetFormalCharge(mol)
    if charge != -5:
        return False, f"Molecule charge is {charge}, should be -5"

    # Check for carboxy and phosphate groups
    carboxy_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C' and
                        atom.GetTotalNumHs() == 0 and
                        len([neighbor for neighbor in atom.GetNeighbors() if neighbor.GetSymbol() == 'O']) == 2)
    if carboxy_count != 1:
        return False, f"Found {carboxy_count} carboxy groups, should be 1"

    phosphate_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'P')
    if phosphate_count != 2:
        return False, f"Found {phosphate_count} phosphate groups, should be 2"

    # Check for fatty acyl chain
    fatty_acyl_chain = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetTotalNumHs() >= 1:
            neighbors = [neighbor for neighbor in atom.GetNeighbors()
                         if neighbor.GetSymbol() == 'C' and neighbor.GetTotalNumHs() >= 1]
            if len(neighbors) >= 1:
                fatty_acyl_chain = True
                break

    if not fatty_acyl_chain:
        return False, "No fatty acyl chain found"

    return True, "Molecule is an omega-carboxy-(fatty acyl)-CoA(5-)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:177898',
                          'name': 'omega-carboxy-(fatty acyl)-CoA(5-)',
                          'definition': 'An acyl-CoA oxoanion obtained by '
                                        'deprotonation of the phosphate, '
                                        'diphosphate and carboxy groups of any '
                                        'omega-carboxy-(fatty acyl)-CoA; major '
                                        'species at pH 7.3.',
                          'parents': ['CHEBI:133241', 'CHEBI:61697']},
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
    'num_true_negatives': 183918,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945628238518}