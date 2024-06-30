import os

def combine_markdown_files(directory, output_file):
    with open(output_file, 'w') as outfile:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.md'):
                    with open(os.path.join(root, file), 'r') as infile:
                        outfile.write(infile.read())
                        outfile.write('\n\n') # add a couple of newlines between files

# call the function with directory and output file
combine_markdown_files('/path/to/directory', 'combined.md')
