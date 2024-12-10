"""
Classifies: CHEBI:28874 phosphatidylinositol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_phosphatidylinositol(smiles: str):
    """
    Determines if a molecule is a phosphatidylinositol, defined as 'Any glycerophosphoinositol having one phosphatidyl group esterified to one of the hydroxy groups of inositol.'

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a phosphatidylinositol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains an inositol ring
    inositol_ring_atoms = []
    for ring in mol.GetRingInfo().AtomRings():
        if len(ring) == 6:
            ring_atoms = [mol.GetAtomWithIdx(idx) for idx in ring]
            if all(atom.GetSymbol() == "O" for atom in ring_atoms):
                inositol_ring_atoms = ring_atoms
                break

    if not inositol_ring_atoms:
        return False, "Molecule does not contain an inositol ring"

    # Check if the inositol ring has a phosphate group attached
    phosphate_attached = False
    for atom in inositol_ring_atoms:
        for neighbor in atom.GetNeighbors():
            if neighbor.GetSymbol() == "P":
                phosphate_attached = True
                break

    if not phosphate_attached:
        return False, "Inositol ring does not have a phosphate group attached"

    # Check if the molecule contains glycerol
    glycerol_atoms = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == "O" and len(atom.GetNeighbors()) == 3:
            neighbors = [neighbor.GetSymbol() for neighbor in atom.GetNeighbors()]
            if "C" in neighbors and "C" in neighbors and "C" in neighbors:
                glycerol_atoms.append(atom)

    if not glycerol_atoms:
        return False, "Molecule does not contain glycerol"

    # Check if the glycerol is attached to the phosphate
    glycerol_attached = False
    for atom in glycerol_atoms:
        for neighbor in atom.GetNeighbors():
            if neighbor.GetSymbol() == "P":
                glycerol_attached = True
                break

    if not glycerol_attached:
        return False, "Glycerol is not attached to the phosphate group"

    # Check if the molecule has acyl chains
    acyl_chains = []
    for atom in glycerol_atoms:
        for neighbor in atom.GetNeighbors():
            if neighbor.GetSymbol() == "C" and len(neighbor.GetNeighbors()) > 1:
                acyl_chain = [neighbor]
                current_atom = neighbor
                while True:
                    neighbors = [n for n in current_atom.GetNeighbors() if n.GetSymbol() == "C"]
                    if len(neighbors) == 1:
                        current_atom = neighbors[0]
                        acyl_chain.append(current_atom)
                    else:
                        break
                acyl_chains.append(acyl_chain)

    if not acyl_chains or len(acyl_chains) < 2:
        return False, "Molecule does not have two acyl chains"

    # If all conditions are met, it's a phosphatidylinositol
    acyl_chain_lengths = [len(chain) for chain in acyl_chains]
    return True, f"Phosphatidylinositol with acyl chain lengths {acyl_chain_lengths}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28874',
                          'name': 'phosphatidylinositol',
                          'definition': 'Any glycerophosphoinositol having one '
                                        'phosphatidyl group esterified to one '
                                        'of the hydroxy groups of inositol.',
                          'parents': ['CHEBI:36315']},
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
    'num_true_negatives': 183499,
    'num_false_negatives': 48,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9997384866001624}