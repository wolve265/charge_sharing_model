# script outputs Unicode for each greek letter, capital and small
# these codes can be used to display greek letters in f-strings in the following way
# print(f"char(916) = b^2 - 4ac")
#
# works for matplotlib axes and figure titles

# alternatively, you can just copy the output of this and use it as follows :)
# print(f"Δ = b^2 - 4ac")

# codes for all capital greek letters
for i in range(913, 938):
    print(f"{i} : {chr(i)}")
print()

# codes for all small greek letters
for i in range(945, 970):
    print(f"{i} : {chr(i)}")
print()

# greek alphabet
str = ""
for i in range(913, 938):
    str += chr(i)
str += "\t"
for i in range(945, 970):
    str += chr(i)
print(str)