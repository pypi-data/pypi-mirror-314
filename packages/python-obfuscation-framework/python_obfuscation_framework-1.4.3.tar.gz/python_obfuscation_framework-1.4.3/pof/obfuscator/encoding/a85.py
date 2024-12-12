from tokenize import LPAR, NAME, NEWLINE, RPAR

from pof.utils.encoding import ASCII85Encoding
from pof.utils.tokens import untokenize


class ASCII85Obfuscator(ASCII85Encoding):
    """Obfuscate with encoding format ASCII85."""

    @classmethod
    def obfuscate_tokens(cls, tokens):
        code = untokenize(tokens)
        return [
            *cls.import_tokens(),
            (NEWLINE, "\n"),
            (NAME, "exec"),
            (LPAR, "("),
            *cls.decode_tokens(cls.encode_tokens(code.encode())),
            (RPAR, ")"),
            (NEWLINE, "\n"),
        ]
