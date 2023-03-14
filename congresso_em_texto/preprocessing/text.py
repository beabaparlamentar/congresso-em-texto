import re


class TextPreprocessor:
    def capitalize_text(self, text):
        return text.capitalize()

    def fix_proper_noun(self, text):
        lowercase = ["da", "de", "do", "das", "dos"]
        text = [word.lower() for word in text.split()]
        text = [word if word in lowercase else word.capitalize() for word in text]

        return " ".join(text)

    def fix_text_brackets(self, text):
        return re.sub(r"(\s+(?<=[\[{(])|\s+(?=[\]})]))", "", text)

    def fix_text_whitespaces(self, text):
        return " ".join(text.split())

    def fix_url_escape_chars(self, text):
        return re.sub(r"([\n\r\t]+)", "", text)

    def remove_text_doubt_markers(self, text):
        return re.sub(r"(\(\?\))", " ", text)

    def remove_text_escape_chars(self, text):
        return re.sub(r"([\n\r\t]+)", " ", text)

    def uppercase_text(self, text):
        return text.upper()
