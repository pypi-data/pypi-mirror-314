from compress_json import compress, decompress
import json
import sys

def minify(folder, file_name):
    "Minify JSON"
    file_data = open(folder+'/'+file_name, "r", 1).read() # store file info in variable
    json_data = json.loads(file_data) # store in json structure
    json_string = json.dumps(json_data, separators=(',', ":")) # Compact JSON structure
    file_name = str(file_name).replace(".json", "") # remove .json from end of file_name string
    new_file_name = folder+"/{0}_minify.json".format(file_name)
    open(new_file_name, "w+", 1).write(json_string) # open and write json_string to file

json_file = f'C:\\Users\\kivanc\\Downloads\\metrics.json'
data_file = f'C:\\Users\\kivanc\\Downloads\\data.json'

minify('C:\\Users\\kivanc\\Downloads','metrics.json')

# with open(json_file, 'r', encoding="utf8") as f:
#     data = json.load(f)

# compressed = compress(data) # the result is a list (array)

# with open(data_file, "w") as fd:
# 	fd.write(json.dumps(compressed)) # convert into string if needed