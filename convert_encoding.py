import codecs

# Define the current encoding of the Procfile
current_encoding = 'ISO-8859-1'

# Define the filename of the Procfile
procfile_filename = 'Procfile'

# Define the filename for the UTF-8 encoded Procfile
procfile_utf8_filename = 'Procfile_utf8'

# Open the Procfile with the current encoding and read its content
with codecs.open(procfile_filename, 'r', encoding=current_encoding) as file:
    content = file.read()

# Open a new file with UTF-8 encoding and write the content to it
with codecs.open(procfile_utf8_filename, 'w', encoding='utf-8') as file:
    file.write(content)
