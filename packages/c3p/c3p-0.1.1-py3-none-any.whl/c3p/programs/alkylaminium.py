"""
Classifies: CHEBI:17664 alkylaminium
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_alkylaminium(smiles: str):
    """
    Determines if a molecule is an alkylaminium, defined as a primary ammonium
    ion obtained by protonation of the amino group of any alkylamine; major species at pH 7.3.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an alkylaminium, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find the ammonium nitrogen atom
    ammonium_n = None
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N' and atom.GetFormalCharge() == 1:
            ammonium_n = atom
            break

    if ammonium_n is None:
        return False, "No ammonium nitrogen found"

    # Check if the ammonium nitrogen is part of a primary amine
    neighbors = ammonium_n.GetNeighbors()
    if len(neighbors) != 3:
        return False, "Ammonium nitrogen is not part of a primary amine"

    # Check if the substituents are alkyl groups
    alkyl_substituents = []
    for neighbor in neighbors:
        is_alkyl, alkyl_chain = is_alkyl_chain(mol, neighbor.GetIdx())
        if not is_alkyl:
            return False, f"Non-alkyl substituent found: {Chem.MolToSmiles(Chem.MolFromAtomBondAtomMapper(mol, neighbor.GetAtomicNum()))}"
        alkyl_substituents.append(alkyl_chain)

    return True, f"Alkylaminium with alkyl substituents: {', '.join(alkyl_substituents)}"

def is_alkyl_chain(mol, atom_idx):
    """
    Checks if the atom at the given index is part of an alkyl chain.

    Args:
        mol (Mol): RDKit molecule object
        atom_idx (int): Index of the atom to start from

    Returns:
        bool: True if the atom is part of an alkyl chain, False otherwise
        str: The alkyl chain in SMILES format
    """
    visited = set()
    queue = [(atom_idx, [])]

    while queue:
        curr_idx, chain = queue.pop(0)
        visited.add(curr_idx)
        atom = mol.GetAtomWithIdx(curr_idx)

        if atom.GetSymbol() != 'C':
            return False, ''

        neighbors = atom.GetNeighbors()
        if len(neighbors) > 2:
            return False, ''

        for neighbor in neighbors:
            if neighbor.GetIdx() not in visited:
                new_chain = chain + [neighbor.GetIdx()]
                queue.append((neighbor.GetIdx(), new_chain))

    return True, Chem.MolToSmiles(Chem.MolFromAtomBondAtomMapper(mol, [mol.GetAtomWithIdx(idx).GetAtomicNum() for idx in chain]))


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17664',
                          'name': 'alkylaminium',
                          'definition': 'A primary ammonium ion obtained by '
                                        'protonation of the amino goup of any '
                                        'alkylamine; major species at pH 7.3.',
                          'parents': ['CHEBI:65296']},
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
    'error': "module 'rdkit.Chem' has no attribute 'MolFromAtomBondAtomMapper'",
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