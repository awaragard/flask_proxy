from os.path import dirname, realpath, join

test_case_dir = dirname(realpath(__file__))

def get_test_def(name):
    return join(test_case_dir, name, 'test.yml')
