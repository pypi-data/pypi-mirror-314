"""
Classifies: CHEBI:138282 5'-end ribonucleotide(2-) residue
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_5__end_ribonucleotide_2___residue(smiles: str):
    """
    Determines if a molecule is a 5'-end ribonucleotide(2-) residue.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 5'-end ribonucleotide(2-) residue, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for nucleotide residue
    if not any(atom.GetSymbol() == 'P' for atom in mol.GetAtoms()):
        return False, "No phosphorus atoms found (not a nucleotide)"

    # Check for ribose sugar
    has_ribose = False
    for ring in mol.GetRingInfo().AtomRings():
        if len(ring) == 5:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if len([a for a in atoms if a.GetSymbol() == 'O']) == 1:  # One oxygen in the ring
                has_ribose = True
                break
    if not has_ribose:
        return False, "No ribose sugar found"

    # Check for 5' phosphate group
    phosphates = [a for a in mol.GetAtoms() if a.GetSymbol() == 'P']
    if not phosphates:
        return False, "No phosphate groups found"

    # Find the ribose sugar atom
    ribose_oxygen = None
    for ring in mol.GetRingInfo().AtomRings():
        if len(ring) == 5:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            ribose_oxygen = next((a for a in atoms if a.GetSymbol() == 'O'), None)
            break

    if ribose_oxygen is None:
        return False, "Failed to find ribose oxygen"

    # Check if the phosphate is attached to the 5' position
    ribose_neighbors = [mol.GetAtomWithIdx(j) for j in ribose_oxygen.GetNeighbors()]
    is_5_prime = any(n.GetSymbol() == 'P' for n in ribose_neighbors)

    if not is_5_prime:
        return False, "Phosphate not attached to 5' position"

    # Check for negative charge
    formal_charge = sum(atom.GetFormalCharge() for atom in mol.GetAtoms())
    if formal_charge != -2:
        return False, "Formal charge is not -2"

    return True, "Molecule is a 5'-end ribonucleotide(2-) residue"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:138282',
                          'name': "5'-end ribonucleotide(2-) residue",
                          'definition': 'An organic anionic group obtained by '
                                        'deprotonation of the phosphate OH '
                                        "groups of any 5'-end ribonucleotide "
                                        'residue. Major microspecies at pH '
                                        '7.3.',
                          'parents': ['CHEBI:64775']},
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
    'error': 'Python argument types in\n'
             '    Mol.GetAtomWithIdx(Mol, Atom)\n'
             'did not match C++ signature:\n'
             '    GetAtomWithIdx(RDKit::ROMol {lvalue} self, unsigned int idx)',
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