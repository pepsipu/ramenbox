import json

op_list = open("./oplist").read().split("\n\n\n")
ops = []
for op_entry in op_list:
    op_modes = op_entry.split("--------------------------------------------")[1].split("\n\n")[0]
    for mode in op_modes.split("\n"):
        if len(mode) > 4:
            mode = mode.strip()
            new_op = {
                "name": op_entry[:3],
                "byte": int(mode[28:30], 16),
                "byte_length": int(mode[34:35])
            }
            addressing = mode[:14].strip()
            if addressing == "accumulator":
                new_op["addressing"] = "ac"
            elif addressing == "immidiate":
                new_op["addressing"] = "i"
            elif addressing == "implied":
                new_op["addressing"] = "ip"
            elif addressing == "relative":
                new_op["addressing"] = "r"
            elif addressing == "zeropage":
                new_op["addressing"] = "z"
            elif addressing == "zeropage,X":
                new_op["addressing"] = "zx"
            elif addressing == "zeropage,Y":
                new_op["addressing"] = "zy"
            elif addressing == "absolute":
                new_op["addressing"] = "a"
            elif addressing == "indirect":
                new_op["addressing"] = "in"
            elif addressing == "absolute,X":
                new_op["addressing"] = "ax"
            elif addressing == "absolute,Y":
                new_op["addressing"] = "ay"
            elif addressing == "(indirect,X)":
                new_op["addressing"] = "ix"
            elif addressing == "(indirect),Y":
                new_op["addressing"] = "iy"
            ops.append(new_op)

open("../src/ramencore/opcodes.json", "w").write(json.dumps(ops))