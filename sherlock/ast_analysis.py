import ast
import itertools

class AstAnalysis(object):

    def __init__(self, source=None, filename=None, line_number=None):
        self.filename = filename
        self.line_number = line_number
        self._ast = None
        self.source = source or self.get_source_by_line_number(line_number, filename)


    def _check_source(self, source):
        if source is None:
            source = self.source
        if self._ast is None:
            try:
                self._ast = ast.dump(ast.parse(source, self.filename))
                return 1
            except BaseException as ex:
                return ex

    def get_source_nextline(self, line_number=None, source=None, **kw):
        line_of_interest = line_number or self.line_number
        source_of_interest = source or self.source
        # import pdb;
        # pdb.set_trace()
        with open(self.filename, 'r') as file:
            while 1 and (len(file.readlines()) <= line_of_interest):
                line = next(itertools.islice(file, line_of_interest, line_of_interest+1), "")
                if len(line) == 0 or self._check_source(source_of_interest) == (True,None):
                    #Since the line is empty or the line syntax is correct then move to the nexline
                    line_of_interest += 1
                    self.get_source_nextline(line_number = line_of_interest + 1,
                                             source=u"""\r\n""")
                if self._check_source(source_of_interest+line) == 1:
                    source_of_interest = source_of_interest+line
                    return line_of_interest, source_of_interest

                if isinstance(val:= self._check_source(source_of_interest+line) , BaseException):
                    if val.__class__.__name__ == "SyntaxError":
                        if val.msg == "unexpected EOF while parsing":
                            line_of_interest += 1
                            return self.get_source_nextline(line_number = line_of_interest,
                                             source=source_of_interest + line, before=source_of_interest, after=line)
                        if val.msg == "unexpected character after line continuation character":
                            return self.get_source_nextline(line_number = line_of_interest,
                                             source=kw.get("before")+kw.get("after"))
        return source_of_interest, line_of_interest

    def get_source_by_line_number(self, line_number, filename):
        with open(filename, 'r') as file:
            line = next(itertools.islice(file, line_number, line_number + 1), None)
            if len(line.strip()) > 0:
                self.get_source_nextline(line_number+1, filename)
            else:
                return line


if __name__ == "__main__":
    aa = AstAnalysis(filename="/home/victor/workspace/sherlockstream/sherlock/sample.py", line_number=46)
    print(aa.get_source_nextline())
    # import dis
    # print(dis.dis(AstAnalysis))
    # import pdb; pdb.set_trace()