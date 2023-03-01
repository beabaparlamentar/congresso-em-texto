import re


class TextPreprocessor:
    def capitalize_text(self, text):
        return text.capitalize()

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
