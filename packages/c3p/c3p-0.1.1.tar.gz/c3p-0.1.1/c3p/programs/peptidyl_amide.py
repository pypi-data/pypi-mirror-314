"""
Classifies: CHEBI:15722 peptidyl amide
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_peptidyl_amide(smiles: str) -> tuple[bool, str]:
    """
    Determines if a molecule is a peptidyl amide (a peptide with a carbamoyl group at the C-terminus).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a peptidyl amide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for peptide bonds
    peptide_bonds = AllChem.MMFFGetMoleculeProperties(mol).GetPropInt('NumPeptideBonds', 0)
    if peptide_bonds < 1:
        return False, "Molecule does not contain any peptide bonds"

    # Check for carbamoyl group at C-terminus
    carbamoyl_found = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetDegree() == 3:
            neighbors = [mol.GetAtomWithIdx(n).GetSymbol() for n in atom.GetNeighbors()]
            if 'O' in neighbors and 'N' in neighbors and 'N' in neighbors:
                carbamoyl_found = True
                break

    if carbamoyl_found:
        return True, "Molecule is a peptidyl amide (peptide with carbamoyl group at C-terminus)"
    else:
        return False, "Molecule does not have a carbamoyl group at the C-terminus"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:15722',
                          'name': 'peptidyl amide',
                          'definition': 'A peptide that has a carbamoyl group '
                                        'at the C-terminus.',
                          'parents': ['CHEBI:16670']},
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
    'error': "'MMFFMolProperties' object has no attribute 'GetPropInt'",
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