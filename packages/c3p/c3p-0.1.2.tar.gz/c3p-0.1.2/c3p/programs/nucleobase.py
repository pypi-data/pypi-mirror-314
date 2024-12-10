"""
Classifies: CHEBI:18282 nucleobase
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_nucleobase(smiles: str):
    """
    Determines if a molecule is a nucleobase.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a nucleobase, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define the nucleobase SMARTS patterns
    purine_pattern = "[r5]1([r5,r6])c([r5,r6])nc([r5,r6])c1[r5,r6]"
    pyrimidine_pattern = "[r5,r6]c1[r5,r6]c([r5,r6])c(=O)[r5,r6]c(=O)[r5,r6]1"
    cytosine_pattern = "Nc1cc[nH]c(=O)n1"
    thymine_pattern = "Cc1c[nH]c(=O)[nH]c1=O"

    purine_query = Chem.MolFromSmarts(purine_pattern)
    pyrimidine_query = Chem.MolFromSmarts(pyrimidine_pattern)
    cytosine_query = Chem.MolFromSmarts(cytosine_pattern)
    thymine_query = Chem.MolFromSmarts(thymine_pattern)

    # Check if the molecule matches the nucleobase SMARTS patterns
    is_purine = mol.HasSubstructMatch(purine_query)
    is_pyrimidine = mol.HasSubstructMatch(pyrimidine_query)
    is_cytosine = mol.HasSubstructMatch(cytosine_query)
    is_thymine = mol.HasSubstructMatch(thymine_query)

    if is_purine:
        return True, "Molecule is a purine nucleobase"
    elif is_pyrimidine:
        return True, "Molecule is a pyrimidine nucleobase"
    elif is_cytosine:
        return True, "Molecule is cytosine"
    elif is_thymine:
        return True, "Molecule is thymine"
    else:
        return False, "Molecule is not a nucleobase"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18282',
                          'name': 'nucleobase',
                          'definition': 'That part of DNA or RNA that may be '
                                        'involved in pairing.',
                          'parents': ['CHEBI:38101']},
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
               "[('O=C1C(=O)C2=C(NC3=C2C=CC=C3)C(=C1C)CC(C)C', 'Molecule is a "
               "purine nucleobase'), "
               "('COc1ccc2c(c1)[nH]c1c(CC=C(C)C)c(O)c(C=O)cc21', 'Molecule is "
               "a purine nucleobase'), "
               "('C1=CC=C(C=C1)C2=C(N3C(=O)C(=CC4=CC(=CC=C4)O)SC3=N2)C5=CC=CC=C5', "
               "'Molecule is a purine nucleobase'), "
               "('O=C(C1=NC2=C(C(=C(CCCCC(C)C)C3=C2C4=C(C=CC=C4)N3)C)O[C@H]1C=5C6=C(C=CC=C6)NC5)C', "
               "'Molecule is a purine nucleobase'), "
               "('O=C1C2=C3C(C=4C[C@H]5[C@](C4N3[C@H]1C(=C)C)([C@@]6([C@H]([C@](/C=C/C=C(/C(=O)O)\\\\C)([C@@H](O)CC6)C)CC5)C)C)=CC7=C2[C@@H](O)[C@@H]8C(OC(C=C78)(C)C)(C)C', "
               "'Molecule is a purine nucleobase'), "
               "('O1C2C3N4C(CC(C3C1)C(C4)=CC)C=5NC6=C(C25)C=CC(OC)=C6', "
               "'Molecule is a purine nucleobase'), "
               "('O=C1C=C2C(=CC[C@]3([C@@]2(O)CC[C@@H]4[C@@]3(C=5NC=6C=C7C8=CC(OC([C@H]8CC7=CC6C5C4)(C)C)(C)C)C)C)O[C@@H]1C(O)(C)C', "
               "'Molecule is a purine nucleobase'), "
               "('CN1C2=C(C=CC(=C2)OC)C3=C1[C@H](N(CC34CCN(CC4)CC5CCCC5)CC6=NC=CS6)CO', "
               "'Molecule is a purine nucleobase'), "
               "('CN1C2=C(C=CC(=C2)OC)C3=C1[C@@H](N(CC34CCN(CC4)C(=O)C5=CC(=CC=C5)F)CC6CC6)CO', "
               "'Molecule is a purine nucleobase'), "
               "('O=C1C(=O)C2=C(NC3=C2C=CC=C3)C(=C1C)CCCCCCC(C)C', 'Molecule "
               "is a purine nucleobase'), "
               "('COc1ccc2c(c1)[nH]c1c(O)cc(C=O)cc21', 'Molecule is a purine "
               "nucleobase'), "
               "('O=C1N2[C@]3(CC4[C@@]1(NC3=O)C(=O)C5=C(N(O)C6=C5C=CC=7OC(C=CC67)(C)C)C4(C)C)CCC2', "
               "'Molecule is a purine nucleobase'), "
               "('O=C(O)C(=O)C1=C2NC=3C=CC=CC3C2=CC4=C1C5=C(C=CC=C5)N4', "
               "'Molecule is a purine nucleobase'), "
               "('CC(O)C1CCc2c3C=CC(=O)c4c(O)c5C(C)OC(CC(O)=O)Cc5c(n12)c34', "
               "'Molecule is a purine nucleobase'), "
               "('O=C1C=C2[C@@]3(CC[C@]4([C@H]2CC[C@@H]5[C@@]4(C=6NC=7C=CC(=CC7C6C5)C(C=C)(C)C)C)C)O[C@@H]1C(O3)(C)C', "
               "'Molecule is a purine nucleobase'), "
               "('C=Cc1cncc2c1cc1-c3[nH]c4ccccc4c3CCn1c2=O', 'Molecule is a "
               "purine nucleobase'), ('CC1(C)[C@@H](O)C(=O)c2c1[nH]c1ccccc21', "
               "'Molecule is a purine nucleobase'), "
               "('O=C1[C@]23C=4N(C=5C2=CC=CC5)C(=O)C=CC4[C@@](C1)(/C(/CN(CC3)C)=C\\\\CO)[H]', "
               "'Molecule is a purine nucleobase'), "
               "('CCC(=O)N1CC2(CCN(CC2)CC3=CC=CC=C3Cl)C4=C([C@H]1CO)NC5=C4C=CC(=C5)OC', "
               "'Molecule is a purine nucleobase'), "
               "('O=C(O[C@@H]1[C@]([C@H]2[C@]([C@]3(C=4NC=5C=CC=CC5C4C[C@@H]3C[C@H]2O)C)(C)CC1)(CCC=C(C)C)C)C', "
               "'Molecule is a purine nucleobase'), "
               "('O=C1N[C@]23[C@H](C(C=4NC5=C(C4C2)C=CC6=C5C(=O)CC(O6)(C)C)(C)C)C[C@]17N(CC[C@@H]7C)C3', "
               "'Molecule is a purine nucleobase'), "
               "('COC1=CC2=C(C=C1)C3=C(N2)[C@@H](N(CC34CCN(CC4)CC5=CC(=CC=C5)F)C(=O)C6CCOCC6)CO', "
               "'Molecule is a purine nucleobase'), "
               "('S=C=N[C@H]1[C@](C=C)(CC[C@H]2[C@H]1C=3C4=C(C=CC=C4)NC3C2(C)C)C', "
               "'Molecule is a purine nucleobase'), "
               "('O=C1N2[C@@]3(C(=O)NC14C(C(C5=[N+]([O-])C6=C(C75[C@@H]4N8C(=O)[C@@]9%10N(CCC9)C(C8%11C(C(C)(C)C%12=C([C@H]7%11)C%13=C(C%14=C(OC(C)(C)C=C%14)C=C%13)N%12)C%10)=O)C=CC%15=C6C=CC(O%15)(C)C)(C)C)C3)CCC2', "
               "'Molecule is a purine nucleobase'), "
               "('COC1=CC2=C(C=C1)C3=C(N2)[C@@H](N(CC34CCN(CC4)CC5=CN=CC=C5)CC6=NC=CS6)CO', "
               "'Molecule is a purine nucleobase'), "
               "('COc1cc(C=O)cc2c3ccccc3[nH]c12', 'Molecule is a purine "
               "nucleobase'), "
               "('CCOC1=CC2=C(C=C1)NC3=C2N=CN=C3NCCC4=CC(=C(C=C4)OC)OC', "
               "'Molecule is a purine nucleobase'), "
               "('ClC1=CC2=C(N(C)C[C@]23C=4NC=5C=CC=CC5C4C=6C3=C(NC6)C(=O)OC)C=C1', "
               "'Molecule is a purine nucleobase'), "
               "('OC=1C=C2NC=3C(C2=CC1C(OC)=O)=CC=CC3', 'Molecule is a purine "
               "nucleobase'), ('O(C1=C(O)C2=C(NC3=C2C=C(OC)C=C3)C(=C1C)C)C', "
               "'Molecule is a purine nucleobase'), "
               "('ClC1=C2N(C=3C=4NC=5C(Cl)=CC=CC5C4C6=C(C3C2=CC(=C1)OC)C(=O)NC6=O)[C@@H]7O[C@@H]([C@@H](OC)[C@@H]([C@H]7O)O)CO', "
               "'Molecule is a purine nucleobase'), "
               "('ClC1=CC2=C(NC3=C2C=C(C(=O)O[C@H]4[C@@H](N)[C@H](O[C@H](C4)O[C@H]5[C@@](O)(C[C@H](O[C@@H]6[C@@H](O[C@H](OC7C8C=CC9CC(O)C(CC%10(C=C(C(C%11(C(C(=C(C9(C8CCC7)C)O)C(=O)N%11)=O)C%10)C)C(=O)O)C)CC)CC6)C)O[C@@H]5C)C)C)N3)C=C1', "
               "'Molecule is a purine nucleobase'), "
               "('Cl[C@H]1[C@](C(C#N)=C2C=3C4=C(C=CC=C4)NC3C([C@H]2C1)(C)C)(C=C)C', "
               "'Molecule is a purine nucleobase'), "
               "('O=C1NCC=2C1=C3C=4N([C@@H]5OC(C)=C([C@@](N6C4C2C7=C6C=CC=C7)(OC)C5)OC)C8=C3C=CC=C8', "
               "'Molecule is a purine nucleobase'), "
               "('ClC1=C2C3=C4C=5[C@@](OC([C@@]6([C@@]3([C@](C6)(C(C2)=C)[H])[H])[H])(C)C)([C@]7([C@@]([C@@]8([C@](O)([C@@]9%10O[C@@]9([C@@H](O)[C@H](O[C@]%10(CC8)[H])C(C)=C)[H])CC7)C)(C5NC4=C1)C)[H])[H]', "
               "'Molecule is a purine nucleobase'), "
               "('O=C1C=2NC=3C=CC=CC3C2C(=C1C4=C(NC5=C4C=CC=C5)/C(/C(=O)OC)=C\\\\C6=CC=C(O)C=C6)C(=O)OC', "
               "'Molecule is a purine nucleobase'), "
               "('CN1C2=C(C=CC(=C2)OC)C3=C1[C@@H](N(CC34CCN(CC4)C(=O)CC5=CC=NC=C5)CC6=CC=NC=C6)CO', "
               "'Molecule is a purine nucleobase'), "
               "('O[C@]12[C@@]([C@@]3([C@@H](CC1)CC4=C3NC5=C4C=C6C(=C5)C=7[C@H](C6)C(OC(C7)(C)C)(C)C)C)(CC[C@@H]8O[C@@H]([C@H](OC(=O)C)C=C28)C(O)(C)C)C', "
               "'Molecule is a purine nucleobase'), "
               "('CC[C@@]1(CN2CCC=3C4=CC=CC=C4NC3[C@@]2(C[C@@]1(CC=O)[H])[H])[H]', "
               "'Molecule is a purine nucleobase'), "
               "('CC1=CC=C(C=C1)S(=O)(=O)N2CCC3(CC2)CN[C@@H](C4=C3C5=C(N4C)C=C(C=C5)OC)CO', "
               "'Molecule is a purine nucleobase'), "
               "('CC(=O)c1nc(C(N)=O)c(O)c2c3ccccc3[nH]c12', 'Molecule is a "
               "purine nucleobase'), ('CC1(C)C(=O)C(=O)c2c1[nH]c1cc(O)ccc21', "
               "'Molecule is a purine nucleobase'), "
               "('CCC(=O)N1CCC2(CC1)CN([C@H](C3=C2C4=C(N3)C=C(C=C4)OC)CO)S(=O)(=O)C5=CC=CC=C5', "
               "'Molecule is a purine nucleobase'), "
               "('O=C1NC(=O)C2=C1C3=C(N([C@@H]4O[C@@H]([C@@H](O)[C@@H]([C@H]4O)O)CO)C5=C3C=CC=C5)C6=C2C7=C(C=CC=C7)N6', "
               "'Molecule is a purine nucleobase'), "
               "('CC1=C2C3=C(C=CC(=C3)[N+](=O)[O-])NC2=C(C=C1)C', 'Molecule is "
               "a purine nucleobase'), "
               "('C=C[C@]1(CN2CCC=3C=4C=CC(=CC4NC3[C@@]2(C[C@@]1(C[C@@]5(C6=C(CCN5C)C7=CC=CC=C7N6)[H])[H])[H])O)[H]', "
               "'Molecule is a purine nucleobase'), "
               "('COc1ccc(cc1O)-c1c2c3cc(OC)c(OS(O)(=O)=O)cc3oc(=O)c2n2ccc3cc(OC)c(OC)cc3c12', "
               "'Molecule is a purine nucleobase'), "
               "('O=C1N2[C@H](C(=O)N3[C@]1(O)[C@@H](OC)C=4C5=C(C=C(OC)C=C5)NC4[C@@H]3CC(O)(C)C)CCC2', "
               "'Molecule is a purine nucleobase'), "
               "('CN1C2=C(C=CC(=C2)OC)C3=C1[C@H](N(CC34CCN(CC4)C(=O)NC5CCCC5)CC6CC6)CO', "
               "'Molecule is a purine nucleobase'), "
               "('CN(C)CC(=O)N1CCC2(CC1)CN([C@@H](C3=C2C4=C(N3)C=C(C=C4)OC)CO)C(=O)C5=CN=CC=C5', "
               "'Molecule is a purine nucleobase'), "
               "('N1=C(C=2NC=3C=CC=CC3C2CC1)C=4C5=C(C=CC=C5)NC4', 'Molecule is "
               "a purine nucleobase'), "
               "('OCc1ccc(o1)-c1nc(cc2c3ccccc3[nH]c12)C(O)=O', 'Molecule is a "
               "purine nucleobase'), "
               "('COC1=CC2=C(C=C1)NC3=C2NC=[N+](C3=O)CCCN4CCOCC4', 'Molecule "
               "is a purine nucleobase'), ('C[C@H]1NCCc2c1[nH]c1ccccc21', "
               "'Molecule is a purine nucleobase'), "
               "('O=C1N(CC=2C1=C3C=4N([C@@H]5O[C@](N6C4C2C7=C6C=CC=C7)([C@H](OC)\\\\C(\\\\C5)=N\\\\O)C)C8=C3C=CC=C8)COC', "
               "'Molecule is a purine nucleobase'), "
               "('CN1C2=C(C=CC(=C2)OC)C3=C1[C@H](N(CC34CCN(CC4)C(=O)COC)CC5=C(C=CC(=C5)F)F)CO', "
               "'Molecule is a purine nucleobase'), "
               "('ClC1=C2C3=C4C=5[C@@H](OC([C@@H]6[C@]3(O)[C@H](C6)C(C2)=C)(C)C)O[C@@]7([C@](C5NC4=C1)([C@@]8(C([C@@]9%10O[C@@H]9[C@@H](O)[C@H](OC%10CC8)C(=C)C)CC7)C)C)O', "
               "'Molecule is a purine nucleobase'), "
               "('[H][C@]12CC[C@H](O)[C@H](C(=O)OC)[C@@]1([H])C[C@]1([H])N(CCc3c1[nH]c1ccccc31)C2', "
               "'Molecule is a purine nucleobase'), "
               "('O=C1N2[C@@]3(C(=O)N[C@]14C(=O)C=5C6=C(C7=C(OC(C)(C)C=C7)C=C6)N(C5C([C@@H]4C3)(C)C)O)CCC2', "
               "'Molecule is a purine nucleobase'), "
               "('O(C1=C(O)C2=C(NC3=C2C=C(CC=C(C)C)C=C3)C(=C1C)C[C@H](O)C)C', "
               "'Molecule is a purine nucleobase'), "
               "('O=C(OCC)C[C@@H]1OCCC2=C1NC=3C(=CC=CC23)CC', 'Molecule is a "
               "purine nucleobase'), ('S1C=2N(OC)C=3C(C2CN=C1S(=O)C)=CC=CC3', "
               "'Molecule is a purine nucleobase'), "
               "('O=C(O)[C@]1([C@H]2[C@@](OC=3C=C4C5=C(C=CC=C5)NC4=CC3CC2)(CC[C@@H]1O)C)C', "
               "'Molecule is a purine nucleobase'), "
               "('O=C1C2=C(C3=C(NC4=C3C[C@@H]5CC[C@@]6([C@@]([C@@]45C)(CC[C@H]7[C@@]68O[C@@H]8[C@@H]9O[C@H](C=C(C)C)OC([C@H]9O7)(C)C)C)O)C=C2)C[C@@H]%10[C@H]1C(OC%10(C)C)(C)C', "
               "'Molecule is a purine nucleobase'), "
               "('CC1(C)[C@@H](O)C(=O)c2c1[nH]c1cc(O)ccc21', 'Molecule is a "
               "purine nucleobase'), "
               "('O=C(O)C1=NC(=C2NC3=C(C2=C1)C=CC=C3)C(=O)CCCC(C)C', 'Molecule "
               "is a purine nucleobase'), "
               "('BrC1=C2C3=C4C=5[C@@H](OC([C@@H]6[C@]3(O)[C@H](C6)C(C2)=C)(C)C)[C@@H]7CC[C@@]8([C@@]([C@]7(C5NC4=C1)C)(CC[C@H]9[C@@]8%10O[C@@H]%10[C@@H](O)[C@H](O9)C(=C)C)C)O', "
               "'Molecule is a purine nucleobase'), "
               "('C=C[C@H]1CN2CCc3c([nH]c4ccccc34)[C@@H]2C[C@@H]1CC=O', "
               "'Molecule is a purine nucleobase'), "
               "('ClC1=C2C3=C4C=5[C@@H](OC([C@@H]6[C@]3(O)[C@H](C6)C(C2)=C)(C)C)[C@]7(O)CC[C@@]8([C@@]([C@]7(C5NC4=C1)C)(CC[C@H]9[C@@]8%10O[C@@H]%10[C@@H](O)[C@H](O9)C(=C)C)C)O', "
               "'Molecule is a purine nucleobase'), "
               "('ClC1=CC=2C=3C=4C(=CNC4)[C@@]5(C=6C=C(Cl)C=CC6N([C@@H]5C3NC2C=C1)C)C', "
               "'Molecule is a purine nucleobase'), "
               "('O=c1n2CCc3cccc(c23)c2[nH]c3ccccc3c12', 'Molecule is a purine "
               "nucleobase'), ('COc1ccc2[nH]c3c(Cc4ccc(O)cc4)nccc3c2c1', "
               "'Molecule is a purine nucleobase'), "
               "('COC1=CC2=C(C=C1)C3=C(N2)[C@H](N(CC34CCN(CC4)CC5=CN=CC=C5)C(=O)C6=CC=C(C=C6)F)CO', "
               "'Molecule is a purine nucleobase'), "
               "('CC1(C2=C(C[C@@H]3N1C(=O)N(C3=O)CC4=CC(=CC=C4)F)C5=CC=CC=C5N2)C', "
               "'Molecule is a purine nucleobase'), "
               "('CCCNC(=O)N1CCC2(CC1)CN([C@H](C3=C2C4=C(N3)C=C(C=C4)OC)CO)C(=O)COC', "
               "'Molecule is a purine nucleobase'), "
               "('CC1=NN2C(=C3C(=C2C(=C1)C4=CC=CC=C4)N(C(=O)N(C3=O)C)C)C5=CC=CC=C5', "
               "'Molecule is a purine nucleobase'), "
               "('O(CC(CNC(C)C)O)C=1C=2C=3C(NC2C=CC1)=CC=CC3', 'Molecule is a "
               "purine nucleobase'), "
               "('BrC1=C2N(C=3C=4NC=5C(Br)=CC=CC5C4C6=C(C3C2=CC=C1)C(=O)NC6=O)C7OC(C(OC)C(C7O)O)CO', "
               "'Molecule is a purine nucleobase'), "
               "('O=C(OCC1=NC(=C2NC3=C(C2=C1)C=CC=C3)[C@@H](O)COC(=O)C)C', "
               "'Molecule is a purine nucleobase'), "
               "('O1[C@H](C(O)(C)C)[C@@H](O)[C@@H]2[C@]3([C@@H]1CC[C@]4([C@@]3(O)CC[C@@H]5[C@@]4(C=6NC=7C=CC=C(C7C6C5)CC=C(C)C)C)C)O2', "
               "'Molecule is a purine nucleobase'), "
               "('O=C1N2C=3[C@@]4([C@]5(N(CC4)C[C@H]([C@](C5)(C3C=C1C(OCC)=O)[H])CC)[H])C=6C2=CC=CC6', "
               "'Molecule is a purine nucleobase'), "
               "('O[C@]12[C@@]([C@@]3([C@@](CC1)(CC4=C3NC5=C4C=C(C(=C5)CC=C(C)C)CC=C(C)C)[H])C)(CC[C@@]6(O[C@@](C(=O)C=C26)(C(O)(C)C)[H])[H])C', "
               "'Molecule is a purine nucleobase'), "
               "('O(C1=C(OC)C2=C(NC3=C2C=CC=C3)C(=C1C)C)C', 'Molecule is a "
               "purine nucleobase'), "
               "('O1[C@@]2(N3C4=C5N([C@]1(C[C@@H](N)[C@H]2O)[H])C=6C(C5=C7C(=C4C=8C3=CC=CC8)CNC7=O)=CC=CC6)C', "
               "'Molecule is a purine nucleobase'), "
               "('O=C1[C@@](O)([C@](O)(C=2NC3=C(C2C1)C=CC=C3)C)C', 'Molecule "
               "is a purine nucleobase'), "
               "('COC1=CC2=C(C=C1)C3=C(N2)[C@@H](N(CC34CCN(CC4)CC5CCCC5)C(=O)CN6CCOCC6)CO', "
               "'Molecule is a purine nucleobase'), "
               "('O1C(C=2NC=3C=CC=CC3C2CC1)(C)C', 'Molecule is a purine "
               "nucleobase'), "
               "('COC(=O)CC(O)N(C)C(=O)c1cc2c3ccccc3[nH]c2c(n1)C(C)=O', "
               "'Molecule is a purine nucleobase'), "
               "('CCC(=O)N1CC2(CCN(CC2)CC3=CC=CC=C3Cl)C4=C([C@@H]1CO)NC5=C4C=CC(=C5)OC', "
               "'Molecule is a purine nucleobase'), "
               "('Brc1ccc2[nH]c3cnccc3c2c1', 'Molecule is a purine "
               "nucleobase'), "
               "('COc1c2-c3[nH]c4ccc(Cl)cc4c3[C@@]3(O)C(=O)N(C)C(=O)[C@@]3(O)n2c2ccc(Cl)cc12', "
               "'Molecule is a purine nucleobase'), "
               "('CC[C@H]1C[C@@H]2CN3CCc4c([nH]c5c([C@H]6CC[C@H]7NCCc8c7n6c6ccccc86)c(O)ccc45)[C@](C2)([C@H]13)C(=O)OC', "
               "'Molecule is a purine nucleobase'), "
               "('CN1C2=C(C=CC(=C2)OC)C3=C1[C@@H](N(CC34CCN(CC4)C(=O)C5=CC=CC=C5F)C(=O)NC6=CC=C(C=C6)F)CO', "
               "'Molecule is a purine nucleobase'), "
               "('CCN1CCN2C3=C(CCCC31)C4=C2C(=CC=C4)C', 'Molecule is a purine "
               "nucleobase'), "
               "('C1CCC(CC1)C2C3=C(CCN2CC4=NC=CN4)C5=CC=CC=C5N3', 'Molecule is "
               "a purine nucleobase'), "
               "('O1C(OC2=CC=3C=4CCN(C4NC3C=C2)C(=O)C)C(O)C(O)C(O)C1C(O)=O', "
               "'Molecule is a purine nucleobase'), "
               "('[C@H]12N3C=4N=C(NC(C4N=C3[C@H]([C@]([C@H](C1)O)(O2)[H])OP(O)(O)=O)=O)N', "
               "'Molecule is a purine nucleobase'), "
               "('[C@H]12N3C=4N=CN=C(C4N=C3[C@H]([C@]([C@H](C1)O)(O2)[H])O)N', "
               "'Molecule is a purine nucleobase'), "
               "('[H][C@]12C[C@@H](OC(=O)c3cc(OC)c(OC)c(OC)c3)[C@H](OC)[C@@H](C(=O)OC)[C@@]1([H])C[C@@]1([H])N(CCc3c1[nH]c1cc(OC)ccc31)C2', "
               "'Molecule is a purine nucleobase'), "
               "('O=C1C(=O)C2=C(NC3=C2C=C(CC4=C(CC(C)(C)CC4)C)C=C3)C(=C1C)C[C@H](O)C', "
               "'Molecule is a purine nucleobase')]\n"
               "False negatives: [('Nc1cc[nH]c(=O)n1', 'Molecule is not a "
               "nucleobase')]",
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 12668,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.9921685331662621}