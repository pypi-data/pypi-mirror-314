"""
Classifies: CHEBI:33551 organosulfonic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_organosulfonic_acid(smiles: str):
    """
    Determines if a molecule is an organosulfonic acid (an organic derivative of sulfonic acid
    where the sulfo group is linked directly to carbon).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an organosulfonic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all sulfonic acid groups in the molecule
    sulfonic_acid_groups = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'S' and atom.GetExplicitValence() == 6:
            attached_to_organic = False
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'C':
                    attached_to_organic = True
                    break
            if attached_to_organic:
                sulfonic_acid_groups.append(atom.GetIdx())

    if not sulfonic_acid_groups:
        return False, "No sulfonic acid groups found"

    # Check if at least one sulfonic acid group is attached to carbon
    for idx in sulfonic_acid_groups:
        atom = mol.GetAtomWithIdx(idx)
        attached_to_carbon = False
        for neighbor in atom.GetNeighbors():
            if neighbor.GetSymbol() == 'C':
                if mol.GetBondBetweenAtoms(atom.GetIdx(), neighbor.GetIdx()).GetIsAromatic() or \
                   mol.GetBondBetweenAtoms(atom.GetIdx(), neighbor.GetIdx()).GetBondType() == Chem.BondType.SINGLE:
                    attached_to_carbon = True
                    break
        if attached_to_carbon:
            return True, "Molecule is an organosulfonic acid"

    return False, "Sulfonic acid group not attached to carbon in an organic molecule"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33551',
                          'name': 'organosulfonic acid',
                          'definition': 'An organic derivative of sulfonic '
                                        'acid in which the sulfo group is '
                                        'linked directly to carbon.',
                          'parents': [   'CHEBI:33261',
                                         'CHEBI:33552',
                                         'CHEBI:64709']},
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
               "False positives: [('CCC=S=O', 'Molecule is an organosulfonic "
               "acid'), ('O=S(CC1C(C1c1ccccc1)c1ccccc1)c1ccccc1', 'Molecule is "
               "an organosulfonic acid'), ('S(S/C=C\\\\C)(=O)CCC', 'Molecule "
               "is an organosulfonic acid'), "
               "('CC(C)(C)S(=O)N1CC2=CC(=NC(=C2[C@@H]1CCO)C3=CC=CC(=C3)C4=CC(=CC=C4)F)C(=O)NCCCN5CCOCC5', "
               "'Molecule is an organosulfonic acid'), "
               "('CC(C)(C)[S@](=O)N1CC2=CC(=NC(=C2[C@@H]1CCO)C3=CC=CC(=C3)C4=CC=C(C=C4)C(=O)N(C)C)C(=O)NC5CCCC5', "
               "'Molecule is an organosulfonic acid'), "
               "('CC(C)(C)[S@@](=O)N1CC2=CC(=NC(=C2[C@H]1CCO)C3=CC=CC(=C3)C4=CC=NC=C4)C(=O)NCC5=CC=NC=C5', "
               "'Molecule is an organosulfonic acid'), "
               "('[S@](=O)(C=1C2=NC=C(O)C3=C2N(C=4C=CC=CC34)C(C1)=O)C', "
               "'Molecule is an organosulfonic acid'), "
               "('S(=O)(CCCCNC(SCC(N)C(=O)NCC(O)=O)=S)C', 'Molecule is an "
               "organosulfonic acid'), ('NCCS([O-])=O', 'Molecule is an "
               "organosulfonic acid'), "
               "('S(C=1C=CC(C2=NC(C=3C=CN=CC3)=C(N2)C4=CC=C(C=C4)F)=CC1)(C)=O', "
               "'Molecule is an organosulfonic acid'), "
               "('OC(=O)[C@@H](N)CC[S@](=O)C', 'Molecule is an organosulfonic "
               "acid'), ('S(CCC(=O)[O-])([O-])=O', 'Molecule is an "
               "organosulfonic acid'), "
               "('CCC[S@@](=O)c1ccc2[nH]c(NC(=O)OC)nc2c1', 'Molecule is an "
               "organosulfonic acid'), "
               "('S(=O)(CC[C@@H]1NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@]2(N(CCC2)C1=O)[H])CC3=CC=CC=C3)CC4=CC=CC=C4)CC=5C=6C(NC5)=CC=CC6)C(C)C)CCSC)CC(C)C)C', "
               "'Molecule is an organosulfonic acid'), "
               "('S(=O)(CCC(NC(=S)C(NC(=O)C(=O)C)C(C)C)C(=S)NC(C(=O)NC(C(=S)NC(C(=S)NC(C(=O)NC1C(=O)NC(C(=O)NC(C(=O)NC(CC2=CC=CC=C2)C(NC(C(NC=CSC1C)=O)C(O)C=3N(C=[N+](C3)C)C)=O)C)C(C)C)C)C)C)C)C', "
               "'Molecule is an organosulfonic acid'), "
               "('CC(C)(C)[S@](=O)N1CC2=CC(=NC(=C2[C@@H]1CCO)C3=CC=CC(=C3)C4=CC=C(C=C4)C#N)C(=O)NCC5=CC(=CC=C5)OC', "
               "'Molecule is an organosulfonic acid'), "
               "('S(O)(=O)C=1C=C2OC(C(O)CC2=C(O)C1[O-])C3=CC(OS(O)(=O)=O)=C(OC)C=C3', "
               "'Molecule is an organosulfonic acid'), "
               "('CC(C)(C)[S@](=O)N1CC2=CC(=NC(=C2[C@@H]1CCO)C3=CC=CC(=C3)C4=CC=C(C=C4)F)C(=O)N5CCCCC5', "
               "'Molecule is an organosulfonic acid'), "
               "('[S@@](=O)(CCC(C=1C2=C(C=CC=C2)NC1)C=3C4=C(C=CC=C4)NC3)C', "
               "'Molecule is an organosulfonic acid'), "
               "('S(=O)(CCC(NC(=O)NC(C(=O)O)CC=1C2=C(C=CC=C2)NC1)C(=O)NC(C(=O)N/C=C\\\\3/OC(N4C(=O)NC(=O)C=C4)C(C3)O)C(N(C(=O)C(N)CC5=CC(O)=CC=C5)C)C)C', "
               "'Molecule is an organosulfonic acid'), "
               "('S(=O)=C(N)/C=C/CCCCCCCCCCC(C)C', 'Molecule is an "
               "organosulfonic acid'), "
               "('S(=O)(CC1=NC=C(C(OC)=C1CO)C)C=2NC3=C(N2)C=CC(OC)=C3', "
               "'Molecule is an organosulfonic acid'), ('S(=O)(C(SSCCC)CC)C', "
               "'Molecule is an organosulfonic acid'), "
               "('CC(C)(C)[S@](=O)N1CC2=CC(=NC(=C2[C@@H]1CCO)C3=CC=CC(=C3)C4=CC=NC=C4)C(=O)N5CCC6=CC=CC=C6C5', "
               "'Molecule is an organosulfonic acid'), "
               "('S(CC1=C(C)C(OC)=CC=N1)(=O)C2=NC3=C(N2)C=CC(=C3)N4C=CC=C4', "
               "'Molecule is an organosulfonic acid'), "
               "('ClC1=CC=2C(=NC(C=3SC=C(N3)C=4N(C(=C([S@@](=O)C)C(C4OC)=O)C(=O)NCCO)C)=CC2)C=C1', "
               "'Molecule is an organosulfonic acid'), "
               "('[S@@](=O)(C[S@](=O)C)C[C@@H](NC(=O)/C=C/C=1C(=O)NC(=O)NC1C)CO', "
               "'Molecule is an organosulfonic acid'), "
               "('S(O)(=O)C=1C=2CC(O)C(OC2C=C(O)C1)C3=CC(O)=C(OC)C=C3', "
               "'Molecule is an organosulfonic acid'), "
               "('CC(C)(C)[S@@](=O)N1CC2=CC(=NC(=C2[C@H]1CCO)C3=CC=CC(=C3)C4=CC=CC(=C4)C#N)C(=O)NCCN5CCCCC5', "
               "'Molecule is an organosulfonic acid'), "
               "('C=12C=CC(=CC1N=C(N2)NC(OC)=O)[S@](CCC)=O', 'Molecule is an "
               "organosulfonic acid'), "
               "('CCOC(=O)C1=NC(=C2[C@H](N(CC2=C1)S(=O)C(C)(C)C)CCO)C3=CC=CC(=C3)C4=CC(=CC=C4)OC', "
               "'Molecule is an organosulfonic acid'), "
               "('S(=O)(C1=CC=CC=C1)CCC2C(=O)N(C3=CC=C(O)C=C3)N(C2=O)C4=CC=CC=C4', "
               "'Molecule is an organosulfonic acid'), "
               "('S(=O)(CC[C@@H]1NC(=O)[C@@H]2CCCN2C1=O)C', 'Molecule is an "
               "organosulfonic acid'), "
               "('CC1=CC=C(C=C1)C2=NC(=C(O2)C)CS(=O)CC(=O)NCCN(CC(C)C)CC(C)C', "
               "'Molecule is an organosulfonic acid'), "
               "('CC(C)(C)[S@@](=O)N1CC2=CC(=NC(=C2[C@H]1CCO)C3=CC=CC(=C3)C4=CC=C(C=C4)C#N)C(=O)NCC5=CC(=CC=C5)OC', "
               "'Molecule is an organosulfonic acid'), "
               "('C(*)(=O)[C@@H](N*)CC[S@@](=O)C', 'Molecule is an "
               "organosulfonic acid'), "
               "('S1(=O)C(SC)C2N(C(=O)C(NC(=O)C(NC(=O)C3=NC=4C(=CC=CC4)C=C3O)COC(C5(N(C(C(C1)N(C(=O)C(NC(=O)C(NC(=O)C6=NC=7C(=CC=CC7)C=C6O)COC(C8(N(C2=O)C)C(C)C8)=O)C)C)=O)C)C(C)C5)=O)C)C', "
               "'Molecule is an organosulfonic acid'), "
               "('CC(C)(C)S(=O)N1CC2=CC(=NC(=C2[C@@H]1CCO)C3=CC=CC(=C3)C#CCN(C)C)C(=O)NCCCN4CCOCC4', "
               "'Molecule is an organosulfonic acid'), "
               "('CNCCCN1C2=CC=CC=C2S(=O)C3=C1C=C(C=C3)Cl', 'Molecule is an "
               "organosulfonic acid'), "
               "('[S@@](=O)(C1=C(OC)C=2C(=CC=CC2)C(=C1)OC)C', 'Molecule is an "
               "organosulfonic acid'), "
               "('CC(C)(C)[S@](=O)N1CC2=CC(=NC(=C2[C@@H]1CCO)C3=CC=CC(=C3)C4=CC=NC=C4)C(=O)NCCC5=CC=NC=C5', "
               "'Molecule is an organosulfonic acid'), "
               "('[C@H]1(O[C@@H]([C@@H](O)[C@@H]([C@H]1O)O)CO)S/C(=N\\\\OS([O-])(=O)=O)/CCCCS(C)=O', "
               "'Molecule is an organosulfonic acid'), "
               "('CCCNC(=O)C1=NC(=C2[C@@H](N(CC2=C1)[S@@](=O)C(C)(C)C)CCO)C3=CC=CC(=C3)C4=CC(=CC=C4)OC', "
               "'Molecule is an organosulfonic acid'), "
               "('C1(=CC=CC=C1O)C2=CC=CC=C2S([O-])=O', 'Molecule is an "
               "organosulfonic acid'), "
               "('S(=O)(CC(N\\\\C=C/1\\\\OCC(O)C(O)C1O)C(O)=O)/C=C/C', "
               "'Molecule is an organosulfonic acid'), "
               "('CS(=O)CCCC(S[C@@H]1O[C@H](CO)[C@@H](O)[C@H](O)[C@H]1O)=NOS([O-])(=O)=O', "
               "'Molecule is an organosulfonic acid'), "
               "('CC(C)(C)[S@@](=O)N1CC2=CC(=NC(=C2[C@H]1CCO)C3=CC=CC(=C3)C4=CC(=CC=C4)F)C(=O)NCCOC', "
               "'Molecule is an organosulfonic acid'), "
               "('S1(=O)C(C(NC(=S)C(NC(=O)C=2N=C(C(NC(=O)C)C)SC2)CC=3NC=NC3)C(=O)N[C@@H]4C(=O)NC5C(=O)NC(=C)C(N[C@@H](C(N6[C@@H](C(NC(C1)C(=O)NC(C(=O)NC(C(=O)NC(C(=O)O)CC(NC(C(C4)C)=O)=O)C)CS(=O)C5)=O)CCC6)=O)CC(C)C)=O)C', "
               "'Molecule is an organosulfonic acid'), "
               "('C1=CC=C2C(=C1)N(C3=C(S2=O)C=CC(=C3)Cl)CCCN', 'Molecule is an "
               "organosulfonic acid'), "
               "('C1=CC=C2C(=C1)C(=O)N(S2=O)C3=CC(=CC=C3)F', 'Molecule is an "
               "organosulfonic acid'), ('C(CCCCS(C)=O)#N', 'Molecule is an "
               "organosulfonic acid'), "
               "('S1(=O)C2C(C(=O)C3=C(O)C=C(O)C=C3CC(=O)O[C@H](CCC2)C)C(C1)(O)C(=O)O', "
               "'Molecule is an organosulfonic acid'), "
               "('CC=CC1=CC=CC(=C1)C2=C3[C@@H](N(CC3=CC(=N2)C(=O)NCC4=CC=CC=N4)[S@@](=O)C(C)(C)C)CCO', "
               "'Molecule is an organosulfonic acid'), "
               "('[H][C@]12Cc3c([nH]c4cc(O)ccc34)[S@](=O)C[C@]([H])(NC(=O)CNC(=O)[C@@]([H])(NC(=O)CNC1=O)[C@@H](C)CC)C(=O)N[C@@H](CC(N)=O)C(=O)N1C[C@H](O)C[C@@]1([H])C(=O)N[C@@]([H])([C@@H](C)[C@@H](O)CO)C(=O)N2', "
               "'Molecule is an organosulfonic acid'), ('CS(=O)c1ccc(O)cc1', "
               "'Molecule is an organosulfonic acid'), ('[NH3+]CCS([O-])=O', "
               "'Molecule is an organosulfonic acid'), "
               "('CC(C)(C)[S@@](=O)N1CC2=CC(=NC(=C2[C@H]1CCO)C3=CC=CC(=C3)C4=CN=CC=C4)C(=O)NCC5=CC=CC=C5F', "
               "'Molecule is an organosulfonic acid'), "
               "('CC(C)(C)[S@@](=O)N1CC2=CC(=NC(=C2[C@H]1CCO)C3=CC(=CC=C3)C4=CCCC4)C(=O)NCCOC', "
               "'Molecule is an organosulfonic acid'), "
               "('COc1ccnc(CS(=O)c2nc3cc(OC(F)F)ccc3[nH]2)c1OC', 'Molecule is "
               "an organosulfonic acid'), "
               "('CC(=O)N[C@@H](CS(N)=O)C(=O)N[C@@H]1[C@@H](O)[C@H](O)[C@@H](CO)O[C@@H]1O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H](O)[C@H]1O', "
               "'Molecule is an organosulfonic acid'), "
               "('S1(=O)[C@H]([C@](O)([C@@]2(O)[C@H](OC)[C@H](O)CC[C@@]2(C1)O)C)CC=C(C)C', "
               "'Molecule is an organosulfonic acid'), "
               "('Cl[C@@]1([C@@H]2OC(=O)[C@H]3N=C([C@@]4(NC(=CC([C@@]([C@H](CCC(=C[C@H]([C@H]1C)[C@@H](C2)O[C@@H]5O[C@@H]([C@@H](N(C)C)CC5)C)C)O)(O[C@@H]6O[C@@H]([C@@H](N(C)C)CC6)C)C)=O)S([C@@H]4OC)=O)C)SC3)C', "
               "'Molecule is an organosulfonic acid'), "
               "('CC=CC1=CC=CC(=C1)C2=C3[C@@H](N(CC3=CC(=N2)C(=O)NCC4=CC=NC=C4)[S@@](=O)C(C)(C)C)CCO', "
               "'Molecule is an organosulfonic acid'), "
               "('Cc1cc(ccc1OCC(O)=O)S(=O)Cc1sc(nc1C)-c1ccc(cc1)C(F)(F)F', "
               "'Molecule is an organosulfonic acid'), "
               "('CC(C)(C)[S@@](=O)N1CC2=CC(=NC(=C2[C@H]1CCO)C3=CC=CC(=C3)C4=CC=CC=C4OC)C(=O)N5CCOCC5', "
               "'Molecule is an organosulfonic acid'), "
               "('CC(C)(C)[S@](=O)N1CC2=CC(=NC(=C2[C@@H]1CCO)C3=CC=CC(=C3)C4=CC=CC(=C4)C#N)C(=O)NCC5=CC=NC=C5', "
               "'Molecule is an organosulfonic acid'), "
               "('S(=O)(CC[C@H](NC(=O)C1=NC=2C(=O)N(C(=O)N(C2N=C1)C)C)C(=O)NC3=C(C(=O)OC)C=CC=C3)C', "
               "'Molecule is an organosulfonic acid'), "
               "('C1=CC=C(C(=C1)CN2C3=C(C=CC(=C3)C(=O)O)S(=O)C4=CC=CC=C4C2=O)F', "
               "'Molecule is an organosulfonic acid'), "
               "('CCCNC(=O)C1=NC(=C2[C@@H](N(CC2=C1)[S@@](=O)C(C)(C)C)CCO)C3=CC=CC(=C3)C4=CC(=CC=C4)F', "
               "'Molecule is an organosulfonic acid'), "
               "('COc1c(C)c(CCCCCCCCCCS(C)=O)oc(=O)c1OC', 'Molecule is an "
               "organosulfonic acid'), "
               "('CC(C)(C)[S@@](=O)N1CC2=CC(=NC(=C2[C@H]1CCO)C3=CC=CC(=C3)C4=CC(=CC=C4)C(=O)N(C)C)C(=O)N5CCCCC5', "
               "'Molecule is an organosulfonic acid'), "
               "('S(=O)(/C=C\\\\C(O[C@H]1[C@@H]([C@]2(C[C@H](C(=O)C=C2CC1)C(C)=C)C)C)=O)C', "
               "'Molecule is an organosulfonic acid'), "
               "('C=1C(=C(C(=CC1C(F)(F)F)Cl)N2N=C(C(=O)C)C(=C2N)S(=O)C)Cl', "
               "'Molecule is an organosulfonic acid'), "
               "('S(=O)(CC[C@H]1NC(=O)C(N(C(=O)CC[C@@H](NC(=O)[C@H]([C@H](/C=C/C(=C/[C@@H]([C@@H](OC)CC2=CC=CC=C2)C)/C)NC([C@@H](NC([C@H]([C@@H](NC([C@@H](NC1=O)CC(C)C)=O)C(=O)O)C)=O)CCCN=C(N)N)=O)C)C(=O)OC)C)=C)C', "
               "'Molecule is an organosulfonic acid'), "
               "('CC(C)(C)[S@](=O)N1CC2=CC(=NC(=C2[C@@H]1CCO)C3=CC=CC(=C3)C4=CC=CC(=C4)C#N)C(=O)NCCN5CCCC5', "
               "'Molecule is an organosulfonic acid'), "
               "('CC(C)(C)[S@](=O)N1CC2=CC(=NC(=C2[C@@H]1CCO)C3=CC=CC(=C3)C4=CC=CC(=C4)C#N)C(=O)NCCC5=CC=NC=C5', "
               "'Molecule is an organosulfonic acid'), "
               "('CC(C)(C)[S@](=O)N1CC2=CC(=NC(=C2[C@@H]1CCO)C3=CC=CC(=C3)C4=CC=C(C=C4)C#N)C(=O)N5CCN(CC5)C', "
               "'Molecule is an organosulfonic acid'), "
               "('CC(C)(C)[S@](=O)N1CC2=CC(=NC(=C2[C@@H]1CCO)C3=CC=CC(=C3)C4=CC(=CC=C4)F)C(=O)NCC(F)(F)F', "
               "'Molecule is an organosulfonic acid'), "
               "('CCNC(=O)C1=NC(=C2[C@H](N(CC2=C1)[S@](=O)C(C)(C)C)CCO)C3=CC=CC(=C3)C4=CC(=CC=C4)C(=O)N(C)C', "
               "'Molecule is an organosulfonic acid'), "
               "('S(=O)(C(C1=CC=CC=C1)C2=CC=CC=C2)CC(O)=O', 'Molecule is an "
               "organosulfonic acid'), "
               "('CC(C)(C)[S@](=O)N1CC2=CC(=NC(=C2[C@@H]1CCO)C3=CC=CC(=C3)C4=CC=CC=C4F)C(=O)N5CCCCC5', "
               "'Molecule is an organosulfonic acid'), "
               "('C1=CC=C2C(=C1)C3=CC=CC=C3S2=O', 'Molecule is an "
               "organosulfonic acid'), "
               "('CC(C)(C)S(=O)N1CC2=CC(=NC(=C2[C@@H]1CCO)C3=CC=CC(=C3)C#CC(C)(C)O)C(=O)N[C@@H]4CCN(C4)CC5=CC=CC=C5', "
               "'Molecule is an organosulfonic acid'), "
               "('[O-]S(=O)CCNC(=[NH2+])NP([O-])([O-])=O', 'Molecule is an "
               "organosulfonic acid'), "
               "('CC(C)(C)[S@](=O)N1CC2=CC(=NC(=C2[C@@H]1CCO)C3=CC=CC(=C3)C4=CC(=CC=C4)C(=O)N(C)C)C(=O)NC5CCCCC5', "
               "'Molecule is an organosulfonic acid'), "
               "('CC(C)(C)[S@](=O)N1CC2=CC(=NC(=C2[C@@H]1CCO)C3=CC=CC(=C3)C4=CC=C(C=C4)C#N)C(=O)NCC5=CC=NC=C5', "
               "'Molecule is an organosulfonic acid'), "
               "('[H][C@@]1(NC(=O)[C@H]2CSSCC\\\\C=C\\\\[C@H](CC(=O)N[C@H](CCS(C)=O)C(=O)N2)OC(=O)C[C@@H]1O)[C@@H](C)CC', "
               "'Molecule is an organosulfonic acid'), "
               "('S(=O)(C1=CC=C(/C=C/2\\\\C3=C(C=C(F)C=C3)C(=C2CO)CC(=O)OC4O[C@H](C(=O)O)[C@@H](O)[C@@H]([C@H]4O)O)C=C1)C', "
               "'Molecule is an organosulfonic acid'), "
               "('CCOC(=O)C1=NC(=C2[C@H](N(CC2=C1)S(=O)C(C)(C)C)CCO)C3=CC=CC(=C3)C#CCN(C)C', "
               "'Molecule is an organosulfonic acid'), "
               "('S1(=O)C(C(=O)C2=CC=C(C(C)C(O)=O)C=C2)=CC=C1', 'Molecule is "
               "an organosulfonic acid'), "
               "('S1(=O)C(C(N(O)C(=O)N)C)=CC=2C1=CC=CC2', 'Molecule is an "
               "organosulfonic acid'), "
               "('S1(=O)C(SC)[C@@H]2N(C(=O)[C@@H](NC(=O)[C@H](NC(=O)C3=NC=4C(=CC=CC4)N=C3)COC([C@@H](N(C([C@H](C1)N(C(=O)[C@@H](NC(=O)[C@H](NC(=O)C5=NC=6C(=CC=CC6)N=C5)COC([C@@H](N(C2=O)C)[C@H](CC)C)=O)C)C)=O)C)[C@H](CC)C)=O)C)C', "
               "'Molecule is an organosulfonic acid'), "
               "('CC(C)(C)[S@](=O)N1CC2=CC(=NC(=C2[C@@H]1CCO)C3=CC=CC(=C3)C4=CC(=CC=C4)F)C(=O)NCCOC', "
               "'Molecule is an organosulfonic acid'), "
               "('S(=O)(CCC(N1C(=O)C=2C=C(O)C3=C(C2C1)O[C@]4([C@@]5([C@H](C([C@H](O)CC5)(C)C)CC[C@H]4C)C)C3)C(=O)NC(C(=O)NC(C(=O)N6C(C(=O)NC(C(=O)NC(C(=O)N7C(C(=O)NC(C(=O)N8C(C(=O)N9C(C(=O)O)CCC9)CCC8)CC(C)C)CCC7)CCC(=O)N)CC=%10NC=NC%10)CCC6)CCC(=O)N)CC=%11NC=NC%11)C', "
               "'Molecule is an organosulfonic acid'), "
               "('CC(C)(C)[S@@](=O)N1CC2=CC(=NC(=C2[C@H]1CCO)C3=CC=CC(=C3)C4=CC=C(C=C4)C#N)C(=O)NCC5=CC=C(C=C5)OC', "
               "'Molecule is an organosulfonic acid'), "
               "('S1(=O)[C@@]2(S[C@]1([C@@H]([C@H]2C)C)[H])[H]', 'Molecule is "
               "an organosulfonic acid'), ('[C@H](CS(=O)[O-])(C(=O)*)N*', "
               "'Molecule is an organosulfonic acid'), "
               "('S(=O)(CCC1NC(=O)C(N(C(=O)C(NC(=O)C(C(C)C)NC(C(CCCCNC1=O)NC(=O)NC(C(=O)O)C(CC)C)=O)CCC2=CC=CC=C2)C)CCC3=CC=C(O)C=C3)C', "
               "'Molecule is an organosulfonic acid'), "
               "('CCCNC(=O)C1=NC(=C2[C@H](N(CC2=C1)[S@](=O)C(C)(C)C)CCO)C3=CC=CC(=C3)C4=CC(=CC=C4)F', "
               "'Molecule is an organosulfonic acid'), "
               "('S(=O)(C(C1=CC=CC=C1)C=2C(=O)OCC2C3=CC=CC=C3)C', 'Molecule is "
               "an organosulfonic acid')]\n"
               "False negatives: [('CCc1cccc(C)c1N(C(C)COC)C(=O)CS(O)(=O)=O', "
               "'No sulfonic acid groups found'), "
               "('OS(=O)(=O)C(C([O-])=O)c1ccccc1', 'No sulfonic acid groups "
               "found'), ('*C(NCCS(O)(=O)=O)=O', 'No sulfonic acid groups "
               "found'), ('Nc1c(O)cc(c2ccccc12)S(O)(=O)=O', 'No sulfonic acid "
               "groups found'), "
               "('Oc1ccc2cc(cc(c2c1\\\\N=N\\\\c1ccccc1)S(O)(=O)=O)S(O)(=O)=O', "
               "'No sulfonic acid groups found'), "
               "('OS(=O)(=O)c1cc(c2cccc(c2c1)S(O)(=O)=O)S(O)(=O)=O', 'No "
               "sulfonic acid groups found'), "
               "('C12=CC(=CC=C1[N+](=C(C2(CCCCC(=O)O*)C)/C=C/C=C/C=C/3\\\\C(C4=CC(=CC=C4N3CCCS(O)(=O)=O)S(O)(=O)=O)(C)C)CCCS([O-])(=O)=O)S(O)(=O)=O', "
               "'No sulfonic acid groups found'), ('OS(=O)(=O)CCS', 'No "
               "sulfonic acid groups found'), "
               "('OS(=O)(=O)c1ccc2O[Cu]Oc3c(\\\\N=N\\\\c2c1)c(cc1c(c(Nc2ncnc(Nc4ccc5c6O[Cu]Oc7ccc(cc7\\\\N=N\\\\c6c(cc5c4S(O)(=O)=O)S(O)(=O)=O)S(O)(=O)=O)n2)ccc31)S(O)(=O)=O)S(O)(=O)=O', "
               "'No sulfonic acid groups found'), "
               "('C12=[N+]3C(=NC=4N5C(N=C6[N+]7=C(N=C8N(C(=N1)C9=CC=CC=C89)[Cu-2]357)C%10=C(C=CC=C6%10)S(O)(=O)=O)=C%11C=CC=CC4%11)C%12=C(C=CC=C2%12)S(O)(=O)=O', "
               "'No sulfonic acid groups found'), ('CC(C)S(O)(=O)=O', 'No "
               "sulfonic acid groups found'), "
               "('OS(=O)(=O)c1ccc(cc1[N+]([O-])=O)[N+]([O-])=O', 'No sulfonic "
               "acid groups found'), ('C(CCS(O)(=O)=O)C', 'No sulfonic acid "
               "groups found'), "
               "('OS(=O)(=O)c1ccc(Nc2ccc(cc2)C(=C2C=CC(C=C2)=Nc2ccc(cc2)S(O)(=O)=O)c2ccc(Nc3ccc(cc3)S(O)(=O)=O)cc2)cc1', "
               "'No sulfonic acid groups found'), "
               "('CCCCCCCCCCCCCCCCS(O)(=O)=O', 'No sulfonic acid groups "
               "found'), ('[Na+].S(=O)(CCS)(=O)[O-]', 'No sulfonic acid groups "
               "found'), ('OC[C@@H](O)CS(O)(=O)=O', 'No sulfonic acid groups "
               "found'), ('OC(=O)c1cc(ccc1O)S(O)(=O)=O', 'No sulfonic acid "
               "groups found'), ('Nc1ccc2c(O)cc(cc2c1)S(O)(=O)=O', 'No "
               "sulfonic acid groups found'), "
               "('S(O)(=O)(=O)C1=CC=2C(C(O)=C1/N=N/C3=C4C(=C(/N=N/C5=CC=C(S(O)(=O)=O)C=C5)C=C3)C=CC(S(O)(=O)=O)=C4)=CC(N)=C(S(O)(=O)=O)C2', "
               "'No sulfonic acid groups found'), "
               "('OC1O[C@H](CS(O)(=O)=O)[C@@H](O)[C@H](O)[C@H]1O', 'No "
               "sulfonic acid groups found'), "
               "('OS(=O)(=O)c1cccc2c(NCCNC(=O)CI)cccc12', 'No sulfonic acid "
               "groups found'), ('CC(=O)NCCCS(O)(=O)=O', 'No sulfonic acid "
               "groups found'), ('S(O)(=O)(=O)CC(N)C(O)CCCCCCCCCCCC(C)C', 'No "
               "sulfonic acid groups found'), ('C(CS(O)(=O)=O)N', 'No sulfonic "
               "acid groups found'), ('Nc1ccccc1S(O)(=O)=O', 'No sulfonic acid "
               "groups found'), ('C[C@@H](O)CSCCS(O)(=O)=O', 'No sulfonic acid "
               "groups found'), "
               "('OC[C@H]1N[C@H]([C@H](O)[C@@H](O)[C@@H]1O)S(O)(=O)=O', 'No "
               "sulfonic acid groups found'), ('OS(=O)(=O)CCN1CCOCC1', 'No "
               "sulfonic acid groups found'), "
               "('Cc1cccc(C)c1N(Cn1cccn1)C(=O)CS(O)(=O)=O', 'No sulfonic acid "
               "groups found')]",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 30,
    'num_false_positives': 100,
    'num_true_negatives': 1541,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.23076923076923078,
    'recall': 1.0,
    'f1': 0.375,
    'accuracy': 0.9401555954518253}