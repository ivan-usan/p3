import re
import os

def compile(file_name):
    with open(file_name, 'r') as f:
        data = f.read()

    for common_file_name in os.listdir('common'):
        if common_file_name.endswith('.py'):
            with open('common/'+common_file_name) as f:
                data = f.read() + '\n' + data

    # print('data', data)
    data = re.sub('from common.+', '',data)

    with open('compiled_'+file_name, 'w') as f:
        f.write(data)


for file_name in ['child', 'parent']:
    compile(file_name+'.py')
