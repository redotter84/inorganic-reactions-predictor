# list of acids that I know
db_iAc = [ "HBO2", "H3BO3", "H2B4O7", "H2CO3", "HCN", "HCNO", "HNO2", "HNO3", "HF", "H2SiO3", "HPO2", "HPO3", "H4P2O7", "H3PO4", "H2S", "H2SO3", "H2SO4", "HCl", "HClO", "HClO2", "HClO3", "HClO4", "H2CrO4", "H2Cr2O7", "HAsO2", "H3AsO3", "H3AsO4", "H2Se", "H2SeO3", "H2SeO4", "HBr", "HBrO", "HBrO2", "HBrO3", "HBrO4", "HSbO3", "H2Te", "H2TeO3", "H2TeO4", "HI", "HIO", "HIO2", "HIO3", "HIO4"]

db_acid_react = [ "HClO4", "HI", "HBr", "H2SO4", "HCl", "HNO3", "H3PO4", "H2SO3", "HF", "HNO2", "H2CO3", "H2S", "H2SiO3", "H3BO3"]

# standalone anions
ans: 'list(str)' = list(map(lambda x: x[2 : ] if x[1].isdigit() else x[1 : ], db_iAc))
# standalone oxidation states of anions
oxs: 'list(int)' = list(map(lambda x: int(x[1]) if x[1].isdigit() else 1, db_iAc))

# list of anions of acids with oxidation states
db_anions = dict(zip(ans, oxs))
