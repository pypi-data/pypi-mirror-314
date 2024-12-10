"""
Classifies: CHEBI:145707 glycosylarabinose
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_glycosylarabinose(smiles: str):
    """
    Determines if a molecule is a glycosylarabinose, a disaccharide having arabinose at the reducing end
    with a glycosyl residue attached at an unspecified position via a glycosidic bond.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a glycosylarabinose, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find the arabinose residue
    arabinose_found = False
    arabinose_atoms = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetDegree() == 1:
            arabinose_atoms = find_arabinose_residue(mol, atom.GetIdx())
            if arabinose_atoms:
                arabinose_found = True
                break

    if not arabinose_found:
        return False, "No arabinose residue found"

    # Check for the presence of a glycosyl residue
    glycosyl_found = False
    for atom_idx in arabinose_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetIdx() not in arabinose_atoms:
                glycosyl_found = True
                break

    if not glycosyl_found:
        return False, "No glycosyl residue found"

    return True, "Molecule is a glycosylarabinose"

def find_arabinose_residue(mol, start_atom_idx):
    """
    Recursively finds the arabinose residue in the molecule.

    Args:
        mol (rdkit.Chem.rdchem.Mol): RDKit molecule object
        start_atom_idx (int): Index of the starting atom

    Returns:
        list: List of atom indices that belong to the arabinose residue
    """
    arabinose_atoms = []
    visited_atoms = set()
    to_visit = [start_atom_idx]

    while to_visit:
        atom_idx = to_visit.pop(0)
        visited_atoms.add(atom_idx)
        atom = mol.GetAtomWithIdx(atom_idx)

        if atom.GetSymbol() != 'C' and atom.GetSymbol() != 'O':
            continue

        arabinose_atoms.append(atom_idx)

        for neighbor in atom.GetNeighbors():
            neighbor_idx = neighbor.GetIdx()
            if neighbor_idx not in visited_atoms:
                to_visit.append(neighbor_idx)

    if len(arabinose_atoms) == 11:  # Arabinose has 11 atoms
        return arabinose_atoms
    else:
        return []


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:145707',
                          'name': 'glycosylarabinose',
                          'definition': 'A disaccharide having arabinose at '
                                        'the reducing end with a glycosyl '
                                        'residue attached at an unspecified '
                                        'position via a glycosidic bond.',
                          'parents': ['CHEBI:36233']},
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
    'num_false_positives': 100,
    'num_true_negatives': 2318,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.95824720959074}