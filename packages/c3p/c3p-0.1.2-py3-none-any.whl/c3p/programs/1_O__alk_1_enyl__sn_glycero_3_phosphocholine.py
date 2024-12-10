"""
Classifies: CHEBI:17832 1-O-(alk-1-enyl)-sn-glycero-3-phosphocholine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_1_O__alk_1_enyl__sn_glycero_3_phosphocholine(smiles: str):
    """
    Determines if a molecule is a 1-O-(alk-1-enyl)-sn-glycero-3-phosphocholine.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a 1-O-(alk-1-enyl)-sn-glycero-3-phosphocholine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for glycerophosphocholine core
    atoms = mol.GetAtoms()
    glycerol_atoms = []
    phosphate_atom = None
    choline_atoms = []

    for atom in atoms:
        symbol = atom.GetSymbol()
        if symbol == 'C':
            glycerol_atoms.append(atom)
        elif symbol == 'P':
            phosphate_atom = atom
        elif symbol == 'N':
            choline_atoms.append(atom)

    if len(glycerol_atoms) != 3 or phosphate_atom is None or len(choline_atoms) != 1:
        return False, "Molecule does not contain the glycerophosphocholine core"

    # Check for alkene substituent on glycerol carbon 1
    alkene_atom = None
    for atom in glycerol_atoms:
        neighbors = atom.GetNeighbors()
        for neighbor in neighbors:
            if neighbor.GetSymbol() == 'C' and neighbor.GetIsAromatic() and neighbor.GetDegree() == 2:
                alkene_atom = neighbor
                break

    if alkene_atom is None:
        return False, "No alkene substituent found on glycerol carbon 1"

    # Check for alkene chain
    alkene_chain = []
    current_atom = alkene_atom
    while current_atom.GetDegree() == 2 and current_atom.GetSymbol() == 'C':
        alkene_chain.append(current_atom)
        neighbor = [n for n in current_atom.GetNeighbors() if n.GetIdx() != alkene_chain[-1].GetIdx()][0]
        current_atom = neighbor

    if len(alkene_chain) < 2:
        return False, "Alkene chain is too short"

    return True, "Molecule is a 1-O-(alk-1-enyl)-sn-glycero-3-phosphocholine"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17832',
                          'name': '1-O-(alk-1-enyl)-sn-glycero-3-phosphocholine',
                          'definition': 'An sn-glycero-3-phosphocholine '
                                        'substituted at the 1-oxygen by an '
                                        'alk-1-enyl group.',
                          'parents': ['CHEBI:64590', 'CHEBI:76170']},
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
    'num_true_negatives': 183925,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945630307842}