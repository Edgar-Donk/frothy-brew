with open("entry_class_3.py", "r") as f:
    lines = f.readlines()
    for ix,line in enumerate(lines):
        #comma = line.replace(" , ", ", ")
        print('comma', line.replace(" , ", ", "))
        #commaspace = ", ".join(t.replace(",", ", ") for t in line.split(", "))
        print('commaspace',", ".join(t.replace(",", ", ") for t in line.split(", ")))
        #colonspace = ": ".join(t.replace(":", ": ") for t in line.split(": "))
        print('colonspace',": ".join(t.replace(":", ": ") for t in line.split(": ")))
        #stripped = line.rstrip()
        print('stripped',line.rstrip())