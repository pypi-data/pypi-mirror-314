"""
Classifies: CHEBI:18244 1-alkyl-sn-glycero-3-phosphoethanolamine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_1_alkyl_sn_glycero_3_phosphoethanolamine(smiles: str):
    """
    Determines if a molecule is a 1-alkyl-sn-glycero-3-phosphoethanolamine.
    A glycerophosphoethanolamine that is sn-glycero-3-phosphoethanolamine carrying any alkyl substituent at position 1.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 1-alkyl-sn-glycero-3-phosphoethanolamine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a glycerol backbone
    glycerol_smarts = "[C@](CO)(CO)CO"
    glycerol_match = mol.GetSubstructMatches(Chem.MolFromSmarts(glycerol_smarts))
    if not glycerol_match:
        return False, "No glycerol backbone found"

    # Check for the presence of a phosphate group
    phosphate_smarts = "OP(O)(=O)O"
    phosphate_match = mol.GetSubstructMatches(Chem.MolFromSmarts(phosphate_smarts))
    if not phosphate_match:
        return False, "No phosphate group found"

    # Check for the presence of an ethanolamine group
    ethanolamine_smarts = "OCCN"
    ethanolamine_match = mol.GetSubstructMatches(Chem.MolFromSmarts(ethanolamine_smarts))
    if not ethanolamine_match:
        return False, "No ethanolamine group found"

    # Check if the phosphate group is connected to the glycerol backbone and the ethanolamine group
    phosphate_atom = mol.GetAtomWithIdx(list(phosphate_match[0])[0])
    phosphate_neighbors = [mol.GetAtomWithIdx(nbr_idx) for nbr_idx in phosphate_atom.GetNeighbors()]

    glycerol_atom = None
    ethanolamine_atom = None
    for neighbor in phosphate_neighbors:
        if neighbor.GetSmarts() == "CO":
            glycerol_atom = neighbor
        elif neighbor.GetSmarts() == "OCCN":
            ethanolamine_atom = neighbor

    if not glycerol_atom or not ethanolamine_atom:
        return False, "Phosphate group not connected to glycerol backbone and ethanolamine group"

    # Check for the presence of an alkyl substituent at position 1
    alkyl_substituent = False
    for neighbor in glycerol_atom.GetNeighbors():
        if neighbor.GetSymbol() == "C" and neighbor.GetAtomicNum() != 8:
            alkyl_substituent = True
            break

    if alkyl_substituent:
        return True, "1-alkyl-sn-glycero-3-phosphoethanolamine"
    else:
        return False, "No alkyl substituent at position 1"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18244',
                          'name': '1-alkyl-sn-glycero-3-phosphoethanolamine',
                          'definition': 'A glycerophosphoethanolamine that is '
                                        'sn-glycero-3-phosphoethanolamine '
                                        'carrying any alkyl substituent at '
                                        'position 1.',
                          'parents': ['CHEBI:138320']},
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