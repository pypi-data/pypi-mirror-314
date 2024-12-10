"""
Classifies: CHEBI:26282 propanals
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_propanals(smiles: str):
    """
    Determines if a molecule is a propanal or a derivative thereof.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a propanal or derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find the aldehyde carbon
    aldehyde_carbon = None
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetTotalNumHs() == 1 and sum(bond.GetBondTypeAsDouble() for bond in atom.GetBonds()) == 3:
            aldehyde_carbon = atom.GetIdx()
            break

    if aldehyde_carbon is None:
        return False, "No aldehyde group found"

    # Check if the aldehyde carbon is part of a propanal skeleton
    propanal_skeleton = False
    for bond in mol.GetAtomWithIdx(aldehyde_carbon).GetBonds():
        neighbor = bond.GetOtherAtom(mol.GetAtomWithIdx(aldehyde_carbon))
        if neighbor.GetSymbol() == 'C':
            path = Chem.GetShortestPath(mol, neighbor.GetIdx(), aldehyde_carbon)
            if len(path) == 2:  # Propanal skeleton has two carbon atoms between the aldehyde and the end of the chain
                propanal_skeleton = True
                break

    if not propanal_skeleton:
        return False, "Molecule does not contain a propanal skeleton"

    # Get the substituents
    substituents = []
    for bond in mol.GetAtomWithIdx(aldehyde_carbon).GetBonds():
        neighbor = bond.GetOtherAtom(mol.GetAtomWithIdx(aldehyde_carbon))
        if neighbor.GetSymbol() != 'H' and neighbor.GetSymbol() != 'C':
            substituents.append(neighbor.GetSymbol())

    if len(substituents) > 0:
        return True, f"Propanal derivative with substituents: {', '.join(set(substituents))}"
    else:
        return True, "Unsubstituted propanal"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26282',
                          'name': 'propanals',
                          'definition': 'An aldehyde based on a propanal '
                                        'skeleton and its derivatives.',
                          'parents': ['CHEBI:17478']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'True positives: []\n'
               "False positives: [('CCCCCCCCCCCC[C@@H](O)C(O)=O', 'Propanal "
               "derivative with substituents: O'), "
               "('O(C(CCOC(=O)C(C)=C)C)C(=O)C(C)=C', 'Propanal derivative with "
               "substituents: O'), ('ClC=1N=C(N)C(F)=CN1', 'Propanal "
               "derivative with substituents: N'), "
               "('OC(CCCCCCCCCCCCCCC)CC(=O)NCC(O)=O', 'Propanal derivative "
               "with substituents: O'), ('O=C1OCC2=C1C=C(OC)C(=C2O)O', "
               "'Unsubstituted propanal'), ('CCC=S=O', 'Propanal derivative "
               "with substituents: S'), "
               "('O=C([C@@]1(O)[C@]2(C(C)(C)CC1)CC=C(CO)CC2)C', 'Unsubstituted "
               "propanal'), ('C(*C1CS1)#N', 'Propanal derivative with "
               "substituents: *, S'), "
               "('O(N1C(=O)CCC1=O)C(=O)C(NC(=O)C)CCCCNC(=O)C', 'Propanal "
               "derivative with substituents: N'), "
               "('O=C(O)C(O)(CC(=O)O)CC(=O)N[C@H](C(=O)O)CCCCN(O)C(=O)CCCCCCC', "
               "'Propanal derivative with substituents: N'), "
               "('O(C(=O)CCCCCCCCCCCCCCCCCCCCC)C[C@@H](O)CO', 'Propanal "
               "derivative with substituents: O'), ('C1(CCCC1)CC', "
               "'Unsubstituted propanal'), ('[O-][N+](=O)c1cnc(s1)N1CCNC1=O', "
               "'Propanal derivative with substituents: N'), "
               "('O1C(=C(C=C1CCC(O)=O)C)CCC(O)=O', 'Unsubstituted propanal'), "
               "('OC(C[C@@H](C(=O)O)CCCCC)=O', 'Unsubstituted propanal'), "
               "('C(*)(=O)[C@H](N*)CCC(=O)O', 'Propanal derivative with "
               "substituents: N'), ('O=C(C=1N2C(CCC2)=C(C1C)C)C(O)C', "
               "'Propanal derivative with substituents: O'), "
               "('OC(=O)CCCCCC(CCCCC)CC', 'Unsubstituted propanal'), "
               "('OC(=O)C1=CCNCC1', 'Unsubstituted propanal'), "
               "('Cl/C(/C(O)=O)=C\\\\Cl', 'Propanal derivative with "
               "substituents: Cl'), "
               "('O=C1O[C@@H](C(=O)O)[C@]([C@@]1(O)CCCCCCCCCCCC)(O)C(=O)O', "
               "'Propanal derivative with substituents: O'), "
               "('CC1=C2C(=C(C(=C1Cl)O)Cl)OC3=C(C(=C(C=C3OC2=O)OC)C(=O)OC)C', "
               "'Unsubstituted propanal'), "
               "('C([C@@H](CC([O-])=O)OC(=O)*C([O-])=O)[N+](C)(C)C', 'Propanal "
               "derivative with substituents: O'), ('S(SCC)C(C)C', 'Propanal "
               "derivative with substituents: S'), "
               "('CC(=C)[C@@H](CCC(C)=O)CC([O-])=O', 'Unsubstituted "
               "propanal'), ('[NH3+]CCCC[NH2+]CCCC[C@H](N-*)C(-*)=O', "
               "'Propanal derivative with substituents: N'), "
               "('C(=O)(O)[C@@H](N)C(C)(C)O', 'Propanal derivative with "
               "substituents: N'), ('O=C1CCC(C1)C#N', 'Unsubstituted "
               "propanal'), ('S1C(C(NC1)C(O)=O)(C)C', 'Propanal derivative "
               "with substituents: N'), ('P(=O)(O)(O)[C@H](O)CNC(=O)C', "
               "'Propanal derivative with substituents: O, P'), "
               "('C[N+](C)(C)CCOP([O-])(=O)OC[C@@H](CO[*])OC([*])=O', "
               "'Propanal derivative with substituents: O'), "
               "('CC(=O)[C@H]([NH3+])C([O-])=O', 'Propanal derivative with "
               "substituents: N'), ('OC(=O)C1CSSC1', 'Unsubstituted "
               "propanal'), ('O[C@H](CO[*])COP([O-])(=O)O[*]', 'Propanal "
               "derivative with substituents: O'), "
               "('C1COCCN1CCNC(=O)CC2=CC(=O)NC(=O)N2', 'Unsubstituted "
               "propanal'), ('C[C@@H](N)C([O-])=O', 'Propanal derivative with "
               "substituents: N'), ('O(*)C[C@@H](CO*)OC(*)=O', 'Propanal "
               "derivative with substituents: O'), "
               "('P1(O[C@H](COC(=O)CCCCCCCCCCCCCCC)CO1)(O)=O', 'Propanal "
               "derivative with substituents: O'), "
               "('NC(=O)N[C@H]([*])C([O-])=O', 'Propanal derivative with "
               "substituents: *, N'), ('[*]CCC=O', 'Propanal derivative with "
               "substituents: O'), ('[NH3+][C@@H](CCCCNO)C([O-])=O', 'Propanal "
               "derivative with substituents: N'), ('O(C(OC)CCCCCCCC)C', "
               "'Propanal derivative with substituents: O'), "
               "('N(C(C(NCCCCNCCCN)=O)O)C(CCCCCCNC(=N)N)=O', 'Propanal "
               "derivative with substituents: O, N'), "
               "('C(N/C(=[NH+]/C)/NC)CC[C@@H](C(=O)[O-])[NH3+]', 'Propanal "
               "derivative with substituents: N'), "
               "('CCCCCCCCCCCCCCCCCc1oc(=O)cc(O)c1C', 'Unsubstituted "
               "propanal'), ('NC(=O)CC[C@H]([NH3+])C(O)=O', 'Propanal "
               "derivative with substituents: N'), "
               "('O=C1NC=2C(=O)C=3NC(=O)C=C(C3C(C2C(=C1C)CCCCC)=O)CCC', "
               "'Unsubstituted propanal'), ('O=C([O-])[C@@H](NO)CCCCCCCSC', "
               "'Propanal derivative with substituents: N'), "
               "('O1C2=C(OC)C(O)=CC(=C2OC1)C', 'Unsubstituted propanal'), "
               "('O=C(NCC(O)=O)[C@@H](NC(=O)CN)CC(=O)N', 'Propanal derivative "
               "with substituents: N'), "
               "('C([C@@](COC(=O)CCCCCCCCCCCCCCCCC)(OC(=O)CCCCCCCCCCCCCCCCC)[H])OC(*)=O', "
               "'Propanal derivative with substituents: O'), "
               "('OC(=O)C1NC(=NCC1)C', 'Propanal derivative with substituents: "
               "N'), ('O(CCCCCCCCCCCC)C(=O)C(N(C)C)C', 'Propanal derivative "
               "with substituents: N'), "
               "('CCCCCCCC(=O)O[C@H](COC([*])=O)COP([O-])(=O)OCC[NH3+]', "
               "'Propanal derivative with substituents: O'), "
               "('O[C@@H](CS(O)(=O)=O)C(O)=O', 'Propanal derivative with "
               "substituents: O'), ('C1(O)=C(C)[NH+]=CC(CO)=C1C[NH3+]', "
               "'Propanal derivative with substituents: N'), "
               "('CCCC(O)CCCCCCCCCC([O-])=O', 'Propanal derivative with "
               "substituents: O'), ('O[C@@H](C(O)=O)C(=O)C(O)=O', 'Propanal "
               "derivative with substituents: O'), "
               "('O(CC(COC(CC)=O)OC(=O)CC)C(CC)=O', 'Propanal derivative with "
               "substituents: O'), ('O=C1NC2C(=O)NC(=O)N=C2N1', 'Propanal "
               "derivative with substituents: N'), "
               "('CCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCCCCCCC', "
               "'Propanal derivative with substituents: O'), ('O=C1CCC(=C1)C', "
               "'Unsubstituted propanal'), "
               "('O(C(=O)CCCCCCCCCCCCCC)[C@H](COC(=O)CCCCCCCCCCCC)CO', "
               "'Propanal derivative with substituents: O'), "
               "('CCCCCCCCCCCCC(O)CO', 'Propanal derivative with substituents: "
               "O'), "
               "('CCCCCCCCCCCCCCCC(=O)OC[C@H](COP([O-])([O-])=O)OC(=O)CCCCCCCCCCCCCCC', "
               "'Propanal derivative with substituents: O'), "
               "('O=C1C(=C)[C@]2([C@@H]3[C@@](O)(CC(C3)(C)C)C[C@@]2(C1)OC)C', "
               "'Unsubstituted propanal'), "
               "('C[N+](C)(C)CCOP([O-])(=O)OC[C@@H](COC([*])=O)OC([*])=O', "
               "'Propanal derivative with substituents: O'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)CCCC)CO)([O-])=O', 'Propanal "
               "derivative with substituents: O'), ('O=C1NC(=CC(=C1C#N)C)C', "
               "'Unsubstituted propanal'), "
               "('O=C1C(O)=C2OC(O)=C(O)C3=C2C(=C1C)C=4O[C@H](C)C(C4C3=O)(C)C', "
               "'Propanal derivative with substituents: O'), "
               "('S(=O)(CCCCNC(SCC(N)C(=O)NCC(O)=O)=S)C', 'Propanal derivative "
               "with substituents: N'), ('[O-]C(=O)[C@@H]1CCCC(=N1)C([O-])=O', "
               "'Propanal derivative with substituents: N'), "
               "('C[C@@H]1CCC[NH2+]1', 'Propanal derivative with substituents: "
               "N'), ('N[C@@H](CNC(=O)COP(O)(O)=O)C(O)=O', 'Propanal "
               "derivative with substituents: N'), "
               "('O=C([O-])[C@@H](N(O)O)CCCCCCSC', 'Propanal derivative with "
               "substituents: N'), ('O=C1NC(=O)NC=C1[N+]#N', 'Propanal "
               "derivative with substituents: N'), ('O=C(C(CCCC)CC)CC(=O)CCC', "
               "'Unsubstituted propanal'), ('O1C([C@H](CC1)NC(=O)*)=O', "
               "'Propanal derivative with substituents: N'), "
               "('CCCCCCCCCCC(O)CCCCCCCCC', 'Propanal derivative with "
               "substituents: O'), ('NC(CCCCNCCC(O)=O)C(O)=O', 'Propanal "
               "derivative with substituents: N'), "
               "('C1(=C(O/C(/C1=O)=C/C)C)O', 'Unsubstituted propanal'), "
               "('C(CCCCC)(OC[C@@H](C(*)=O)N*)=O', 'Propanal derivative with "
               "substituents: N'), ('N[C@@H](CCCNC(N)=N)C([O-])=O', 'Propanal "
               "derivative with substituents: N'), ('OC(CCCCCCCC)CO', "
               "'Propanal derivative with substituents: O'), "
               "('CCC(=O)N1CCCC1C(O)=O', 'Propanal derivative with "
               "substituents: N'), ('CCC1CO1', 'Propanal derivative with "
               "substituents: O'), ('C[C@H](O)CCO', 'Propanal derivative with "
               "substituents: O'), ('*C(OCC(CO)O*)=O', 'Propanal derivative "
               "with substituents: O'), ('OC(CCCCC(O)=O)CCO', 'Propanal "
               "derivative with substituents: O'), "
               "('OC(=O)[C@@H](N)CCCCN.OC(=O)CCC', 'Propanal derivative with "
               "substituents: N'), "
               "('P(OCC[N+](C)(C)C)(OC[C@H](OC(=O)C)COC)([O-])=O', 'Propanal "
               "derivative with substituents: O'), "
               "('P(OC[C@H](O)COC(=O)CCCCCCCCCCCCCCCCCC)(O)(O)=O', 'Propanal "
               "derivative with substituents: O'), ('CSCCCCCC(N(O)O)C(O)=O', "
               "'Propanal derivative with substituents: N'), "
               "('OC(=O)[C@@H](N)CC[S@](=O)C', 'Propanal derivative with "
               "substituents: N'), ('C([C@@H](C(*)=O)N*)[Se-]', 'Propanal "
               "derivative with substituents: N'), ('O=C(CCC(C)C)CC', "
               "'Unsubstituted propanal'), ('Cl.Cc1ncc(n1CCO)[N+]([O-])=O', "
               "'Propanal derivative with substituents: N'), "
               "('N1=C(CCC)C(=NC(=C1)C)C', 'Propanal derivative with "
               "substituents: N'), "
               "('[C@](COCCCCCCCCCC)(OCCCCCCCCCC)([H])COP(OCC[N+](C)(C)C)(=O)[O-]', "
               "'Propanal derivative with substituents: O'), "
               "('C1CN2CCC1C(=O)C2(CO)CO', 'Unsubstituted propanal')]\n"
               "False negatives: [('OC(CS(O)(=O)=O)C=O', 'Molecule does not "
               "contain exactly one aldehyde group')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 3,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.038461538461538464}