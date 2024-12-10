"""
Classifies: CHEBI:133070 yanuthones
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_yanuthones(smiles: str):
    """
    Determines if a molecule is a yanuthone.

    A class of meroterpenoids whose core structure consists of 5,6-epoxycyclohex-2-en-1-one which is substituted by
    varying side chains at positions 3 and 4, and by a sesquiterpene chain at position 6. The core structure may be
    derived from 6-methylsalicylic acid, which due to a decarboxylation results in a C7 scaffold (a 6-membered
    methylated ring); these are known as class I yanuthones. Class II yanuthones contain a C6 scaffold derived
    from an unknown precursor.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a yanuthone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find the 5,6-epoxycyclohex-2-en-1-one core
    core_smarts = "[C@H]1[C@@H]2[C@H]([C@@H]3[C@@H]([C@@H]([C@H](O3)C2=O)O)O)O1"
    patt = Chem.MolFromSmarts(core_smarts)
    core_match = mol.GetSubstructMatches(patt)
    if not core_match:
        return False, "Core structure not found"

    # Check for substituents at positions 3 and 4
    core_atoms = set(core_match[0])
    substituents_3 = []
    substituents_4 = []
    for atom_idx in core_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        if atom.GetSymbol() == 'C':
            for neighbor in atom.GetNeighbors():
                if neighbor.GetIdx() not in core_atoms:
                    if neighbor.GetIsAromatic():
                        return False, "Aromatic substituent found"
                    if atom.GetProp3D('_CIPCode') == 'R':
                        substituents_4.append(neighbor.GetSymbol())
                    else:
                        substituents_3.append(neighbor.GetSymbol())

    # Check for sesquiterpene chain at position 6
    sesquiterpene_chain = False
    for atom_idx in core_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        if atom.GetSymbol() == 'C' and atom.GetProp3D('_CIPCode') == 'S':
            for neighbor in atom.GetNeighbors():
                if neighbor.GetIdx() not in core_atoms:
                    sesquiterpene_chain = True
                    break

    if not sesquiterpene_chain:
        return False, "Sesquiterpene chain not found"

    # Classify as Class I or Class II
    if len(substituents_3) > 0 or len(substituents_4) > 0:
        return True, f"Class I yanuthone with substituents at positions 3 and 4: {', '.join(set(substituents_3 + substituents_4))}"
    else:
        return True, "Class II yanuthone"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:133070',
                          'name': 'yanuthones',
                          'definition': 'A class of meroterpenoids whose core '
                                        'structure consists of '
                                        '5,6-epoxycyclohex-2-en-1-one which is '
                                        'substituted by varying side chains at '
                                        'positions 3 and 4, and by a '
                                        'sesquiterpene chain at position 6. '
                                        'The core structure may be derived '
                                        'from 6-methylsalicylic acid, which '
                                        'due to a decarboxylation results in a '
                                        'C7 scaffold (a 6-membered methylated '
                                        'ring); these are known as class I '
                                        'yanuthones. Class II yanuthones '
                                        'contain a C6 scaffold derived from an '
                                        'unknown precursor.',
                          'parents': [   'CHEBI:32955',
                                         'CHEBI:48953',
                                         'CHEBI:51689',
                                         'CHEBI:64419']},
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
    'num_true_negatives': 183921,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.999994562912539}