from textconverter import block_to_block_type, block_to_block_splitter

ordered = "1. First\n\n2. Second"

splited = block_to_block_splitter(ordered)
test = block_to_block_type(ordered)

print(splited)

print(test)

