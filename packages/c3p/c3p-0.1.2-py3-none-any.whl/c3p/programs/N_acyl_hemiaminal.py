"""
Classifies: CHEBI:142734 N-acyl hemiaminal
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_N_acyl_hemiaminal(smiles: str):
    """
    Determines if a molecule is an N-acyl hemiaminal.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is an N-acyl hemiaminal, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find amide and alcohol groups
    amide_atoms = []
    alcohol_atoms = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N':
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'C' and neighbor.GetDegree() == 3 and neighbor.GetFormalCharge() == 0:
                    amide_atoms.append(neighbor.GetIdx())
        elif atom.GetSymbol() == 'O' and atom.GetHybridization() == Chem.HybridizationType.SP3:
            alcohol_atoms.append(atom.GetIdx())

    # Check if amide groups are connected to aldehyde or ketone
    for amide_idx in amide_atoms:
        amide_atom = mol.GetAtomWithIdx(amide_idx)
        carbonyl_atom = None
        for neighbor in amide_atom.GetNeighbors():
            if neighbor.GetSymbol() == 'C' and neighbor.GetDegree() == 3 and neighbor.GetFormalCharge() == 0:
                carbonyl_atom = neighbor
                break
        if carbonyl_atom is None:
            continue
        for neighbor in carbonyl_atom.GetNeighbors():
            if neighbor.GetSymbol() == 'O' and neighbor.GetFormalCharge() == 0:
                break
        else:
            continue  # No carbonyl group found

        # Check if amide and alcohol groups are connected
        for alcohol_idx in alcohol_atoms:
            alcohol_atom = mol.GetAtomWithIdx(alcohol_idx)
            if mol.GetBondBetweenAtoms(amide_atom.GetIdx(), alcohol_atom.GetIdx()) is not None:
                return True, "The molecule is an N-acyl hemiaminal"

    return False, "The molecule does not meet the criteria for an N-acyl hemiaminal"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:142734',
                          'name': 'N-acyl hemiaminal',
                          'definition': 'An organic hydroxy compound resulting '
                                        'from the formal addition of the amino '
                                        'group of a carboxamide to the '
                                        'carbonyl group of an aldehyde or '
                                        'ketone.',
                          'parents': ['CHEBI:33822', 'CHEBI:37622']},
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
               "[('CC1=CN([C@H]2C[C@H](O)[C@@H](COP(O)(=O)O[C@H]3C[C@@H](O[C@@H]3CO)N3C=CC(N)=NC3=O)O2)C(=O)NC1=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('Cc1cn([C@H]2C[C@H](O)[C@@H](COP(O)(=O)O[C@H]3C[C@@H](O[C@@H]3COP(O)(=O)O[C@H]3C[C@@H](O[C@@H]3COP(O)(O)=O)n3cc(C)c(=O)[nH]c3=O)n3cc(C)c(=O)[nH]c3=O)O2)c(=O)[nH]c1=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('C1(C(=O)OP(OC[C@H]2O[C@@H](N3C=4N=CN=C(N)C4N=C3)[C@@H]([C@@H]2O)O)(=O)[O-])=CC=C(C=C1)N', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('CCOP(O)(=O)OP(O)(=O)OP(O)(=O)OC[C@@H]1CC[C@@H](O1)n1cc(C)c(=O)[nH]c1=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('O1[C@H](N2C3=NC=NC(N[C@@H](CC(O)=O)C(O)=O)=C3N=C2)[C@H](O)[C@H](O)[C@H]1CO', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('O(C[C@@H](COC(CCCCCCCCCCCCC)=O)OC(CCCCCCCCCCCCC)=O)P(OP(OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)N2C(N=C(C=C2)N)=O)(=O)O)(=O)O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('Cc1cn([C@@H]2O[C@H](CO)[C@@H](O)[C@H]2O)c(=O)nc1N', 'The "
               "molecule is an N-acyl hemiaminal'), "
               "('O(C[C@@H](COC(CCCCCC=CCCCCCC)=O)OC(CCCCCC=CCCCCCC)=O)P(OP(OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)N2C(N=C(C=C2)N)=O)(=O)O)(=O)O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)C[C@@](C(=O)[O-])(O)CC(=O)[O-])=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('[H][C@]1(O[C@@H](OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H](C[C@@H]2O)n2cc(C)c(=O)[nH]c2=O)[C@H](O)[C@H]1O)[C@@H](C)O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('O=C(OC)[C@H]1O[C@H](N2C3=C(C(OC)=CC=C3)C(=C2)CC(=O)N)[C@@H](O)[C@H](C1)O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('O1[C@@H](N2C3=NC=NC(N)=C3NC2=O)C[C@H](O)[C@H]1CO', 'The "
               "molecule is an N-acyl hemiaminal'), "
               "('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)\\\\C=C\\\\C=C\\\\[*]', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('[H][C@]12NC(=N)N[C@@]1(O)[C@@]1([H])[C@H](CNC(=O)c3cc(Br)c(Br)[nH]3)[C@@H](CNC(=O)c3cc(Br)c(Br)[nH]3)[C@H](O)[C@@]11NC(=N)N[C@@]1([H])O2', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)CCC(C)C)=O)=O)O)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)[C@H](CO)C)=O)=O)O)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('P(O[C@H]1C[C@@H](O[C@@H]1CO)N2CN(C3=C2N=C(NC3=O)N)C)(O)(O)=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('CC(=O)C1=CC=C[N+](=C1)[C@@H]1O[C@H](COP([O-])(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)N2C=NC3=C2N=CN=C3N)[C@@H](O)[C@H]1O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C1=CCC=CC1', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('C[C@@H](O)[C@@H]1O[C@H](OP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H](C[C@@H]2O)n2cc(C)c(=O)[nH]c2=O)[C@H](O)[C@H]1O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)\\\\C=C1\\\\CC=CC=CO1', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('CN(N=O)C(O)CCC(=O)c1cccnc1', 'The molecule is an N-acyl "
               "hemiaminal'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)CCCC/C=C\\\\C)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('O(P(OC[C@H]1O[C@@H](N2C=3N=C(NC(=O)C3N=C2)N)[C@@H]([C@@H]1O)O)(=O)[O-])P(O[C@H]4[C@H]([C@H](*)O[C@@H]4COP(*)(=O)[O-])O)([O-])=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('O1C(N2C=3N=CN4C(=NC=C4)C3N=C2)C[C@H](O)[C@H]1CO', 'The "
               "molecule is an N-acyl hemiaminal'), "
               "('N(C(C(NCCCCNCCCN)=O)O)C(CCCCCCNC(=N)N)=O', 'The molecule is "
               "an N-acyl hemiaminal'), "
               "('P(OC[C@H]1O[C@@H](N2C=CC(=NC2=O)N)[C@H](O)[C@@H]1O)(OP(OC[C@H](OC(=O)CCCCCCCC(=O)/C=C/C=C\\\\CCCCC)COC(=O)CCCCCCCCCCC(C)C)(O)=O)(O)=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C(CC(O)=O)Cc1ccccc1', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('O1[C@@H](N2C=CC(=NC2=O)NC(=O)C)C[C@H](O)[C@H]1CO', 'The "
               "molecule is an N-acyl hemiaminal'), "
               "('OC([N+](C)(C)C)C(O)(C(=O)CC(C)C)CC([O-])=O', 'The molecule "
               "is an N-acyl hemiaminal'), "
               "('C[C@H]1O[C@@H](CC(=O)[C@@H]1O)OP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H](C[C@@H]1O)n1cc(C)c(=O)[nH]c1=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('N([C@@H]1O[C@@H]([C@H]([C@@H]([C@H]1NC(=O)C)O)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)CO)O[C@H]3[C@H]([C@H]([C@@H]([C@H](O3)CO[C@@H]4[C@H]([C@H]([C@@H]([C@H](O4)CO[C@@H]5[C@H]([C@H]([C@@H]([C@H](O5)CO)O)O)O)O)O[C@@H]6[C@H]([C@H]([C@@H]([C@H](O6)CO)O)O)O[C@@H]7[C@H]([C@H]([C@@H]([C@H](O7)CO)O)O)O)O)O)O[C@@H]8[C@H]([C@H]([C@@H]([C@H](O8)CO)O)O)O[C@@H]9[C@H]([C@H]([C@@H]([C@H](O9)CO)O)O)O)O)O)NC(C)=O)CO)C(C[C@@H](C(*)=O)N*)=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)[C@H](C)CCC[C@]([C@@]4([C@]5(CC[C@@]6([C@]7(CCC(C=C7CC[C@]6([C@@]5(CC4)[H])[H])=O)C)[H])C)[H])(C)[H])=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'The molecule is an N-acyl hemiaminal'), ('O1C(N=C(C1)C)C', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('[H][C@]12OC[C@](CO)(O[C@H]1n1cc(C)c(N)nc1=O)[C@H]2O', 'The "
               "molecule is an N-acyl hemiaminal'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)CC[C@@](C)([C@]4(CC[C@@]5([C@@]4(CC[C@@]6([C@]7(CC[C@H](C[C@]7(CC[C@@]56[H])[H])O)C)[H])C)[H])[H])[H])=O)=O)O)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('[C@@H]1(O[C@H]([C@@H]([C@@H]1O*)O)N2C3=C(C(=NC=N3)N)N=C2)COP(OP([O-])(=O)[O-])(=O)[O-]', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('N1([C@@H]2O[C@H](CO)[C@H]([C@H]2O)O)C(=C(C(=NC1=*)*)*)*', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('[C@@H]1(N2C(NC(=O)C(=C2)CNC)=S)O[C@H](COP(*)(=O)O)[C@H]([C@H]1O)O*', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('P1(OC[C@H]2O[C@@H](N3C=CC(=NC3=O)N)[C@H](C(=O)C[C@@H](O)[C@@H]([C@H](O)[C@@H]2O)/C=C/[C@@H](O)CCCCC)CC=CCCCC(OC[C@@H](OC(=O)CCCCCCCC/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCCC)COP(O1)(O)=O)=O)(O)=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('P(OC[C@H]1O[C@@H](N2C3=NC=NC(N)=C3N=C2)[C@H](O)[C@@H]1O)(OC(=O)CCCCCCCCCCCCCCCCC)(O)=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('Cc1cn([C@H]2C[C@H](O)[C@@H](COP(O)(=O)O[C@H]3C[C@@H](O[C@@H]3COP(O)(=O)O[C@H]3C[C@@H](O[C@@H]3COP(O)(=O)O[C@H]3C[C@@H](O[C@@H]3COP(O)(=O)O[C@H]3C[C@@H](O[C@@H]3COP(O)(O)=O)n3cc(C)c(=O)[nH]c3=O)n3cc(C)c(=O)[nH]c3=O)n3cc(C)c(=O)[nH]c3=O)n3cc(C)c(=O)[nH]c3=O)O2)c(=O)[nH]c1=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('OC[C@H]1O[C@H](C[C@@H]1OP(O)(=O)OC[C@H]1O[C@H](C[C@@H]1OP(O)(=O)OC[C@H]1O[C@H](C[C@@H]1OP(O)(=O)OC[C@H]1O[C@H](C[C@@H]1OP(O)(=O)OC[C@H]1O[C@H](C[C@@H]1O)n1ccc(=O)[nH]c1=O)n1ccc(=O)[nH]c1=O)n1ccc(=O)[nH]c1=O)n1ccc(=O)[nH]c1=O)n1ccc(=O)[nH]c1=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('C[C@H](O)C(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)N1C=NC2=C1N=CN=C2N', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('C[C@@H]1OC(OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2cnc3c2nc(N)[nH]c3=O)[C@@H](O)[C@H](O)[C@@H]1O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('P(O[C@@H]1[C@H](O[C@H]([C@@H]1O)N2C=NC=3C(=NC=NC32)N)COP(O[C@@H]4[C@H](O[C@H]([C@@H]4O)N5C=NC=6C(NC(=NC65)N)=O)CO)(=O)[O-])([O-])(=O)[O-]', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(C[C@H](CC)O)=O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)CC[C@@](C)([C@]4(CC[C@@]5([C@@]4(CC[C@@]6([C@]7(CCC(C[C@]7(CC[C@@]56[H])[H])=O)C)[H])C)[H])[H])[H])=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('C[C@H]1O[C@H](OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H](C[C@@H]2O)n2cc(C)c(=O)[nH]c2=O)[C@H](O)[C@@H](N)[C@H]1O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('C[C@H]1O[C@@H](C[C@@H](O)C1=O)OP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H](C[C@@H]1O)n1cc(C)c(=O)[nH]c1=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('P(OC[C@H]1O[C@@H](N2C=CC(=NC2=O)N)C(O)[C@H]1O)(OP(OC[C@H](OC(=O)CCCCCCCCCCC(C)C)COC(=O)CCCCCCCCC(C)C)(O)=O)(O)=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('P(OCC1OC(N2C=3N=C(NC(=O)C3N=C2)N)CC1O)(O)(O)=O', 'The "
               "molecule is an N-acyl hemiaminal'), "
               "('[C@@H]1(N2C(NC(=O)C(=C2)C)=O)O[C@H](COP(OP(O[C@H]3O[C@@H]([C@H](CC3)[NH+](C)C)C)(=O)[O-])(=O)[O-])[C@H](C1)O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('O1C(O)[C@H](OC(CCCCCCC)=O)[C@H](O)[C@H]1COP(OP(OC[C@@H]2[C@H]([C@H]([C@H](N3C4=NC=NC(=C4N=C3)N)O2)O)O)(=O)[O-])(=O)[O-]', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)c1ccc(O)o1', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('OC[C@H]1O[C@H]([C@H](OP(O)(O)=O)[C@@H]1O)n1ccc(=O)[nH]c1=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('C[C@H]1O[C@H](OP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(N)nc2=O)[C@H](O)C[C@H]1O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('O[C@H]1C[C@@H](O[C@@H]1COP(O)(=O)OP(O)(O)=O)n1cnc2c1nc[nH]c2=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('C([C@]1([H])[C@]([H])([C@]([H])([C@]([H])(N2CN=C3C2=NC=NC3(CO)N)O1)O)O)O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('[C@@H]1(N2C(NC(=O)C=C2)=O)O[C@H](COP(OP([O-])(O[C@@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O)OC(=O)C[C@@H](*)O)NC(C[C@@H](*)O)=O)=O)([O-])=O)[C@H]([C@H]1O)O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC([C@H](C(NCCC(NCCSC(=O)C(*)O)=O)=O)O)(C)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1ccc(N)nc1=O)OC(=O)CCC\\\\C=C/C\\\\C=C/C\\\\C=C/C\\\\C=C/CCCCC', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('[H][C@]12NC3=C(N[C@@]1([H])C1=C(S[Mo-](O)(=O)(=O)S1)[C@@H](COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)N1C=NC4=C1N=C(N)NC4=O)O2)C(=O)NC(N)=N3', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('[C@H]1([C@H](O[C@H]([C@@H]1O)N2C=NC3=C2N=C(NC3=O)NC4O[C@H](COP(OP(OC[C@H]5O[C@@H](N6C7=C(C(=NC=N7)N)N=C6)[C@@H]([C@@H]5O)O)(=O)[O-])(=O)[O-])[C@H]([C@H]4O)O)COP(OP([O-])(=O)[O-])(=O)[O-])O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('N[C@@H](O)Cc1c[nH]c2ccccc12', 'The molecule is an N-acyl "
               "hemiaminal'), "
               "('[C@@H]1(N2C(NC(=O)C=C2)=O)O[C@H](COP(*)(=O)[O-])[C@H]([C@H]1OC)O*', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C[C@H](O)C(O)=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('P(OC[C@H]1O[C@@H](N2C3=NC=NC(N)=C3N=C2)[C@H](O)[C@@H]1O)(OP(OC[C@H]4O[C@H]([N+]=5C=C(C=CC5)C(=O)N)[C@H](O)[C@@H]4O)([O-])=O)(O)=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC([C@H](C(NCCC(NCCSC(C(CCCCCCCCCCCCCCCC)C)=O)=O)=O)O)(C)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('Cc1cn([C@H]2CC[C@@H](COP(O)(=O)OP(O)(=O)OP(O)(O)=O)O2)c(=O)[nH]c1=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('[Cl-].O1[C@@H]([N+]=2C=C(C=CC2)C(=O)N)[C@H](O)[C@H](O)[C@H]1CO', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('[H][C@@]1(CN2CCN3CCC[C@@]3([H])[C@]2([H])O1)NC[C@H]1CN(C)[C@]2([H])Cc3c[nH]c4cccc(C2=C1)c34', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CCCCCCC\\\\C=C/C\\\\C=C/CC=C', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('O1[C@@H]([C@H]([C@H]([C@@H]1N2C(=C[NH+]=C2)N)O)O)COP(=O)([O-])[O-]', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC([C@H](C(NCCC(NCCS(N)=O)=O)=O)O)(C)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('O1[C@@H](N2CCC(=O)NC2=O)[C@H](O)[C@H](O)[C@H]1COC\\\\C=C(\\\\CCC(O)C(O)(CCC=C(C)C)C)/C', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC([C@H](C(NCCC(NCCSC(=O)C[C@@H](O)CCCCCCCCCCCCCCCCCCC)=O)=O)O)(C)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('O1[C@H](OC(C)=O)[C@H](O)[C@H](O)[C@H]1COP(OP(OC[C@@H]2[C@H]([C@H]([C@H](N3C4=NC=NC(=C4N=C3)N)O2)O)O)(=O)[O-])(=O)[O-]', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('O1C(O)[C@H](OC(CCCC(O)=O)=O)[C@H](O)[C@H]1COP(OP(OC[C@@H]2[C@H]([C@H]([C@H](N3C4=NC=NC(=C4N=C3)N)O2)O)O)(=O)O)(=O)O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC[C@H]1[C@@H]2CCC(=O)[C@@]2(C)CC[C@H]1O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC12OC1C=CC=C2', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('O[C@H]1CO[C@H](OP(O)(=O)OP(O)(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2O)n2ccc(=O)[nH]c2=O)[C@H](O)[C@H]1O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('CCC(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1cnc2c(N)ncnc12', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('O1C(N2C3=NC=NC(NC/C=C(/CO)\\\\C)=C3N=C2)C(O)C(O)C1CO', 'The "
               "molecule is an N-acyl hemiaminal'), "
               "('CO[C@@H]1[C@H]2OCO[C@H](NC(=O)[C@@H](O)[C@]3(CC(=C)[C@@H](C)[C@@H](C)O3)OC)[C@H]2O[C@H](C[C@H](O)CCC\\\\C=C\\\\C=C\\\\C=C\\\\C(=O)NC(CCCNC(N)=N)C(O)=O)C1(C)C', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('[H][C@]12Nc3nc(N)[nH]c(=O)c3N[C@@]1([H])C1=C(S[Mo](=O)(=O)(SC[C@H](N)C(O)=O)S1)[C@@H](COP([O-])([O-])=O)O2', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CCS(O)=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C1=CCCCC1O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('P(OC[C@H]1O[C@@H](N2C=CC(=NC2=O)N)C(O)[C@H]1O)(OP(OC[C@H](OC(=O)CCCCCCCCCCCCCC(C)C)COC(=O)CCCCCCCCCCCCCC(C)C)(O)=O)(O)=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('O1[C@@H]([C@H]([C@H]([C@@H]1N2C(=CN=C2)N)O)O)CO', 'The "
               "molecule is an N-acyl hemiaminal'), "
               "('[O-]C(=O)C(F)(F)F.[H][C@@]12CC[C@@]3([H])[C@@H](C(=O)OCCCCCCCCCCCCCC[C@]4([H])O[C@](O)(CCN)[C@H](O)N(CCCN)C4=O)[C@@]4(CCC[C@H](C)O4)NC(N[C@@]4(CC[C@H](O4)\\\\C=C\\\\CC)C1)=[N+]23', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)\\\\C=C\\\\c1ccccc1', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('OC[C@H]1O[C@H]([C@@H](O)[C@@H]1O)n1ccc(=O)[nH]c1=O', 'The "
               "molecule is an N-acyl hemiaminal'), "
               "('[H][C@]1(O)NC(=[NH2+])N[C@@]23[C@@]([H])(O)[C@]4([H])O[C@@](O)(O[C@]([H])([C@]12[H])[C@@]4(O)CO)[C@@]3([H])O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('O1[C@@H](N2C=CC(=NC2=O)NCCCCCCCC/C=C\\\\CCCCCCCC)[C@@H](O)[C@H](O)[C@H]1CO', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('CC(C)(COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP(O)(O)=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)[C@H](O)Cc1ccccc1', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)C[C@@H](O)CCC([O-])=O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('P1(OC[C@H]2O[C@@H](N3C=CC(=NC3=O)N)[C@@H](CC=CCCCC(OC[C@@H](OC(=O)CCCCCCCCCCCCCCC)COP(O1)(O)=O)=O)C=CC(=O)[C@@H]([C@H](O)[C@@H]2O)C=C[C@@H](O)CCCCC)(O)=O', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('CCCCCCCCCCCCCCCC(=O)OC[C@H](COP(O)(=O)OP(O)(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)n1ccc(N)nc1=O)OC(=O)CCCCCCCCCCCCCCC', "
               "'The molecule is an N-acyl hemiaminal'), "
               "('C[C@H]1O[C@H](OP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H](C[C@@H]2O)n2cc(C)c(=O)[nH]c2=O)[C@H](O)[C@H]([C@@H]1O)[NH+](C)C', "
               "'The molecule is an N-acyl hemiaminal')]\n"
               "False negatives: [('C(CCCCCCCCCC)CCCCC(N[C@H](C(O)=O)O)=O', "
               "'The amide and alcohol groups are not connected')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 4512,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.9783221331021027}