"""
Classifies: CHEBI:19555 2-deoxy-D-glucoside
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_2_deoxy_D_glucoside(smiles: str):
    """
    Determines if a molecule is a 2-deoxy-D-glucoside compound.

    A 2-deoxy-D-glucoside compound is a D-glucoside compound with the 2-hydroxy substituent
    either absent or replaced by a different functional group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 2-deoxy-D-glucoside, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find the glucoside substructure
    glucoside_smarts = "OC1C(O)C(O)C(O)C(O)C1O"
    glucoside_mol = Chem.MolFromSmarts(glucoside_smarts)
    matches = mol.GetSubstructMatches(glucoside_mol)

    if not matches:
        return False, "Molecule does not contain a glucoside substructure"

    for match in matches:
        # Check if the 2-hydroxy substituent is absent or replaced
        atom_idx = match[1]
        atom = mol.GetAtomWithIdx(atom_idx)
        if atom.GetHybridization() == Chem.HybridizationType.SP3:
            if atom.GetNumExplicitHs() == 0:
                return True, "Molecule is a 2-deoxy-D-glucoside (2-hydroxy substituent absent)"
            elif atom.GetIsAromatic() or any(neighbor.GetIsAromatic() for neighbor in atom.GetNeighbors()):
                return True, "Molecule is a 2-deoxy-D-glucoside (2-hydroxy substituent replaced by an aromatic group)"
            else:
                substituent = ''.join(sorted([neighbor.GetSymbol() for neighbor in atom.GetNeighbors() if neighbor.GetIdx() not in match]))
                return True, f"Molecule is a 2-deoxy-D-glucoside (2-hydroxy substituent replaced by {substituent})"

    return False, "Molecule does not meet the criteria for a 2-deoxy-D-glucoside"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:19555',
                          'name': '2-deoxy-D-glucoside',
                          'definition': 'A D-glucoside compound with the '
                                        '2-hydroxy substituent either absent '
                                        'or replaced by a different functional '
                                        'group.',
                          'parents': ['CHEBI:35436']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'True positives: []\n'
               'False positives: '
               "[('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)(OC(CCCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](O)COC(=O)CCCCCCCCC/C=C\\\\CCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1[C@H](O)[C@@H](O)C(O)[C@@H](O)[C@H]1O)(OC[C@H](OC(=O)CCC/C=C\\\\[C@@H](O)/C=C/C=C\\\\C/C=C\\\\C=C\\\\[C@@H](O)C/C=C\\\\CC)COC(=O)CCCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCCCCCCCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCCCCCCCCCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCC/C=C\\\\CCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCC)COCCCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCCCC)=O)(OC(CCCCCCC/C=C\\\\CCCCCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O[C@@H]2OC([C@H](O)C(O)[C@@H]2O)CO)C(O)C(O)C(O)[C@H]1O[C@H]3OC([C@@H](O)C(O)[C@H]3O)CO)(OC[C@H](O)COC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCCCC)=O)(OC(CCCCCCCCCCCCCCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCCCC)=O)(OC(CCCCCCCCCCCCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCCCC/C=C\\\\CCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCCCCCCCCCC)=O)(OC(CCCCCCCCCCCCCCCCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\\\CCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCCCCC)COC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCCCCCCCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1[C@H](O)[C@H](O)C(O)[C@H](O)[C@H]1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)([O-])=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1[C@H](O)[C@@H](O)C(O)[C@H](O)[C@@H]1O)(O)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](O)COC(=O)CCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COCCCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('OC1C(O)C(O)C(OP([O-])(=O)OCC(CO[*])OC([*])=O)C(O)C1O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCCCC/C=C\\\\CCCCCC)=O)(OC(CCCCCCCCC/C=C\\\\CCCCCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCC)COCCCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCC(O)/C=C/C(O)=O)COC(=O)CCCCCCC/C=C\\\\CCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCC/C=C\\\\CCCCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1[C@@H](O)[C@@H](O)C(OP(O)(O)=O)[C@H](O)[C@H]1O)(O)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCCCCCCCCCCCC)=O)(OC(CCCCCCC/C=C\\\\C/C=C\\\\CCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCCCCCCCCCC)=O)(OC(CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('S(C[C@H](N)C(O[C@@H](COP(OC1[C@H](O)[C@H](O)C(O)[C@H](O)[C@H]1O)(O)=O)COC(=O)CCCCCCCCCCCCCCCCC)=O)[C@@H]([C@@H](O)CCCC(O)=O)/C=C/C=C/C=C\\\\C/C=C\\\\CCCCC', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)(OC(CCCCCCC/C=C\\\\CCCCCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCC/C=C\\\\CCCCCCCC)=O)(OC(CCCCCCCCCCCCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCCCC/C=C\\\\CCCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCC/C=C\\\\CCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COCCCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1[C@H](O)[C@@H](O)C(O)[C@@H](O)[C@H]1O)(OCC(OC(=O)CCCCCCCCCCCCCCC)CO)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)C(O)C1O)(OCC(OC(=O)CCC/C=C\\\\CC2OC2C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCC/C=C\\\\CCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('O(C1[C@H](O)[C@@H](O)C(OC(=O)CC=2C=3C(NC2)=CC=CC3)[C@@H](O)[C@@H]1O)[C@@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('O(C1[C@@H](O)[C@H](O)C(O)[C@@H](O)[C@H]1O)C', 'Molecule is a "
               "2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCC/C=C\\\\CCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCCCCC)COCCCCCCCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCCCCCCCCCCCC)=O)(OC(CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCC)CO/C=C\\\\CCCCCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O[C@@H]2OC([C@H](O)C(O)[C@@H]2O)CO)C(O)C(O)C(O)[C@H]1O[C@H]3OC([C@@H](O)C(O)[C@H]3O)CO)(OC[C@H](O)COC(=O)CCCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCCCCCCCCCCCC)=O)(OC(CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCC/C=C\\\\CCCCCCCC)=O)(OC(CCCCCCC/C=C\\\\CCCCCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)(OC(CCCCCCCCCCCCCCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('OC(CO[*])COP([O-])(=O)OC1C(O)C(O)C(O)C(O)C1O', 'Molecule is "
               "a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\\\CCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCCCC/C=C\\\\CCCCCCCC)=O)(OC(CCCCCCCCC/C=C\\\\CCCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)COC(=O)CCCCCCC/C=C\\\\CCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCC)COC(=O)CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCCCC/C=C\\\\CCCCCC)=O)(OC(CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1[C@H](O)[C@H](O)C(O)[C@H](O)[C@H]1O)(OC[C@H](O)CO)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O[C@@H]2OC([C@H](O)C(O)[C@@H]2O)CO)C(O)C(O)C(O)[C@H]1O[C@H]3OC([C@@H](O)C(O)[C@H]3O)CO)(OC[C@H](O)COC(=O)CCCCCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCCC)COCCCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCC)COC(=O)CCCCCCC/C=C\\\\CCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCCCC/C=C\\\\CCCCCC)=O)(OC(CCCCCCCCCCCCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](O)COC(=O)CCCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1[C@H](O)[C@H](O)C(O)[C@H](O)[C@H]1O)(OC[C@H](OC(=O)CCCC(O)/C=C/C=C/C\\\\C=C\\\\CCCCCCCC)COC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCC(O)=O)COC(=O)CCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCCCCC)COC(=O)CCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\C/C=C\\\\CCCC)COC(=O)CCCCCCCCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCC)COC(=O)CCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCC(=O)/C=C/C=O)COC(=O)CCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCC)CO/C=C\\\\CCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCCCC)COC(=O)CCCCCCCCCCCCCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCCCC/C=C\\\\CCCCCC)=O)(OC(CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCC/C=C\\\\CCCCCCC)COC(=O)CCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCC(=O)/C=C/C=O)COC(=O)CCCCCCC/C=C\\\\CCCCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('O(C1[C@H](O)[C@@H](O)C(O)[C@H](O)[C@@H]1O)[C@H]2O[C@@H]([C@H](O)[C@H](O)[C@H]2O)CO[C@H]3O[C@@H]([C@H](O)[C@H](O)[C@H]3O)CO[C@H]4O[C@@H]([C@H](O)[C@H](O)[C@H]4O)CO', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCCCC/C=C\\\\CCCCCCCC)=O)(OC(CCCCCCC/C=C\\\\CCCCCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](O)COC(=O)CCCCCCC/C=C\\\\CCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CCCCCCCCCCCCCCC)=O)(OC(CCCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('P(OC1C(O)C(O)C(O)[C@@H](O)C1O)(OC[C@H](OC(=O)CCCCCCCCCCC/C=C\\\\C/C=C\\\\CCCCC)COC(=O)CCCCCCC/C=C\\\\CCCCCC)(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside'), "
               "('[C@@H]1(C(C(C([C@H](C1O)O)O)O)O)OP(OC[C@@](COC(CC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)=O)(OC(CCCCCCCCCCCCCCC)=O)[H])(O)=O', "
               "'Molecule is a 2-deoxy-D-glucoside')]\n"
               'False negatives: '
               "[('CC(=O)N[C@@H](CSCC(=O)c1ccccc1)C(=O)N[C@@H]1[C@@H](O)[C@H](O)[C@@H](CO)O[C@@H]1O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O', "
               "'Molecule contains 2-hydroxy substituent')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 16470,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.9939653611731338}