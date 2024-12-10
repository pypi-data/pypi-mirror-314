"""
Classifies: CHEBI:33240 coordination entity
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_coordination_entity(smiles: str):
    """
    Determines if a molecule is a coordination entity.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a coordination entity, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get all atoms and their coordinated neighbors
    atom_coords = []
    for atom in mol.GetAtoms():
        coords = []
        for neighbor in atom.GetNeighbors():
            bond = mol.GetBondBetweenAtoms(atom.GetIdx(), neighbor.GetIdx())
            if bond.GetIsCoordinate():
                coords.append(neighbor.GetSymbol())
        atom_coords.append((atom.GetSymbol(), coords))

    # Check for central atom and ligands
    central_atoms = []
    ligands = []
    for symbol, coords in atom_coords:
        if len(coords) > 0:
            central_atoms.append(symbol)
            ligands.extend(coords)

    # Classify as coordination entity if there is a central atom with ligands
    if len(central_atoms) > 0 and len(ligands) > 0:
        central_atom_str = ', '.join(set(central_atoms))
        ligand_str = ', '.join(set(ligands))
        reason = f"Central atom(s): {central_atom_str}, Ligand(s): {ligand_str}"
        return True, reason

    return False, "No coordination entity found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33240',
                          'name': 'coordination entity',
                          'definition': 'An assembly consisting of a central '
                                        'atom (usually metallic) to which is '
                                        'attached a surrounding array of other '
                                        'groups of atoms (ligands).',
                          'parents': ['CHEBI:37577']},
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
    'success': False,
    'best': True,
    'error': "'Bond' object has no attribute 'GetIsCoordinate'",
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