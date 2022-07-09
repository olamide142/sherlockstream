def mydecorator(func):

    def inner(*args, **kwargs):
        # TODO:Get all the info needed and pass 
        # info to sherlock server here
        
        func(*args, **kwargs)

    return inner

@mydecorator
def function_decorator(source_file):
    
    fake_code = None

    with open(source_file, 'r') as f:
        fake_code = f.readlines()

    def get_indent_length(line):
        indent_size = 0
        for character in line:
            if character == ' ':
                indent_size += 1
            else: break
        return indent_size

    with open(source_file, 'w') as f:
        for line in fake_code:
            if line.strip().startswith(('def ', 'async def ')):
                f.write(f"{' '*get_indent_length(line)}@mydecorator\n")
            f.write(line)

function_decorator(source_file='sherlock/fakecode')