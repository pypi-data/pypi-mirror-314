"""
Classifies: CHEBI:23197 cholestanoyl-CoA
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_cholestanoyl_CoA(smiles: str):
    """
    Determines if a molecule is a cholestanoyl-CoA, defined as a steroidal acyl-CoA that results
    from the formal condensation of the thiol group of coenzyme A with the carboxy group of any
    cholestan-26-oic acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a cholestanoyl-CoA, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a CoA moiety
    CoA_pattern = Chem.MolFromSmarts('SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12')
    matches = mol.GetSubstructMatches(CoA_pattern)
    if not matches:
        return False, "CoA moiety not found"

    # Check for the presence of a cholestanoyl moiety
    cholestanoyl_pattern = Chem.MolFromSmarts('[C@@]1([H])CC[C@@]2([H])[C@]3([H])[C@H](O)C[C@]4([H])C[C@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C')
    matches = mol.GetSubstructMatches(cholestanoyl_pattern)
    if not matches:
        return False, "Cholestanoyl moiety not found"

    # Check for the presence of a carbonyl linker between the cholestanoyl and CoA moieties
    carbonyl_linker_pattern = Chem.MolFromSmarts('C(=O)')
    linker_atoms = mol.GetSubstructMatches(carbonyl_linker_pattern)
    linker_atom_idx = [atom_idx for atom_idx in linker_atoms if mol.GetAtomWithIdx(atom_idx).IsInRingSize(0)]

    if not linker_atom_idx:
        return False, "No carbonyl linker found between cholestanoyl and CoA moieties"

    linker_atom = mol.GetAtomWithIdx(linker_atom_idx[0])
    cholestanoyl_neighbor = None
    CoA_neighbor = None

    for neighbor in linker_atom.GetNeighbors():
        if neighbor.GetIdx() in [atom_idx for match in matches for atom_idx in cholestanoyl_pattern.GetAtomMapNumbers()]:
            cholestanoyl_neighbor = neighbor
        elif neighbor.GetIdx() in [atom_idx for match in matches for atom_idx in CoA_pattern.GetAtomMapNumbers()]:
            CoA_neighbor = neighbor

    if cholestanoyl_neighbor is None or CoA_neighbor is None:
        return False, "Cholestanoyl and CoA moieties not properly connected"

    return True, "Molecule is a cholestanoyl-CoA"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23197',
                          'name': 'cholestanoyl-CoA',
                          'definition': 'A steroidal acyl-CoA that results '
                                        'from the formal condensation of the '
                                        'thiol group of coenzyme A with the '
                                        'carboxy group of any cholestan-26-oic '
                                        'acid.',
                          'parents': ['CHEBI:52135']},
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
    'num_true_negatives': 183924,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999945630012234}