
class CodeViewer(object):

    def __init__(self, filename, startline=1, endline=None):
        self.filename = filename
        self.startline = int(startline)
        self.endline = int(endline)

    def show(self):
        with open(self.filename, 'r') as f:
            lines = f.readlines()
            return lines[self.startline] if self.endline == None else lines[self.startline: self.endline+1]

    @staticmethod
    def load_for_web(request):
        filename = request.args.get("filename")
        startline = request.args.get("startline")
        endline = request.args.get("endline")
        print(filename, startline, endline)
        # import pdb; pdb.set_trace()
        return CodeViewer(filename, startline, endline).show(), startline, endline

if __name__ == "__main__":
    view = CodeViewer('sherlock/code_viewer.py', 9,13)
