era5file = open('./strings/other.txt')
string = era5file.read()

string = string.replace("'", '"')

text_file = open("./strings/other.json", "w")
text_file.write(string)