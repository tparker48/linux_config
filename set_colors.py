import argparse
import os
import json

home = os.path.expanduser('~')
templates = './config_files/'

parser = argparse.ArgumentParser()
parser.add_argument('-c','--config', type=str, action='store', required=True)
args = parser.parse_args()
config_file = args.config

try:
    with open(config_file, 'rb') as master_config_json:
        master_config = json.load(master_config_json)
except:
    print(f"ERROR: config file '{config_file}' not found!")
    exit(1)

print(master_config)

# Scan ../config_files/dyanmic/ for all template config files
config_paths = []
for root, dirs, files in os.walk(templates):
    for file in files:
        template_path = os.path.join(root,file)
        rel_path = root.split(os.sep)[2:]
        output_path = os.path.join(home, '.config', *rel_path, file)
        config_paths.append([template_path, output_path])

print(config_paths)

# Fill in templates with master config vals, write out
for template_path, output_path in config_paths:
    with open(template_path, 'r') as template:
        lines = template.readlines()

    for i,line in enumerate(lines):
        for name, val in master_config['color_assignments'].items():
            lines[i] = lines[i].replace(f'[{name}]', f'[{val}]')
        for name, val in master_config['colors'].items():
            lines[i] = lines[i].replace(f'[{name}]', val)
        for name, val in master_config['misc'].items():
            lines[i] = lines[i].replace(f'[{name}]', str(val))

    with open(output_path, 'w') as outfile:
        outfile.writelines(lines)
        print(f'{output_path} overwritten!')


