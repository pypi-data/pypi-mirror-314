"""
Classifies: CHEBI:142839 enolate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_enolate(smiles: str):
    """
    Determines if a molecule is an enolate (an organic anion arising from deprotonation of the hydroxy group of an enol).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an enolate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find enol groups
    enol_atoms = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetTotalNumHs() == 1:
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'C' and neighbor.GetTotalNumHs() == 1:
                    enol_atoms.append((atom.GetIdx(), neighbor.GetIdx()))

    if not enol_atoms:
        return False, "No enol groups found"

    # Check if enol groups are deprotonated
    for enol_atom_idx, enol_carbon_idx in enol_atoms:
        enol_atom = mol.GetAtomWithIdx(enol_atom_idx)
        enol_carbon = mol.GetAtomWithIdx(enol_carbon_idx)
        if enol_atom.GetFormalCharge() == -1 and enol_carbon.GetTotalNumHs() == 0:
            return True, f"Enolate formed from deprotonation of enol group at atom indices {enol_atom_idx} and {enol_carbon_idx}"

    return False, "Enol groups found, but not deprotonated"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:142839',
                          'name': 'enolate',
                          'definition': 'An organic anion arising from '
                                        'deprotonation of the hydroxy group of '
                                        'an enol.',
                          'parents': ['CHEBI:25696']},
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
    'num_true_negatives': 183919,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945628534145}