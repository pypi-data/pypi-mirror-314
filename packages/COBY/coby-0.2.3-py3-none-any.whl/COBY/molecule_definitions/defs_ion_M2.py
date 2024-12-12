ion_defs     = {}

############
### IONS ###
############
params = "M2"
ion_defs[params] = {}
ion_defs[params]["positive"] = {
    ### Monovalent
    "NA":   {"beads": [{"name": "NA+",  "x": 0, "y":  0, "z": 0, "charge": 1}]},
    "NC3+": {"beads": [{"name": "NC3",  "x": 0, "y":  0, "z": 0, "charge": 1}]},
    ### Divalent
    "CA+":  {"beads": [{"name": "CA+",  "x": 0, "y":  0, "z": 0, "charge": 1}]},
}

ion_defs[params]["negative"] = {
    ### Monovalent
    "CL":   {"beads": [{"name": "CL-",  "x": 0, "y":  0, "z": 0, "charge": -1}]},
}
