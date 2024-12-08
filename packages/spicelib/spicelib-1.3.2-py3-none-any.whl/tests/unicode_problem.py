from spicelib import AscEditor

asc = AscEditor("Bug_test_File.asc")
print(asc.get_components())
asc.add_instruction("; A comment will be added to the spice file.")
asc.save_netlist("Bug_test_File_updated.asc")