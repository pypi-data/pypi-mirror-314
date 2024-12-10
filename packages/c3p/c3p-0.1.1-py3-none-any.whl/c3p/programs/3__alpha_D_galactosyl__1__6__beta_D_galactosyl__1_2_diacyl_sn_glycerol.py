"""
Classifies: CHEBI:28396 3-[alpha-D-galactosyl-(1->6)-beta-D-galactosyl]-1,2-diacyl-sn-glycerol
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors, rdMolDescriptors

def is_3__alpha_D_galactosyl__1__6__beta_D_galactosyl__1_2_diacyl_sn_glycerol(smiles: str):
    """
    Determines if a molecule is a 3-[alpha-D-galactosyl-(1->6)-beta-D-galactosyl]-1,2-diacyl-sn-glycerol.

    A digalactosylglycerol derivative in which the digalactosyl moiety is alpha-D-galactosyl-(1->6)-beta-D-galactosyl at O-3,
    with O-1 and O-2 both acylated.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule belongs to the class, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for glycerol backbone
    glycerol_atom_indices = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetDegree() == 2:
            glycerol_atom_indices.append(atom.GetIdx())

    if len(glycerol_atom_indices) != 3:
        return False, "Molecule does not contain a glycerol backbone"

    # Check for acylation at O-1 and O-2
    acylated_oxygen_indices = []
    for idx in glycerol_atom_indices:
        atom = mol.GetAtomWithIdx(idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetSymbol() == 'C' and neighbor.GetDegree() == 3 and any(nbr.GetSymbol() == 'O' and nbr.GetDegree() == 1 for nbr in neighbor.GetNeighbors()):
                acylated_oxygen_indices.append(idx)

    if len(acylated_oxygen_indices) != 2:
        return False, "Molecule is not acylated at O-1 and O-2"

    # Check for digalactosyl moiety at O-3
    digalactosyl_oxygen_idx = [idx for idx in glycerol_atom_indices if idx not in acylated_oxygen_indices][0]
    digalactosyl_atom = mol.GetAtomWithIdx(digalactosyl_oxygen_idx)

    if digalactosyl_atom.GetDegree() != 1:
        return False, "O-3 is not substituted with a digalactosyl moiety"

    digalactosyl_neighbor = digalactosyl_atom.GetNeighbors()[0]
    if digalactosyl_neighbor.GetSymbol() != 'C':
        return False, "Digalactosyl moiety is not attached to O-3 via a carbon atom"

    # Check for alpha-D-galactosyl-(1->6)-beta-D-galactosyl connectivity
    galactose_rings = Chem.GetSSSR(mol)
    if len(galactose_rings) != 2:
        return False, "Molecule does not contain two galactose rings"

    alpha_galactose_ring, beta_galactose_ring = galactose_rings

    alpha_ring_atoms = [mol.GetAtomWithIdx(idx) for idx in alpha_galactose_ring]
    beta_ring_atoms = [mol.GetAtomWithIdx(idx) for idx in beta_galactose_ring]

    if not all(atom.GetSymbol() == 'C' or atom.GetSymbol() == 'O' for atom in alpha_ring_atoms):
        return False, "Alpha galactose ring contains non-C/O atoms"

    if not all(atom.GetSymbol() == 'C' or atom.GetSymbol() == 'O' for atom in beta_ring_atoms):
        return False, "Beta galactose ring contains non-C/O atoms"

    alpha_ring_oxygen_indices = [atom.GetIdx() for atom in alpha_ring_atoms if atom.GetSymbol() == 'O']
    beta_ring_oxygen_indices = [atom.GetIdx() for atom in beta_ring_atoms if atom.GetSymbol() == 'O']

    if len(alpha_ring_oxygen_indices) != 1 or len(beta_ring_oxygen_indices) != 1:
        return False, "Galactose rings do not have the expected number of oxygen atoms"

    alpha_ring_oxygen = mol.GetAtomWithIdx(alpha_ring_oxygen_indices[0])
    beta_ring_oxygen = mol.GetAtomWithIdx(beta_ring_oxygen_indices[0])

    if alpha_ring_oxygen.GetDegree() != 2 or beta_ring_oxygen.GetDegree() != 2:
        return False, "Galactose ring oxygen atoms do not have the expected connectivity"

    alpha_ring_oxygen_neighbor = [neighbor for neighbor in alpha_ring_oxygen.GetNeighbors() if neighbor.GetIdx() not in alpha_galactose_ring][0]
    beta_ring_oxygen_neighbor = [neighbor for neighbor in beta_ring_oxygen.GetNeighbors() if neighbor.GetIdx() not in beta_galactose_ring][0]

    if alpha_ring_oxygen_neighbor.GetSymbol() != 'C' or beta_ring_oxygen_neighbor.GetSymbol() != 'C':
        return False, "Galactose rings are not connected via oxygen atoms"

    if alpha_ring_oxygen_neighbor.GetDegree() != 4 or beta_ring_oxygen_neighbor.GetDegree() != 4:
        return False, "Atoms connecting galactose rings do not have the expected connectivity"

    if alpha_ring_oxygen_neighbor.GetNeighbor(1).GetIdx() != beta_ring_oxygen_neighbor.GetIdx():
        return False, "Galactose rings are not connected in the expected (1->6) configuration"

    return True, "Molecule is a 3-[alpha-D-galactosyl-(1->6)-beta-D-galactosyl]-1,2-diacyl-sn-glycerol"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28396',
                          'name': '3-[alpha-D-galactosyl-(1->6)-beta-D-galactosyl]-1,2-diacyl-sn-glycerol',
                          'definition': 'A digalactosylglycerol derivative in '
                                        'which the digalactosyl moiety is '
                                        'alpha-D-galactosyl-(1->6)-beta-D-galactosyl '
                                        'at O-3, with O-1 and O-2 both '
                                        'acylated.',
                          'parents': ['CHEBI:63428', 'CHEBI:90553']},
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
    'num_true_negatives': 183927,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999891262389291}