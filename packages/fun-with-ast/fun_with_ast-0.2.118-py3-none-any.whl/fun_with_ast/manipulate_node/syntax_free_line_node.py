import _ast
import re


class SyntaxFreeLine(_ast.stmt):
    """Class defining a new node that has no syntax (only optional comments)."""
    COMMENT_LINE = 'comment_line'
    EMPTY_LINE = 'empty_line'
    EMPTY_LINE_NO_EOL = 'empty_line_no_eol'
    def __init__(self, comment=None, col_offset=0, comment_indent=1):
        super(SyntaxFreeLine, self).__init__()
        self.col_offset = col_offset
        self._fields = ['full_line']
        self.comment = comment
        self.comment_indent = comment_indent

    @property
    def full_line(self):
        if self.comment is not None:
            full_line = '{}#{}{}'.format(' ' * self.col_offset,
                                    ' ' * self.comment_indent,
                                    self.comment)
            return full_line
        return ''


    @classmethod
    def is_syntaxfree_line(cls, text):
        is_empty_line = re.match('([ \t]*)(\n)', text)
        if is_empty_line:
             return (is_empty_line, SyntaxFreeLine.EMPTY_LINE)

        is_empty_line = re.match('([ \t]+)$', text)
        if is_empty_line:
             return (is_empty_line, SyntaxFreeLine.EMPTY_LINE_NO_EOL)

        is_comment_line = re.match('([ \t]*)(#)([ \t]*)(.*)(\n)', text)
        if is_comment_line:
            return (is_comment_line, SyntaxFreeLine.COMMENT_LINE)
        return None

    def SetFromSrcLine(self, line):
        match_type = self.is_syntaxfree_line(line)
        if not match_type:
            raise ValueError('line {} is not a valid SyntaxFreeLine'.format(line))
        type = match_type[1]
        match = match_type[0]
        if type == SyntaxFreeLine.EMPTY_LINE or type == SyntaxFreeLine.EMPTY_LINE_NO_EOL:
            self.col_offset = len(match.group(1))
            self.comment_indent = 0
            self.comment = None
            return
        self.col_offset = len(match.group(1))
        self.comment = match.group(3) +  match.group(4)
        #self.comment_indent = len(match.group(3))
        self.comment_indent = 0 # alwas 0 for now
