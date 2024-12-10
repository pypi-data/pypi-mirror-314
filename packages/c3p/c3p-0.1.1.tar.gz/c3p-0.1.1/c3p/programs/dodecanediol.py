"""
Classifies: CHEBI:195615 dodecanediol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_dodecanediol(smiles: str):
    """
    Determines if a molecule is a dodecanediol (a diol that is dodecane carrying two hydroxy groups at unspecified positions).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a dodecanediol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains 12 carbon atoms and 2 oxygen atoms
    if Descriptors.HeavyAtomCount(mol) != 14:
        return False, "Molecule does not contain 12 carbon atoms and 2 oxygen atoms"

    # Check if the molecule contains exactly 2 hydroxyl groups
    hydroxyl_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and atom.GetHybridization() == Chem.HybridizationType.SP3)
    if hydroxyl_count != 2:
        return False, "Molecule does not contain exactly 2 hydroxyl groups"

    # Check if the molecule has a linear chain of 12 carbon atoms
    sssr = Chem.GetSymmSSSR(mol)
    ring_count = len(sssr)
    if ring_count > 0:
        return False, "Molecule contains rings"

    # Check if the hydroxy groups are attached to the carbon chain
    atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'C']
    carbon_chain = []
    for atom in atoms:
        neighbors = [neighbor.GetSymbol() for neighbor in atom.GetNeighbors()]
        if 'O' in neighbors:
            carbon_chain.append(True)
        else:
            carbon_chain.append(False)

    if sum(carbon_chain) != 2:
        return False, "Hydroxy groups are not attached to the carbon chain"

    return True, "Molecule is a dodecanediol"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:195615',
                          'name': 'dodecanediol',
                          'definition': 'A diol that is dodecane carrying two '
                                        'hydroxy groups at unspecified '
                                        'positions.',
                          'parents': [   'CHEBI:23824',
                                         'CHEBI:24026',
                                         'CHEBI:50584']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.02631578947368421 is too low.\n'
               "True positives: [('CCCC(O)CCCCCCCCO', 'Molecule is a "
               "dodecanediol')]\n"
               "False positives: [('OC(CC#CC#CC#CCO)C(O)=O', 'Molecule is a "
               "dodecanediol'), ('OC(CCCCCCCO)CC(O)=O', 'Molecule is a "
               "dodecanediol'), ('O=C(O)CNCP(=O)(O)O.NC(C)C', 'Molecule is a "
               "dodecanediol'), ('N[C@@H](CCC(O)=O)C(=O)OP(O)(O)=O', 'Molecule "
               "is a dodecanediol'), "
               "('O=C/C(=C/C=C/C)/[C@@H](O)[C@@H](O)/C=C\\\\C', 'Molecule is a "
               "dodecanediol'), "
               "('[NH3+][C@@H](CCC(=O)OP([O-])([O-])=O)C([O-])=O', 'Molecule "
               "is a dodecanediol'), ('COC(=O)C=C(C)OP(=O)(OC)OC', 'Molecule "
               "is a dodecanediol'), ('O[C@]([C@H](O)C(O)=O)(CC(O)=O)C(O)=O', "
               "'Molecule is a dodecanediol'), ('CC(C)CCCCCCOS(O)(=O)=O', "
               "'Molecule is a dodecanediol'), ('CS(=O)(=O)OCCCCOS(C)(=O)=O', "
               "'Molecule is a dodecanediol'), "
               "('O=C(O)C[C@H](O)C[C@H](O)CCCCC', 'Molecule is a "
               "dodecanediol'), ('CC(C)CCC[C@@H](C)COS([O-])(=O)=O', 'Molecule "
               "is a dodecanediol'), ('CC[C@@H](CO)NCCN[C@@H](CC)CO', "
               "'Molecule is a dodecanediol'), ('COP(=S)(OC)SCC(=O)N(C)C=O', "
               "'Molecule is a dodecanediol'), "
               "('[H]C(OP([O-])([O-])=O)=C(O)C(=O)CCSC', 'Molecule is a "
               "dodecanediol'), ('OCCCCCCC[C@@H](O)CC(O)=O', 'Molecule is a "
               "dodecanediol'), "
               "('C(C(=O)NP([O-])(=O)[O-])C[C@@H](C(=O)[O-])[NH3+]', 'Molecule "
               "is a dodecanediol'), "
               "('C(=O)([C@@H](N)CO)N[C@H](C(=O)O)[C@@H](C)O', 'Molecule is a "
               "dodecanediol'), ('[H]C(OP(O)(O)=O)=C(O)C(=O)CCSC', 'Molecule "
               "is a dodecanediol'), ('CC[C@H](CO)NCCN[C@H](CC)CO', 'Molecule "
               "is a dodecanediol'), ('CCOP(=S)(OCC)SCCSCC', 'Molecule is a "
               "dodecanediol'), ('OC(C(NC(=O)C(N)CO)C(O)=O)C', 'Molecule is a "
               "dodecanediol'), ('O=C(O)/C=C/C=C/CCC[C@H](O)CO', 'Molecule is "
               "a dodecanediol'), ('O(CCCCCCCCC)S([O-])(=O)=O', 'Molecule is a "
               "dodecanediol'), ('P(OC(=O)[C@@H](N)CCCCN)(O)(O)=O', 'Molecule "
               "is a dodecanediol'), ('ClC/C(=C\\\\CO)/CC[C@H](OC)C(=C)C', "
               "'Molecule is a dodecanediol'), "
               "('C[C@@H](O)CCCCC[C@@H](O)CC(O)=O', 'Molecule is a "
               "dodecanediol'), ('NC(CCC(=O)OP(O)(O)=O)C(O)=O', 'Molecule is a "
               "dodecanediol'), ('CC(C)CCC[C@@H](C)COS(O)(=O)=O', 'Molecule is "
               "a dodecanediol'), ('CCOP(=O)(OCC)SCCSCC', 'Molecule is a "
               "dodecanediol'), ('N[C@@H](CCC(=O)OP(O)(O)=O)C(O)=O', 'Molecule "
               "is a dodecanediol'), ('OC(CCCCC)CC(O)CC(O)=O', 'Molecule is a "
               "dodecanediol'), ('CC(C)CCCC(C)COS(O)(=O)=O', 'Molecule is a "
               "dodecanediol'), ('OC(C(O)C(O)=O)C#CCCCCC', 'Molecule is a "
               "dodecanediol'), ('OC(CCCCC/C=C/C(O)=O)CO', 'Molecule is a "
               "dodecanediol'), ('OC(=O)CN(CC(O)=O)CP(O)(O)=O', 'Molecule is a "
               "dodecanediol'), ('C(CCCC(=O)NO)CCC(=O)NO', 'Molecule is a "
               "dodecanediol'), ('CNC(=O)\\\\C=C(/C)OP(=O)(OC)OC', 'Molecule "
               "is a dodecanediol'), ('O=C(O)[C@@H](N(O)O)CCCCCSC', 'Molecule "
               "is a dodecanediol'), ('O=C(/C=C/C=C/C)C[C@@H](OC)CCO', "
               "'Molecule is a dodecanediol'), "
               "('N[C@H](CCC(=O)OP(O)(O)=O)C(O)=O', 'Molecule is a "
               "dodecanediol'), ('CCS(=O)(=O)CCSP(=O)(OC)OC', 'Molecule is a "
               "dodecanediol'), ('CCC(CO)NCCNC(CC)CO', 'Molecule is a "
               "dodecanediol'), ('C(C(=O)NP(O)(=O)O)C[C@@H](C(=O)O)N', "
               "'Molecule is a dodecanediol'), "
               "('C(C[NH3+])CCC[NH2+]CC([C@@H](CO)O)=O', 'Molecule is a "
               "dodecanediol'), ('CC(C)CCCC(C)COS([O-])(=O)=O', 'Molecule is a "
               "dodecanediol'), ('NC(CCC(O)=O)C(=O)OP(O)(O)=O', 'Molecule is a "
               "dodecanediol'), "
               "('[H]C([H])(C=O)[C@](C)([N+]([O-])=O)[C@@]([H])(OC)[C@]([H])(C)O', "
               "'Molecule is a dodecanediol'), "
               "('C[C@@H](O)[C@H]([NH3+])C(=O)N[C@@H](CO)C([O-])=O', 'Molecule "
               "is a dodecanediol'), ('O=C(O)CC/C=C/[C@H](O)CC[C@H](O)C', "
               "'Molecule is a dodecanediol'), ('CSCCCCCC(N(O)O)C(O)=O', "
               "'Molecule is a dodecanediol'), ('OC(C(O)C(OCC)=O)C(OCC)=O', "
               "'Molecule is a dodecanediol'), "
               "('O.OC(=O)CC(O)(CC(O)=O)C(O)=O', 'Molecule is a "
               "dodecanediol'), ('COC(=O)C(\\\\C)=C\\\\OP(=S)(OC)OC', "
               "'Molecule is a dodecanediol'), "
               "('OC(C(O)C(O)=O)(CC(O)=O)C(O)=O', 'Molecule is a "
               "dodecanediol'), ('OC(C(N)C(=O)NC(CO)C(O)=O)C', 'Molecule is a "
               "dodecanediol'), "
               "('[NH3+][C@@H](CCC([O-])=O)C(=O)OP([O-])([O-])=O', 'Molecule "
               "is a dodecanediol'), ('O=C(O)C=CNC(=O)[C@H](O)C(O)(C)C', "
               "'Molecule is a dodecanediol'), "
               "('ClC/C(=C\\\\COC)/CC[C@H](O)C(=C)C', 'Molecule is a "
               "dodecanediol'), ('CCS(=O)CC(C)SP(=O)(OC)OC', 'Molecule is a "
               "dodecanediol'), ('C[C@@H](O)[C@H](N)C(=O)N[C@@H](CO)C(O)=O', "
               "'Molecule is a dodecanediol'), ('CC(C)CCCCCCOS([O-])(=O)=O', "
               "'Molecule is a dodecanediol'), ('CSCCCCCC(N(O)O)C([O-])=O', "
               "'Molecule is a dodecanediol'), "
               "('[H+].[H+].NCCS.OC(C(O)C([O-])=O)C([O-])=O', 'Molecule is a "
               "dodecanediol'), ('N[C@H](CCC(O)=O)C(=O)OP(O)(O)=O', 'Molecule "
               "is a dodecanediol'), ('O(C(OC)CCCCCCCCC)C', 'Molecule is a "
               "dodecanediol'), ('O(CCC(C)C)C(OCCC(C)C)C', 'Molecule is a "
               "dodecanediol'), "
               "('C[C@@H](O)[C@H](NC(=O)[C@@H]([NH3+])CO)C([O-])=O', 'Molecule "
               "is a dodecanediol'), ('O=C([O-])[C@@H](N(O)O)CCCCCSC', "
               "'Molecule is a dodecanediol'), "
               "('CC(C)CCC[C@H](C)COS([O-])(=O)=O', 'Molecule is a "
               "dodecanediol'), ('O(C(C=C(CCC=C(C)C)C)OC)C', 'Molecule is a "
               "dodecanediol'), ('O=C(O)\\\\C=C/C=C/[C@H](O)CC[C@H](O)C', "
               "'Molecule is a dodecanediol'), "
               "('CC(C)CCC[C@H](C)COS(O)(=O)=O', 'Molecule is a "
               "dodecanediol'), ('CCC(C)(O)C#CC#CC(C)(O)CC', 'Molecule is a "
               "dodecanediol')]\n"
               'False negatives: []',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 21,
    'num_true_negatives': 183903,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.045454545454545456,
    'recall': 1.0,
    'f1': 0.08695652173913045,
    'accuracy': 0.9998858230256898}