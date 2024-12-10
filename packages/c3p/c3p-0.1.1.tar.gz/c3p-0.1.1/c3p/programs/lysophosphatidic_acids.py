"""
Classifies: CHEBI:32957 lysophosphatidic acids
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_lysophosphatidic_acids(smiles: str):
    """
    Determines if a molecule is a lysophosphatidic acid, defined as:
    Any monoacylglycerol phosphate obtained by hydrolytic removal of one of the two acyl groups of any phosphatidic acid or derivatives therein.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a lysophosphatidic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a phosphate group
    has_phosphate = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'P' and atom.GetTotalDegree() == 4:
            has_phosphate = True
            break

    if not has_phosphate:
        return False, "No phosphate group found"

    # Check for the presence of a glycerol moiety
    has_glycerol = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetTotalDegree() == 2:
            neighbors = [mol.GetAtomWithIdx(neighbor.GetIdx()) for neighbor in atom.GetNeighbors()]
            if len(neighbors) == 2 and all(neighbor.GetSymbol() == 'C' for neighbor in neighbors):
                carbon_neighbors = [mol.GetAtomWithIdx(neighbor.GetIdx()) for neighbor in neighbors[0].GetNeighbors() if neighbor.GetIdx() != atom.GetIdx()]
                if len(carbon_neighbors) == 2 and all(neighbor.GetSymbol() == 'C' for neighbor in carbon_neighbors):
                    has_glycerol = True
                    break

    if not has_glycerol:
        return False, "No glycerol moiety found"

    # Check for the presence of a single acyl chain
    acyl_chains = []
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.SINGLE and bond.GetBeginAtom().GetSymbol() == 'C' and bond.GetEndAtom().GetSymbol() == 'O':
            acyl_chain = []
            atom = bond.GetBeginAtom()
            while atom.GetSymbol() == 'C' and atom.GetTotalDegree() <= 3:
                acyl_chain.append(atom.GetIdx())
                neighbors = [mol.GetAtomWithIdx(neighbor.GetIdx()) for neighbor in atom.GetNeighbors() if neighbor.GetIdx() not in acyl_chain]
                if len(neighbors) == 1:
                    atom = neighbors[0]
                else:
                    break
            acyl_chains.append(acyl_chain)

    if len(acyl_chains) != 1:
        return False, "Incorrect number of acyl chains found"

    return True, "Molecule is a lysophosphatidic acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:32957',
                          'name': 'lysophosphatidic acids',
                          'definition': 'Any monoacylglycerol phosphate '
                                        'obtained by hydrolytic removal of one '
                                        'of the two acyl groups of any '
                                        'phosphatidic acid or derivatives '
                                        'therein.',
                          'parents': ['CHEBI:16961']},
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
    'num_false_positives': 16,
    'num_true_negatives': 183849,
    'num_false_negatives': 7,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9998749129829446}