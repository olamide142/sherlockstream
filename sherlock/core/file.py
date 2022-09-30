code_string = """
def function_decorator(source_file):
    decorated = 0 #number of decorated functions in a file
    code_string = ""

    with open(source_file, 'r') as f:
        code_string = f.read()

    marker_import = 'from sherlock.transformer import sherlock_yellow'
    functions = function_finder(code_string)
    has_future = module_has_future(code_string)
    marker_imported = False
    first_import_line = 0
    if len(functions):
            
        with open(source_file, 'w') as f:

            for index, line in enumerate(code_string.split(''), start=1):
                # if file uses the __future__ module, 
                # import yellow_marker on the next line
                    
                if all([
                        len(functions), 
                        (not has_future), 
                        (not marker_imported)
                    ]):
                    f.write(marker_import)
                    marker_imported = True
                elif has_future and index > first_import_line:
                    f.write(marker_import)
                    marker_imported = True

                function = functions[0] if len(functions) else 0

                if function and (index == function.get('line_number')):
                    column_offset = function.get('column_offset')
                    f.write(indent_and_add(column_offset))
                    functions.pop(0)
                    decorated += 1
                    
                f.write(f'{line}')    
                
    return decorated
"""

code_object = compile(code_string, __file__, 'exec')
import dis
print(dis.dis(code_string))
