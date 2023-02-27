from dataclasses import dataclass


@dataclass(frozen=True)
class PatternsNamespace:
    REGEX = {
        "chamber_speaker": (
            r"""((?:\(NÃO IDENTIFICADO\))|(?:\(Não identificado\))|(?:(?:[AO]\s(?:(?"""
            r""":SR\.?A?\.?\s)|(?:DR\.?A?\.?\s)|(?:SR\.?A?\.?\sDR\.?A?\.?\s)))(?:(?:"""
            r"""[A-ZA-Ú´'\-\s\|\\\)]+(?:J[rR]\.)?(?:\(\?\)[A-ZA-Ú´'\-\s\|\\]*(?:J[rR"""
            r"""]\.)?)?\s?(?:\-\s)?\([a-zà-úA-ZÀ-Ú´'\-\s\|\\\/\-\.\?]+(?:J[rR]\.)?(?"""
            r""":\(\?\)[a-zà-úA-ZÀ-Ú´'\-\s\|\\\/\-\.\?]*(?:J[rR]\.)?)?\))|(?:[A-ZÀ-Ú"""
            r"""´'\-\s\|\\\)]+(?:J[rR]\.)?(?:\(\?\)[A-ZÀ-Ú´'\-\s\|\\\)]*(?:J[rR]\.)?"""
            r""")?)|(?:[A-ZA-Ú´'\-\s\|\\\)]+(?:J[rR]\.)?(?:\(\?\)[A-ZA-Ú´'\-\s\|\\\)"""
            r"""]*(?:J[rR]\.)?)?\s\([a-zà-úA-ZÀ-Ú´'\-\s\|\\\/\-\.\?]+(?:J[rR]\.)?(?:"""
            r"""\(\?\)[a-zà-úA-ZÀ-Ú´'\-\s\|\\\/\-\.\?]*(?:J[rR]\.)?)?\))|(?:[a-zà-úA"""
            r"""-ZÀ-Ú´'\-\s\|\\\)]+(?:J[rR]\.)?(?:\(\?\)[a-zà-úA-ZÀ-Ú\-\s\|\\]*(?:J["""
            r"""rR]\.)?)?))|(?:[AO]\s(?:(?:SR\.?A?\.?)|(?:DR\.?A?\.?)|(?:SR\.?A?\.?"""
            r"""\sDR\.?A?\.?))(?:\s\(\?\))?)))(?:\(\?\))?(?:\?)?(?:\s?\-{1,2}\s)"""
        )
    }

    def get_regex(self, name):
        return self.REGEX.get(name, "")


PATTERNS = PatternsNamespace()
