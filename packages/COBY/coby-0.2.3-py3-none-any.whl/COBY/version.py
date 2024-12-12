__version__="0.2.3"

major_changes = [
]

minor_changes = [
    "Fragment definitions:",
    [
        "Added fragment definitions for the upcoming 'lipid task force' lipids. The documentation has also been updated with information about the fragments. Fragments are included for:",
        [
            "Phospholipids (with glycerol, ether and plasmalogen linkers)",
            "Triglycerides",
            "Diglycerides",
            "Monoglycerides",
            "Fatty acids",
            "Hydrocarbons",
            "Sphingolipids",
            "Cardiolipins",
            "Bis(monoacylglycero)phosphates (BMP)",
        ],
    ],
]

bug_fixes = [
    "Fixed errors that occured when reading certain charge designations from lipid scaffolds.",
]

tutorial_changes = [
]

documentation_changes = [
    "Updated the documentation to include information about all the added fragment difinitions as well as a few examples.",
    "Added an example to the 'Scaling imported structure coordinates', that was accidentally left out when the section was originally added.",
]

def version_change_writer(iterable, recursion_depth = 0):
    list_of_strings = []
    for i in iterable:
        if type(i) == str:
            if recursion_depth == 0:
                list_of_strings.append("    " * recursion_depth + i)
            else:
                list_of_strings.append("    " * recursion_depth + "-" + " " + i)

        elif type(i) in [list, tuple]:
            list_of_strings.extend(version_change_writer(i, recursion_depth + 1))
    return list_of_strings

### Extra empty "" is to add a blank line between sections
all_changes = []
if len(major_changes) > 0:
    all_changes += ["Major changes:", major_changes, ""]

if len(minor_changes) > 0:
    all_changes += ["Minor changes:", minor_changes, ""]

if len(bug_fixes) > 0:
    all_changes += ["Bug fixing:", bug_fixes, ""]

if len(documentation_changes) > 0:
    all_changes += ["Documentation changes:", documentation_changes, ""]

if len(tutorial_changes) > 0:
    all_changes += ["Tutorial changes:", tutorial_changes]

version_changes_list = version_change_writer(all_changes)
version_changes_str = "\n".join(version_changes_list)

def version_changes():
    print(version_changes_str)

### Abbreviation
changes = version_changes

