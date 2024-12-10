"""
Classifies: CHEBI:33272 ketimine
"""
from rdkit import Chem

def is_ketimine(smiles: str):
    """
    Determines if a molecule is a ketimine (any imine derived from a ketone).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a ketimine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find imine bonds
    imine_bonds = []
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.DOUBLE:
            begin_atom = bond.GetBeginAtom()
            end_atom = bond.GetEndAtom()
            if begin_atom.GetAtomicNum() == 7 and end_atom.GetAtomicNum() == 6:
                imine_bonds.append(bond)
            elif begin_atom.GetAtomicNum() == 6 and end_atom.GetAtomicNum() == 7:
                imine_bonds.append(bond)

    if not imine_bonds:
        return False, "No imine bonds found"

    # Check if the imine is derived from a ketone
    for bond in imine_bonds:
        carbon_atom = bond.GetBeginAtom() if bond.GetBeginAtom().GetAtomicNum() == 6 else bond.GetEndAtom()
        neighbors = carbon_atom.GetNeighbors()
        carbon_neighbors = [neighbor for neighbor in neighbors if neighbor.GetAtomicNum() == 6]

        if len(carbon_neighbors) == 2:
            for neighbor in carbon_neighbors:
                neighbor_bonds = [bond for bond in neighbor.GetBonds() if bond.GetBeginAtomIdx() == neighbor.GetIdx() or bond.GetEndAtomIdx() == neighbor.GetIdx()]
                double_bond_count = sum(1 for bond in neighbor_bonds if bond.GetBondType() == Chem.BondType.DOUBLE)
                if double_bond_count == 1:
                    return True, "Ketimine derived from a ketone"

    return False, "Not a ketimine or not derived from a ketone"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33272',
                          'name': 'ketimine',
                          'definition': 'Any imine derived from a ketone.',
                          'parents': ['CHEBI:24783']},
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
               'False positives: '
               "[('C=12N3C(=CC4=[N+]5C(=CC=6N7C=8C(=C9[N+](=C(C1)[C@H]([C@@H]9CCC([O-])=O)C)[Mg-2]753)CC(C8C6C)=O)C(=C4C)CC)C(=C2C)C=C', "
               "'Ketimine derived from a ketone'), ('N1=C(/C=C/CCCCCCC)CCCC1', "
               "'Ketimine derived from a ketone'), "
               "('C1C(N=C2C=C(NN2C1C(F)(F)F)C(=O)O)C3=CC=CO3', 'Ketimine "
               "derived from a ketone'), "
               "('CC1=CC=C(O1)C2=CC(=NN2)C(=O)NN=CC=CC3=CC=CC=C3OC', 'Ketimine "
               "derived from a ketone'), "
               "('C1=CC(=CC=C1C2=CC=C(C=C2)NN=C3C=CC(=O)C(=C3)C(=O)O)NN=C4C=CC(=O)C(=C4)COO', "
               "'Ketimine derived from a ketone'), "
               "('ON=C1C=CC(C=C1)=NNC(=O)c1ccccc1', 'Ketimine derived from a "
               "ketone'), "
               "('OC(=O)CCC=1C2N=C(CC3N=C(CC4=NC(CC=5NC(C2)=C(C5CCC(O)=O)C)C(=C4C)CCC(O)=O)C(=C3C=C)C)C1C', "
               "'Ketimine derived from a ketone'), "
               "('[O-]N=C1C(=O)C=Cc2cc(ccc12)S([O-])(=O)=O', 'Ketimine derived "
               "from a ketone'), "
               "('O=C(NC(C(=O)O)C(O)C(=O)N)/C(=C/C=C/C=C/C=C/C(=C/[C@H]1N=C(/C=C/C=2NC=CC2)O[C@@H]1C)/C)/C', "
               "'Ketimine derived from a ketone'), "
               "('COC(=O)NN=CC1=CC(=NNC2=CC=CC=C2Cl)C=CC1=O', 'Ketimine "
               "derived from a ketone'), ('OC(=O)CC1=NCN=C1', 'Ketimine "
               "derived from a ketone'), "
               "('CCC1=C(C)\\\\C(NC1=O)=C\\\\C1=C(C)C(CCC([O-])=O)=C(N1)\\\\C=C1/N=C(/C=C2\\\\NC(=O)[C@H](C)\\\\C\\\\2=C/C)C(C)=C1CCC([O-])=O', "
               "'Ketimine derived from a ketone'), "
               "('CCOC(=O)C1=C(C(=C2CSC(=NN2)NC3=CC=CC=C3)N=C1C)C', 'Ketimine "
               "derived from a ketone'), "
               "('OC[C@H]1O[C@@H](Oc2cc3C[C@@H](C([O-])=O)\\\\[N+](=C/C=C4C[C@H](NC(=C\\\\4)C(O)=O)C(O)=O)c3cc2O)[C@H](O)[C@@H](O)[C@@H]1O', "
               "'Ketimine derived from a ketone'), "
               "('C1CN=C(C(=O)N1)CC(=O)C2=CC=C(C=C2)Br', 'Ketimine derived "
               "from a ketone'), "
               "('C1=C2[N+]3=C([C@H](C2(C)C)CCC(N)=O)C(=C2N4[C@@H]5[C@@H]([C@@]2(C)CCC(=O)NC[C@@H](C)OP([O-])(=O)O[C@@H]2[C@@H](CO)O[C@@H]([C@@H]2O)n2c6c(ncnc6[n+]([Co-3]343(C#N)[N+]4=C1[C@H]([C@](C4=C(C1=[N+]3[C@]5(C)[C@@]([C@@H]1CCC(N)=O)(C)CC(N)=O)C)(C)CC(N)=O)CCC(N)=O)c2)N)CC(N)=O)C', "
               "'Ketimine derived from a ketone'), "
               "('OC=1\\\\C(=C/2\\\\C=3C(N=C4C3C=CC=C4)=C(OC)C=C2C)\\\\C(=C(O)C=5C1N=C6C5C=CC=C6)C', "
               "'Ketimine derived from a ketone'), "
               "('C1=2N3C(C=C4N5=C(C=C6N7C(=CC8=N(C(=C1)C(=C8CCC(O)=O)C)[Fe]735)C(=C6C)CCC(O)=O)C(=C4C)C=C)=C(C2C)[C@H](CC/C=C(\\\\C)/CC/C=C(/CCC=C(C)C)\\\\C)O', "
               "'Ketimine derived from a ketone'), "
               "('O=C(OC)[C@@]1(O)C(O)=C2C(=C3C=C4N=C(C=C5N=C(C=C6NC(=C1C2=N3)[C@H]([C@@H]6C)CCC(=O)OC/C=C(/CCC[C@@H](CCC[C@@H](CCCC(C)C)C)C)\\\\C)C(=C5C=C)C)C(=C4CC)C)C', "
               "'Ketimine derived from a ketone'), "
               "('CO\\\\N=C(/C(=O)N[C@H]1[C@H]2SCC(COC(N)=O)=C(N2C1=O)C(=O)OC(C)OC(C)=O)c1ccco1', "
               "'Ketimine derived from a ketone'), "
               "('N1(CC(NC1=O)=O)N=CC=CC=2OC(=CC2)[N+]([O-])=O', 'Ketimine "
               "derived from a ketone'), "
               "('C1(=CC=NC=C1)C(N/N=C(/C([O-])=O)\\\\C)=O.[Ca+2].C1(=CC=NC=C1)C(N/N=C(/C([O-])=O)\\\\C)=O', "
               "'Ketimine derived from a ketone'), "
               "('C=12N3C(=CC4=[N+]5C(=CC=6N7C=8C(=C9[N+](=C(C1)[C@H]([C@@H]9CCC(OC/C=C(/CCC[C@@H](CCC[C@@H](CCCC(C)C)C)C)\\\\C)=O)C)[Mg-2]735)[C-](C(C8C6C)=O)C(=O)OC)[C@@H]([C@H]4C)CC)C(=C2C)C(=O)C', "
               "'Ketimine derived from a ketone'), "
               "('O=C1C(N=C2C(=O)C=3C=4C(=C(C)C=C(C4C2=O)O)C=5O[C@@H](C(C5C3O)(C)C)C)=C(O)C=6C(O)=CC(=C7C6C1=C(O)C=8C([C@@H](C)OC78)(C)C)C', "
               "'Ketimine derived from a ketone'), "
               "('[C@@H]1(N2C(N=C(C(=C2*)*)*)=*)O[C@H](COP(=O)([O-])*)[C@H](C1)O*', "
               "'Ketimine derived from a ketone'), "
               "('[H]C(=C1N=C(CC2NC(=O)C(CC)C2C)C(C)=C1CCC(O)=O)c1[nH]c(CC2NC(=O)C(C)C2CC)c(C)c1CCC(O)=O', "
               "'Ketimine derived from a ketone'), "
               "('O(C=1/C(/N=C(C1)C=2NC=CC2)=C/C=3NC(C)=C4C3[C@H](CCC4)C)C', "
               "'Ketimine derived from a ketone'), "
               "('CCCCN=C1C(=CC=C2C1=NC3(N2O)CCCCC3)[N+](=O)[O-]', 'Ketimine "
               "derived from a ketone'), "
               "('CO[C@H]1\\\\C=C\\\\O[C@@]2(C)Oc3c(C)c(O)c4C(=O)C(NC(=O)\\\\C(C)=C/C=C/[C@H](C)[C@H](O)[C@@H](C)[C@@H](O)[C@@H](C)[C@H](OC(C)=O)[C@@H]1C)=C1NC5(CCN(CC5)CC(C)C)N=C1c4c3C2=O', "
               "'Ketimine derived from a ketone'), "
               "('[Na+].CO\\\\N=C(/C(=O)N[C@H]1[C@H]2SCC([C@@H]3CCCO3)=C(N2C1=O)C([O-])=O)c1csc(N)n1', "
               "'Ketimine derived from a ketone'), "
               "('COC1=C(C=C(C=C1)CC(=O)NN=CC=CC2=CC(=CC=C2)[N+](=O)[O-])OC', "
               "'Ketimine derived from a ketone'), "
               "('C\\\\C=C1\\\\[C@@H](C)C(=O)N\\\\C\\\\1=C/C1=C(C)C(CCC([O-])=O)=C(N1)\\\\C=C1/N=C(/C=C2\\\\NC(=O)C(C=C)=C2C)C(C)=C1CCC([O-])=O', "
               "'Ketimine derived from a ketone'), "
               "('O(C=1C(N=C(C1)C=2NC=CC2)=CC=3NC(C)=C(C3)CCCCC(C)C)C', "
               "'Ketimine derived from a ketone'), "
               "('C=12[C@H]([C@@](CC([O-])=O)(C)C=3[N+]1[Ni-2]45N6C(C3)=C(C(CCC([O-])=O)=C6C=C7[N+]5=C(C=C8N4C(=C2)[C@]([C@@H]8CCC([O-])=O)(CC([O-])=O)C)C(=C7CCC([O-])=O)CC([O-])=O)CC([O-])=O)CCC([O-])=O', "
               "'Ketimine derived from a ketone'), "
               "('O=C(O)C(N=C1C(OC)=C(N)CC(C1)(O)COC2C(O)C(O)C(O)OC2CO)C(OC3C(O)C(O)C(O)OC3CO)C', "
               "'Ketimine derived from a ketone'), "
               "('CC1=C2[N+]3=C(C=C4N5C(=CC6=[N+]7C(Cc8c(CCC([O-])=O)c(CC([O-])=O)c1n8[Co--]357)=C(CCC([O-])=O)C6CC([O-])=O)[C@@H](CCC([O-])=O)[C@]4(C)CC([O-])=O)[C@@H](CCC([O-])=O)[C@]2(C)CC([O-])=O', "
               "'Ketimine derived from a ketone'), "
               "('O\\\\N=C1/Cc2cc(Br)c(Oc3cc(C\\\\C(C(=O)NCCc4ccc(Br)c(Oc5ccc(CCNC1=O)c(Br)c5O)c4)=N/O)cc(Br)c3O)c(Br)c2', "
               "'Ketimine derived from a ketone'), "
               "('CC1=C2[N+]3=C(C=C4N5C(=CC6=[N+]7C(=Cc8c(CCC(O)=O)c(CC(O)=O)c1n8[Co--]357)C(CCC(O)=O)=C6CC(O)=O)[C@@H](CCC(O)=O)[C@]4(C)CC(O)=O)[C@@H](CCC(O)=O)[C@]2(C)CC(O)=O', "
               "'Ketimine derived from a ketone'), "
               "('C(CCCCCCCCCC(O[C@@H]1CC=2[C@]([C@]3(CC[C@]4([C@]([C@@]3(CC2)[H])(CC[C@@]4([C@H](C)CCCC(C)C)[H])[H])C)[H])(C)CC1)=O)C=5N6[B-]([N+]7=C(C=CC7=CC6=CC5)C=8C=CC(=CC8)OC)(F)F', "
               "'Ketimine derived from a ketone'), "
               "('ClC=1C2=C(C(=O)N(C1C)/N=C(/C(=O)C)\\\\C)C(O)=C3C4=C(O)C=5C(=O)C6=C([C@H](OC)[C@@H](O)C[C@H]6OC)OC5C7=C4[C@@H](CC3=C2)OCO7', "
               "'Ketimine derived from a ketone'), "
               "('P(OCC(OCC)COCCCCCCCCCCCCCCCC)(OCC[N+]1=CC(=O)C(N(C)C)C=C1)[O-]', "
               "'Ketimine derived from a ketone'), "
               "('S1C(=NC(=C1)C(=O)NC(C(=O)NC(C(=O)N)=C)=C)C2=N[C@@H]3C=4N=C([C@@H]5NC(=O)C=6N=C([C@H](NC(=O)[C@H]7N=C(\\\\C(\\\\NC([C@@H](NC(C=8N=C([C@@]3(NC(=O)[C@H](NC(=O)C(NC(=O)C(NC(=O)[C@@H](C(C)C)N[C@H]9[C@@H](C=%10N=C(C(O[C@H]5C)=O)C=C(CO)C%10C=C9)O)=C)=C)C)CC2)SC8)=O)[C@@H](O)C)=O)=C\\\\C)SC7)[C@@](O)([C@@H](O)C)C)SC6)SC4', "
               "'Ketimine derived from a ketone'), ('N=C1C=CC(=O)C=C1', "
               "'Ketimine derived from a ketone'), "
               "('OC(=O)[C@@H]1N=C1\\\\C=C\\\\CCCCCCCCCC=C(Br)Br', 'Ketimine "
               "derived from a ketone'), "
               "('C=12N3C(=CC4=[N+]5C(=CC=6N7C=8C(=C9[N+](=C(C1)[C@H]([C@@H]9CCC(O)=O)C)[Mg-2]753)CC(C8C6*)=O)C(=C4C(O)O)C*)C(=C2C)C(O)C', "
               "'Ketimine derived from a ketone'), "
               "('C=12N3C(=CC4=[N+]5C(=CC=6N7C=8C(=C9[N+](=C(C1)[C@H]([C@@H]9CCC(O)=O)C)[Mg-2]735)[C@H](C(C8C6C)=O)C(=O)OC)C(=C4C)CC)C(=C2C)C(=O)C', "
               "'Ketimine derived from a ketone'), "
               "('[C@H](O)(CNC1=C(C(NC(N1)=O)=O)/N=C/C(=O)C)[C@@H]([C@@H](C)O)O', "
               "'Ketimine derived from a ketone'), "
               "('C1=CC(=CC(=C1)Cl)NN=C2C(=NN(C2=O)C(=S)N)C3=CC=C(C=C3)[N+](=O)[O-]', "
               "'Ketimine derived from a ketone'), "
               "('O1[C@@H]([C@H]([C@@H]([C@H]1OCCON=C(C(=O)N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@H](C(N[C@@H](CC(N)=O)C(N2[C@H](C(=O)N)CCC2)=O)=O)C(C)C)=O)C(C)C)=O)CC=3C=CC(=CC3)O)=O)[C@H](O)C)=O)[C@H](O)C)[H])O)O)CO[C@H]4O[C@@H]([C@H]([C@@H]4O)O[C@H]5O[C@@H]([C@H]([C@@H]5O[C@@H]6O[C@@H]([C@H]([C@@H]6O)O)CO)O)CO)CO[C@H]7O[C@@H]([C@H]([C@@H]7O[C@@H]8O[C@@H]([C@H]([C@@H]8O)O)CO)O)CO', "
               "'Ketimine derived from a ketone'), "
               "('C=12N3C(=CC4=[N+]5C(=CC=6N7C=8C(=C9[N+](=C(C1)[C@H]([C@@H]9CCC([O-])=O)C)[Mg-2]753)CC(C8C6CC)=O)C(=C4C)CC(C)C)C(=C2C)C=C', "
               "'Ketimine derived from a ketone'), "
               "('COCCCN=C1C(C(=O)C2=CC=CC=C2C1=O)Cl', 'Ketimine derived from "
               "a ketone'), "
               "('C1CCC(CC1)N=C2C(=CC=C3C2=NC4(N3O)CCCCC4)[N+](=O)[O-]', "
               "'Ketimine derived from a ketone'), "
               "('N1=C(C[C@@H](C1)O)C(O)=O', 'Ketimine derived from a "
               "ketone'), "
               "('O=C1N=CC(C2=CC=C(O)C=C2)=C3C1[C@H](O)[C@](C[C@H](C/C=C/C)C)(C)O3', "
               "'Ketimine derived from a ketone'), "
               "('Cc1c(C=C)c2C=C3[N+]4=C(C=c5c(CCC([O-])=O)c(C)c6=CC7=[N+]8C(=Cc1n2[Fe--]48n56)C(C=C)=C7C)[C@](O)(CCC([O-])=O)[C@@]3(C)O', "
               "'Ketimine derived from a ketone'), "
               "('O=C1NC(O)=C(C=C2C3=C(C=CC(=C3)CC=C(C)C)N=C2C(C=C)(C)C)NC1=O', "
               "'Ketimine derived from a ketone'), "
               "('CC1=NNC(=NC1=O)NN=C(C)C(=O)O', 'Ketimine derived from a "
               "ketone'), "
               "('O=C1NC(O)=C(C=C2C3=C(C=CC(=C3)C[C@H](O)C(O)(C)C)N=C2C(C=C)(C)C)NC1=O', "
               "'Ketimine derived from a ketone'), "
               "('C1[C@H](N=C(C(C1)(C)C)C(=O)[O-])C(=O)[O-]', 'Ketimine "
               "derived from a ketone'), "
               "('N[C@@H](CC1=C/[N+](=C\\\\C=C2C[C@H](NC(=C/2)C(O)=O)C(O)=O)/C=N1)C([O-])=O', "
               "'Ketimine derived from a ketone'), "
               "('CN1C2=NC3(CCCCC3)ON=C2C(=O)N(C1=O)C', 'Ketimine derived from "
               "a ketone'), "
               "('C1OC2=C(O1)C=C(C=C2)NN=C3C(=NN(C3=N)C4=CC=CC=C4)N', "
               "'Ketimine derived from a ketone'), "
               "('O=C1N(C(O)=C(C=C2C3=C(C=CC=C3)N=C2C(C=C)(C)C)NC1=O)C', "
               "'Ketimine derived from a ketone'), "
               "('O=C1OC=2C=3C(C(O)=C4C2C5(O)C(=O)CC(C)CC5(O[C@H]6O[C@@H]([C@H](O[C@H]7O[C@@H]([C@H](O)[C@@H](C7)O)C)[C@@H](C6)N(C)C)C)C=C4)=C(O)C(=CC3C1=C8C9=C(C=CC=C9)N=C8)[C@@H]%10O[C@@H]([C@@H](O)[C@@H](C%10)O)C', "
               "'Ketimine derived from a ketone'), "
               "('C[C@]1(CC(O)=O)[C@H](CCC(O)=O)C2=CC3=[N+]4C(Cc5c(CCC(O)=O)c(CC(O)=O)c6C=C7[N+]8=C(C=C1N2[Co--]48n56)[C@@H](CCC(O)=O)[C@]7(C)CC(O)=O)=C(CCC(O)=O)C3CC(O)=O', "
               "'Ketimine derived from a ketone'), "
               "('C/1(\\\\C(N(N=C1C2=CC=CC=C2)C3=CC=CC(=C3)C(O)=O)=O)=C\\\\C4=CC=C(C=C4)C5=CC=CC=C5', "
               "'Ketimine derived from a ketone'), "
               "('O(C1=C(NC(=C1)C=2NC=CC2)C3=C4N=C5CCCCCCCCC3C(C(C)C)C4=C5)C', "
               "'Ketimine derived from a ketone'), "
               "('C1=CC=CC(=C1)C=2OC(=CC2)/C=C/3\\\\C(N(N=C3C4=CC=CC=C4)C5=CC=CC(=C5)C(O)=O)=O', "
               "'Ketimine derived from a ketone'), "
               "('CC1=C(CCC(O)=O)\\\\C(/N=C1/C=C1NC(=O)C(C=C)=C/1C)=C\\\\c1[nH]c(\\\\C=C2NC(=O)C(C)=C/2C=C)c(C)c1CCC(O)=O', "
               "'Ketimine derived from a ketone'), "
               "('O(C1=C(NC(=C1)C=2NC=CC2)C(C=3NC=4CCCCCC[C@@H](C3C4)CCCC)=C5N=C(CCCCCCCCCCC)C=C5)C', "
               "'Ketimine derived from a ketone'), "
               "('O=NN/N=C/C=C/C=C/C=C/CCCC', 'Ketimine derived from a "
               "ketone'), ('C1C=CC=C2Sc3ccccc3N=C12', 'Ketimine derived from a "
               "ketone'), "
               "('N=1C2=C(C=CC=C2)C(C1)=C(C=3C4=C(C=CC=C4)NC3)C=5C6=C(C=CC=C6)NC5', "
               "'Ketimine derived from a ketone'), "
               "('CCCCCCCCCCCC1=CC=C(N1)\\\\C=C1/N=C(C=C1OC)C1=CC=CN1', "
               "'Ketimine derived from a ketone'), "
               "('COC(=O)[C@H]1C(=O)c2c(C)c3=CC4=N\\\\C(=C/c5c(C(C)=O)c(C)c6\\\\C=C7/N=C([C@@H](CCC(=O)OC\\\\C=C(/C)CCC[C@H](C)CCC[C@H](C)CCCC(C)C)[C@@H]7C)C1=c2n3[Mg]n56)[C@H](C)C/4=C/C', "
               "'Ketimine derived from a ketone'), "
               "('C1=CC=C(C=C1)C2=NN=CC2=CNNC(=O)C3=CC=CS3', 'Ketimine derived "
               "from a ketone'), "
               "('O=C(NC(C(=O)O)CC(=O)N)/C(=C/C=C/C=C/C=C/C=C/C=C/C(=C/[C@H]1N=C(/C=C/C=2NC=CC2)O[C@@H]1C)/C)/C', "
               "'Ketimine derived from a ketone'), "
               "('C1=2N3C(C=C4N5=C(C=C6N7C(=CC8=N(C(=C1)C(=C8CCC(O)=O)C)[Fe+]573)C(=C6C)CCC(O)=O)C(=C4C)C=C)=C(C2C)C=C', "
               "'Ketimine derived from a ketone'), "
               "('C1=CC=C2C(=C1)C=CC(=C2O)NN=C3C4=C(C=C(C=C4)[N+](=O)[O-])C(=CC3=O)S(=O)(=O)O', "
               "'Ketimine derived from a ketone'), ('O=C1N=CC=N1', 'Ketimine "
               "derived from a ketone'), "
               "('O(C(=O)CCC1C(C=2NC1=C3CC(=O)C=4C3=NC(C4C)=CC=5N=C(C=C6N=C(C2)C(=C6C=C)C)C(C5CC)=CO)C)C\\\\C=C(\\\\CC(CC(CCCC(CCCCC)C)C)C)/C', "
               "'Ketimine derived from a ketone'), "
               "('CC(=O)NC1=CC=C(C=C1)S(=O)(=O)NC2=C(NC3=CC=CC=C3N2)N=C4C=CC(=O)C(=C4)C(=O)O', "
               "'Ketimine derived from a ketone'), "
               "('C=12N3C(=CC4=[N+]5C(=CC=6N7C=8C(=C9[N+](=C(C1)[C@H]([C@@H]9CCC([O-])=O)C)[Mg-2]753)CC(C8C6*)=O)C(=C4C=O)C*)C(=C2C)C(O)C', "
               "'Ketimine derived from a ketone'), "
               "('O=C1NC(O)=C(C=C2C3=C(C=CC=C3)N=C2C(C=C)(C)C)NC1=O', "
               "'Ketimine derived from a ketone'), "
               "('C1CN(CCN1C2=CC=CC=N2)N=CC=CC3=CC=CC=C3', 'Ketimine derived "
               "from a ketone'), "
               "('COC1=C(Cc2c[nH]c3c(CC=C(C)C)cccc23)N2O[Fe-3]34(ON5C(Cc6c[nH]c7c(CC=C(C)C)cccc67)=C(OC)N=C(C)C5=[O+]3)(ON3C(Cc5c[nH]c6c(CC=C(C)C)cccc56)=C(OC)N=C(C)C3=[O+]4)[O+]=C2C(C)=N1', "
               "'Ketimine derived from a ketone'), "
               "('C=12N3C(=CC4=NC(=CC=5N(C=6C(=C7N=C(C1)[C@H]([C@@H]7CCC(O)=O)C)[C@H](C(C6C5C)=O)C(=O)OC)[Mg]3)C(=C4CO)CC)C(=C2C)C=C', "
               "'Ketimine derived from a ketone'), "
               "('O=C(NC(O)(C)C)C1C2(C(C3C(C4(C(N=C(O)C=C4)CC3)C)CC2)CC1)C', "
               "'Ketimine derived from a ketone'), "
               "('C=1(NC(/C=C/2\\\\NC(C(=C2C)C=C)=O)=C(C1C)C=C)/C=C/3\\\\N=C(\\\\C=C/4\\\\C(=C(C(N4)=O)C)CCC(O)=O)C(=C3C)CCC(O)=O', "
               "'Ketimine derived from a ketone'), "
               "('Nc1ccc(cc1)\\\\N=C1/C=C(N)\\\\C(\\\\C=C/1N)=N\\\\c1ccc(N)cc1', "
               "'Ketimine derived from a ketone'), ('C1=CC2N=c3ccccc3=C2C=C1', "
               "'Ketimine derived from a ketone'), "
               "('O=C(O)C1=C(N/N=C(\\\\C(=O)C)/C)C=CC=C1', 'Ketimine derived "
               "from a ketone'), "
               "('CCC1=C(C)\\\\C(NC1=O)=C\\\\c1[nH]c(\\\\C=C2/N=C(/C=C3\\\\NC(=O)[C@H](C)C3=CC)C(C)=C/2CCC(O)=O)c(CCC(O)=O)c1C', "
               "'Ketimine derived from a ketone'), "
               "('C1=CC(=CC(=C1C(=O)O)C=2OC(=CC2)/C=C/3\\\\C(N(N=C3C4=CC=CC=C4)C5=CC=C(C=C5)C(C)C)=O)Cl', "
               "'Ketimine derived from a ketone'), "
               "('O(C=1C(N=C(C1)C=2NC=CC2)=CC=3NC(C=4NC=CC4)=CC3OC)C', "
               "'Ketimine derived from a ketone'), "
               "('C1=2N3C(C=C4N5=C(C=C6N7C(=CC8=N(C(=C1)C(=C8CCC([O-])=O)C([H])=O)[Fe+]735)C(=C6C)CCC([O-])=O)C(=C4C)C=C)=C(C2C)[C@H](CCCC(C)CCCC(CCCC(C)C)C)O', "
               "'Ketimine derived from a ketone'), "
               "('CCC1=C(C)C(=O)N[C@H]1Cc1[nH]c(\\\\C=C2/N=C(C[C@H]3NC(=O)C(CC)=C3C)C(C)=C/2CCC(O)=O)c(CCC(O)=O)c1C', "
               "'Ketimine derived from a ketone'), "
               "('C=12[N+]3=C(C=C4N5C(=CC6=[N+]7C(=CC=8N(C(C1)=C(C8CCC([O-])=O)C)[Fe-2]537)C(=C6C)CCC(=O)[O-])[C@H]([C@@]4(CC(=O)[O-])C)CCC([O-])=O)[C@H]([C@@]2(CC([O-])=O)C)CCC([O-])=O', "
               "'Ketimine derived from a ketone'), "
               "('O=C1N[C@@](ON=C1[C@H](CC)C)(C(=O)OCC)[C@H](CC)C', 'Ketimine "
               "derived from a ketone'), "
               "('C1(NC(/C=C/2\\\\N=C(/C=C/3\\\\N\\\\C(=C/C4=NC(C(=C4CCC(O)=O)C)=O)\\\\C(=C3C)CCC(O)=O)C(=C2C)C=C)=C(C1C)C=C)=O', "
               "'Ketimine derived from a ketone')]\n"
               "False negatives: [('CC(=N)C(O)=O', 'No imine bonds found'), "
               "('C(=O)(C(=N)C[C@H](O)[C@H](O)CO)O', 'No imine bonds found')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 100,
    'num_true_negatives': 12403,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.9920031987205118}