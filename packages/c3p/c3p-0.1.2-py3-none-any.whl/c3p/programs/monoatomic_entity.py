"""
Classifies: CHEBI:33238 monoatomic entity
"""
from rdkit import Chem

def is_monoatomic_entity(smiles: str):
    """
    Determines if a molecule is a monoatomic entity (consists of a single atom).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a monoatomic entity, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule consists of a single atom
    if mol.GetNumAtoms() != 1:
        return False, "Molecule has more than one atom"

    # Check if the atom has a charge or is an isotope
    atom = mol.GetAtomWithIdx(0)
    charge = atom.GetFormalCharge()
    isotope = atom.GetIsotope()

    if charge != 0 or isotope != 0:
        atom_symbol = atom.GetSymbol()
        if charge != 0:
            charge_str = "+" * charge if charge > 0 else "-" * abs(charge)
            return True, f"{atom_symbol}({charge_str})"
        else:
            return True, f"{atom_symbol}-{isotope}"
    else:
        return True, f"Neutral {atom.GetSymbol()} atom"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33238',
                          'name': 'monoatomic entity',
                          'definition': 'A monoatomic entity is a molecular '
                                        'entity consisting of a single atom.',
                          'parents': ['CHEBI:33259']},
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
    'num_true_positives': 18,
    'num_false_positives': 100,
    'num_true_negatives': 43746,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.15254237288135594,
    'recall': 1.0,
    'f1': 0.2647058823529412,
    'accuracy': 0.9977202261535656}