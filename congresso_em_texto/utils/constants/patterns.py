from dataclasses import dataclass


@dataclass(frozen=True)
class PatternsNamespace:
    REGEX = {
        "chamber_speaker": (
            r"""((?:(?:\(NÃO IDENTIFICADO\))|(?:\(Não identificado\)))|(?:[AO]\s(?:S"""
            r"""R\.?A?\.?\s)|(?:DR\.?A?\.?\s))(?:(?:(?:[a-zà-úA-ZÀ-Ú´'\s\|\\]+(?:J[r"""
            r"""R]\.)?(?:\(\?\)[a-zà-úA-ZÀ-Ú´'\s\|\\]*(?:J[rR]\.)?)?))|(?:[a-zà-úA-Z"""
            r"""À-Ú´'\s\|\\]+(?:J[rR]\.)?(?:\(\?\)[a-zà-úA-ZÀ-Ú´'\s\|\\]*(?:J[rR]\.)"""
            r"""?)?\s?(?:[\-\–]\s)?\([a-zà-úA-ZÀ-Ú´'\-\–\s\|\\\/\.\?]+(?:J[rR]\.)?(?"""
            r""":\(\?\)[a-zà-úA-ZÀ-Ú´'\-\–\s\|\\\/\-\–\.\?]*(?:J[rR]\.)?)?\))))(?:\("""
            r"""\?\))?(?:\?)?(?:\s?[\–\-]{1,2}\s)"""
        )
    }

    def get_regex(self, name):
        return self.REGEX.get(name, "")


PATTERNS = PatternsNamespace()
