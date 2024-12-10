"""
Classifies: CHEBI:139066 mannosylinositol-1-phosphophytoceramide(1-)
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_mannosylinositol_1_phosphophytoceramide_1__(smiles: str):
    """
    Determines if a molecule is a mannosylinositol-1-phosphophytoceramide(1-).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a mannosylinositol-1-phosphophytoceramide(1-), False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Extract the molecular fragments
    fragments = Chem.GetMolFrags(mol, aromatics=Chem.Aromaticity.AROMATICITY_MDL)

    # Check if there is a single fragment
    if len(fragments) != 1:
        return False, "Molecule contains multiple fragments"

    # Check for the presence of mannose, inositol, and phosphate groups
    mannose_present = False
    inositol_present = False
    phosphate_present = False

    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetDegree() == 2:
            neighbors = [mol.GetAtomWithIdx(n).GetSymbol() for n in atom.GetNeighbors()]
            if 'C' in neighbors and 'P' in neighbors:
                phosphate_present = True

        if atom.GetSmarts() == 'C1OC(O)C(O)C(O)C(O)C1O':
            inositol_present = True

        if atom.GetSmarts() == 'C1OC(OC2OC(CO)C(O)C(O)C2O)C(O)C(O)C1O':
            mannose_present = True

    if not (mannose_present and inositol_present and phosphate_present):
        return False, "Molecule does not contain the required functional groups"

    # Check for the presence of a ceramide-like chain
    ceramide_chain_present = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N':
            neighbors = [mol.GetAtomWithIdx(n).GetSymbol() for n in atom.GetNeighbors()]
            if 'C' in neighbors and 'C' in neighbors and 'C' in neighbors:
                ceramide_chain_present = True
                break

    if not ceramide_chain_present:
        return False, "Molecule does not contain a ceramide-like chain"

    # Check for the presence of a negative charge
    formal_charge = sum(atom.GetFormalCharge() for atom in mol.GetAtoms())
    if formal_charge != -1:
        return False, "Molecule does not have a negative charge"

    return True, "Molecule is a mannosylinositol-1-phosphophytoceramide(1-)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:139066',
                          'name': 'mannosylinositol-1-phosphophytoceramide(1-)',
                          'definition': 'An mannosylinositol '
                                        'phosphophytoceramide(1-) obtained by '
                                        'deprotonation of the free phosphate '
                                        'OH group of any '
                                        'mannosylinositol-1-phosphophytoceramide; '
                                        'major species at pH 7.3.',
                          'parents': ['CHEBI:64991']},
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
    'error': "module 'rdkit.Chem' has no attribute 'Aromaticity'",
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