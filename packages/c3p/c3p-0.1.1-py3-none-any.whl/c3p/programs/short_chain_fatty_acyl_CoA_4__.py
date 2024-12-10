"""
Classifies: CHEBI:137040 short chain fatty acyl-CoA(4-)
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_short_chain_fatty_acyl_CoA_4__(smiles: str):
    """
    Determines if a molecule is a short chain fatty acyl-CoA(4-), defined as 'A fatty acyl-CoA(4-) arising from deprotonation
    of the phosphate and diphosphate OH groups of any short-chain fatty acyl-CoA; major species at pH 7.3'.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a short chain fatty acyl-CoA(4-), False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of CoA moiety
    coa_pattern = Chem.MolFromSmarts('C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12')
    match = mol.HasSubstructMatch(coa_pattern)
    if not match:
        return False, "CoA moiety not found"

    # Check for the presence of a short chain fatty acyl group
    fatty_acyl_pattern = Chem.MolFromSmarts('C(=O)C[C;H1]')
    match = mol.HasSubstructMatch(fatty_acyl_pattern)
    if not match:
        return False, "Short chain fatty acyl group not found"

    # Check for the presence of four negative charges
    charge = AllChem.GetFormalCharge(mol)
    if charge != -4:
        return False, f"Incorrect charge ({charge}), should be -4"

    return True, "Molecule is a short chain fatty acyl-CoA(4-)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:137040',
                          'name': 'short chain fatty acyl-CoA(4-)',
                          'definition': 'A fatty acyl-CoA(4-) arising from '
                                        'deprotonation of the phosphate and '
                                        'diphosphate OH groups of any '
                                        'short-chain fatty acyl-CoA; major '
                                        'species at pH 7.3.',
                          'parents': ['CHEBI:77636']},
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
               "[('[H][C@@](C)(CCC(=O)C(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@]1([H])CC[C@@]2([H])[C@]3([H])[C@H](O)C[C@]4([H])C[C@H](O)CC[C@]4(C)[C@@]3([H])C[C@H](O)[C@]12C', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC[C@H]1[C@@H]2CCC(=O)[C@@]2(C)CCC1=O', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)CC[C@@](C)([C@]4(CC[C@@]5([C@@]4(CC[C@@]6([C@]7(CCC(C=C7C=C[C@@]56[H])=O)C)[H])C)[H])[H])[H])=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('C[C@@H]([C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('C[C@H](CCC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('CC(C(C)=O)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)CC(=O)C=Cc1ccc(O)cc1', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)CC[C@@](C)([C@]4(CC[C@@]5([C@@]4([C@H](C[C@@]6([C@]7(CCC(C=C7CC[C@@]56[H])=O)C)[H])O)C)[H])[H])[H])=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)CC[C@@](C)([C@]4(CC[C@@]5([C@@]4(CC[C@@]6([C@]7(CCC(C=C7C[C@H]([C@@]56[H])O)=O)C)[H])C)[H])[H])[H])=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('C[C@@H](O[C@@H]1O[C@@H](C)[C@H](O)C[C@H]1O)C(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP([O-])([O-])=O)N3C=NC4=C(N)N=CN=C34', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('C(C[C@@H]([C@]([C@@]1([C@]2(CC[C@@]3([C@]4(CCC(C=C4CC[C@]3([C@@]2(CC1)[H])[H])=O)C)[H])C)[H])(C)[H])O)(=O)SCCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]5O[C@@H](N6C7=C(C(=NC=N7)N)N=C6)[C@@H]([C@@H]5OP([O-])([O-])=O)O)(=O)[O-])(=O)[O-])(C)C)O)=O', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('C[C@H](C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)C1(O)CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('C12=C(N=CN=C1N)N(C=N2)[C@@H]3O[C@@H]([C@@H](C3O)OP(=O)([O-])[O-])COP(=O)(OP(=O)(OCC([C@](C(NCCC(NCCSC(CCCCCCC[C@@H]4[C@@H](C(CC4)=O)C/C=C\\\\CC)=O)=O)=O)(O)[H])(C)C)[O-])[O-]', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('CC(C)(COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@@H](O)C(=O)NCCC(=O)NCCSC(=O)C1C(O)CCCC1=O', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('S(C(=O)CCCCC[C@@H]1[C@@H](C(C=C1)=O)C/C=C\\\\CC)CCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]2O[C@@H](N3C4=C(C(=NC=N4)N)N=C3)[C@@H]([C@@H]2OP([O-])([O-])=O)O)(=O)[O-])(=O)[O-])(C)C)O)=O', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('C[C@H](CCC[C@H](C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)CC[C@@](C)([C@]4(CC[C@@]5([C@@]4(CC[C@@]6([C@]7(CCC(C=C7C[C@@H]([C@@]56[H])O)=O)C)[H])C)[H])[H])[H])=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('C[C@@H]([C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)C=C[C@]4(C)[C@@]3(O)CC[C@]12C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('CC(C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)=C1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(CCC/C=C\\\\C/C=C\\\\CC(/C=C/C=C\\\\CCCCC)=O)=O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(C(C(CC\\\\C(=C\\\\CC4=C(C(=C5C(=C4O)C(OC5)=O)C)OC)\\\\C)=O)C)=O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('C[C@H](CCC=C(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('C[C@@H]([C@H]1CC[C@H]2[C@H](CCc3cc(O)ccc3C)C(=O)CC[C@]12C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('C[C@H](C=CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('C(/C=C/[C@]([C@@]1([C@]2(CC[C@@]3([C@]4(CCC(C=C4CC[C@]3([C@@]2(CC1)[H])[H])=O)C)[H])C)[H])(C)[H])(=O)SCCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]5O[C@@H](N6C7=C(C(=NC=N7)N)N=C6)[C@@H]([C@@H]5OP([O-])([O-])=O)O)(=O)[O-])(=O)[O-])(C)C)O)=O', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C(C(NCCC(NCCSC(=O)CC(=O)/C=C/C4=CC=C(C(=C4)OC)O)=O)=O)O)(C)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(CCC/C=C\\\\C/C=C\\\\C\\\\C=C/C=C/C(CCCCC)=O)=O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('CCCCCCCCCCCCCC(=O)C(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('C[C@@H]([C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)C=C[C@]4(C)[C@H]3CC[C@]12C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('COc1cc(C=CC(=O)CC(=O)SCCNC(=O)CCNC(=O)C(O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP([O-])([O-])=O)n2cnc3c(N)ncnc23)ccc1O', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('C(CC[C@]([C@@]1([C@]2([C@H](C[C@@]3([C@]4(CCC(C=C4C=C[C@]3([C@@]2(CC1)[H])[H])=O)C)[H])O)C)[H])(C)[H])(=O)SCCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]5O[C@@H](N6C7=C(C(=NC=N7)N)N=C6)[C@@H]([C@@H]5OP([O-])([O-])=O)O)(=O)[O-])(=O)[O-])(C)C)O)=O', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('S(C(CCCCCCC[C@@H]1[C@@H](C(C=C1)=O)C/C=C\\\\CC)=O)CCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]2O[C@@H](N3C4=C(C(=NC=N4)N)N=C3)[C@@H]([C@@H]2OP([O-])([O-])=O)O)(=O)[O-])(=O)[O-])(C)C)O)=O', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)C(C)C(CC[C@]([C@@]4([C@]5(CC[C@@]6([C@]7(CC[C@H](C[C@]7(C[C@H]([C@]6([C@@]5(CC4)[H])[H])O)[H])O)C)[H])C)[H])(C)[H])=O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('S(C(=O)CCCCC[C@@H]1[C@@H](C(CC1)=O)C/C=C\\\\CC)CCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]2O[C@@H](N3C4=C(C(=NC=N4)N)N=C3)[C@@H]([C@@H]2OP([O-])([O-])=O)O)(=O)[O-])(=O)[O-])(C)C)O)=O', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('C(C[C@H]([C@]([C@@]1([C@]2(CC[C@@]3([C@]4(CCC(C=C4CC[C@]3([C@@]2(CC1)[H])[H])=O)C)[H])C)[H])(C)[H])O)(=O)SCCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]5O[C@@H](N6C7=C(C(=NC=N7)N)N=C6)[C@@H]([C@@H]5OP([O-])([O-])=O)O)(=O)[O-])(=O)[O-])(C)C)O)=O', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('CC(C)CCCC(C)CCCC(C)CCC(=O)C(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)[C@H](C)CCC[C@]([C@@]4([C@]5(CC[C@@]6([C@]7(CCC(C=C7CC[C@]6([C@@]5(CC4)[H])[H])=O)C)[H])C)[H])(C)[H])=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('C(CC[C@]([C@@]1([C@]2([C@H](C[C@@]3([C@]4(CCC(C=C4C[C@H]([C@]3([C@@]2(CC1)[H])[H])O)=O)C)[H])O)C)[H])(C)[H])(=O)SCCNC(CCNC(=O)[C@@H](C(COP(OP(OC[C@H]5O[C@@H](N6C7=C(C(=NC=N7)N)N=C6)[C@@H]([C@@H]5OP([O-])([O-])=O)O)(=O)[O-])(=O)[O-])(C)C)O)=O', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('C[C@@H]([C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@@]3(O)CC[C@]12C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('C[C@@H]([C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C)C(=O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('C[C@H](CCCC(C)C(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12)[C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC(C)([C@H](C(NCCC(NCCSC(=O)CC(C(C)C)=O)=O)=O)O)C)(=O)[O-])(=O)[O-])[C@H]([C@H]1O)OP([O-])([O-])=O', "
               "'Molecule is a short chain fatty acyl-CoA(4-)'), "
               "('CC1=CC(=O)[C@H](CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]2O[C@H]([C@H](O)[C@@H]2OP([O-])([O-])=O)n2cnc3c(N)ncnc23)C1(C)C', "
               "'Molecule is a short chain fatty acyl-CoA(4-)')]\n"
               'False negatives: '
               "[('C[C@H](O)CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP([O-])(=O)OP([O-])(=O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1OP([O-])([O-])=O)n1cnc2c(N)ncnc12', "
               "'Short chain fatty acyl group not found')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 90882,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.9989008935735247}