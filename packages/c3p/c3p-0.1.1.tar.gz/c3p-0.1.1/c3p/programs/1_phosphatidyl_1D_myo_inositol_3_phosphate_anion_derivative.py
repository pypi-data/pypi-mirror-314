"""
Classifies: CHEBI:147335 1-phosphatidyl-1D-myo-inositol-3-phosphate anion derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_1_phosphatidyl_1D_myo_inositol_3_phosphate_anion_derivative(smiles: str):
    """
    Determines if a molecule is a 1-phosphatidyl-1D-myo-inositol-3-phosphate anion derivative.

    A 1-phosphatidyl-1D-myo-inositol-3-phosphate anion derivative is defined as a phosphatidylinositol
    anion where the inositol is phosphorylated at position 3 and either phosphorylated or not at
    position 4 and/or position 5; major species at pH 7.3.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a 1-phosphatidyl-1D-myo-inositol-3-phosphate anion derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find the inositol ring
    inositol_ring = None
    for ring in mol.GetRingInfo().AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetSymbol() == 'O' for atom in atoms):
                inositol_ring = ring
                break

    if inositol_ring is None:
        return False, "No inositol ring found"

    # Check if inositol is phosphorylated at position 3
    inositol_atoms = [mol.GetAtomWithIdx(i) for i in inositol_ring]
    phosphate_count = sum(1 for atom in inositol_atoms if atom.GetDegree() == 4)
    if phosphate_count < 1:
        return False, "Inositol ring is not phosphorylated at position 3"

    # Check if inositol is phosphorylated or not at position 4 and/or position 5
    phosphate_count = sum(1 for atom in inositol_atoms if atom.GetDegree() == 4)
    if phosphate_count < 1 or phosphate_count > 3:
        return False, "Inositol ring is not phosphorylated at positions 3, 4, and/or 5"

    # Check if the molecule is an anion
    formal_charge = Chem.GetFormalCharge(mol)
    if formal_charge >= 0:
        return False, "Molecule is not an anion"

    return True, "Molecule is a 1-phosphatidyl-1D-myo-inositol-3-phosphate anion derivative"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:147335',
                          'name': '1-phosphatidyl-1D-myo-inositol-3-phosphate '
                                  'anion derivative',
                          'definition': 'A phosphatidylinositol anion where '
                                        'the inositol is phosphorylated at '
                                        'position 3 and either phosphorylated '
                                        'or not at position 4 and/or position '
                                        '5; major species at pH 7.3.',
                          'parents': ['CHEBI:62643']},
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
    'num_true_negatives': 183924,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945630012234}