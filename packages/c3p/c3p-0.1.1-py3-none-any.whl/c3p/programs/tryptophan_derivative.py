"""
Classifies: CHEBI:27164 tryptophan derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_tryptophan_derivative(smiles: str):
    """
    Determines if a molecule is a tryptophan derivative.

    A tryptophan derivative is defined as an amino acid derivative resulting from
    reaction of tryptophan at the amino group or the carboxy group, or from the
    replacement of any hydrogen of tryptophan by a heteroatom. The definition
    normally excludes peptides containing tryptophan residues.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a tryptophan derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find tryptophan substructure
    tryptophan = Chem.MolFromSmiles('N[C@@H](Cc1c[nH]c2ccccc12)C(O)=O')
    if not mol.HasSubstructMatch(tryptophan):
        return False, "Molecule does not contain tryptophan substructure"

    # Check for modifications
    modified = False
    reason = "Unmodified tryptophan"

    # Check for substitutions on the amino group
    amino_atom = mol.GetSubstructMatch(tryptophan)[0]
    amino_atom_mol = mol.GetAtomWithIdx(amino_atom)
    if amino_atom_mol.GetFormalCharge() != 0 or len(amino_atom_mol.GetNeighbors()) != 3:
        modified = True
        reason = "Modification at amino group"

    # Check for substitutions on the carboxy group
    carboxy_atom = mol.GetSubstructMatch(tryptophan)[2]
    carboxy_atom_mol = mol.GetAtomWithIdx(carboxy_atom)
    if carboxy_atom_mol.GetFormalCharge() != 0 or len(carboxy_atom_mol.GetNeighbors()) != 3:
        modified = True
        reason = "Modification at carboxy group"

    # Check for substitutions on the tryptophan core
    tryptophan_atoms = mol.GetSubstructMatch(tryptophan)
    for atom in mol.GetAtoms():
        if atom.GetIdx() not in tryptophan_atoms and atom.GetSymbol() != 'H':
            modified = True
            reason = "Substitution on tryptophan core"
            break

    return modified, reason


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27164',
                          'name': 'tryptophan derivative',
                          'definition': 'An amino acid derivative resulting '
                                        'from reaction of tryptophan  at the '
                                        'amino group or the carboxy group, or '
                                        'from the replacement of any hydrogen '
                                        'of tryptophan  by a heteroatom. The '
                                        'definition normally excludes peptides '
                                        'containing tryptophan residues.',
                          'parents': ['CHEBI:83821']},
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
    'num_true_positives': 5,
    'num_false_positives': 100,
    'num_true_negatives': 27652,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 1.0,
    'f1': 0.0909090909090909,
    'accuracy': 0.9963973051842778}