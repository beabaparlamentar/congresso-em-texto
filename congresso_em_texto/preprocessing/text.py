import re


class TextPreprocessor:
    """
    Classe para pré-processamento de texto.
    """

    def capitalize_text(self, text):
        """
        Torna a primeira letra de cada palavra do texto em maiusculo.

        Args:
            text (str): O texto a ser capitalizado.

        Returns:
            str: Texto com a primeira letra em maiúscula.
        """
        return text.capitalize()

    def fix_proper_noun(self, text):
        """
        Corrige o formato de nome próprio.

        Args:
            text (str): O nome próprio a ser corrigido.

        Returns:
            str: Nome próprio com a primeira letra de cada palavra em maiúscula.
        """
        lowercase = ["da", "de", "do", "das", "dos", "e"]
        text = [word.lower() for word in text.split()]
        text = [word if word in lowercase else word.capitalize() for word in text]

        return " ".join(text)

    def fix_text_brackets(self, text):
        """
        Remove espaços em excesso em torno de colchetes, parênteses e chaves.

        Args:
            text (str): O texto a ser corrigido.

        Returns:
            str: Texto após remoção de espaços em excesso em torno de colchetes, parênteses e chaves.
        """
        return re.sub(r"(\s+(?<=[\[{(])|\s+(?=[\]})]))", "", text)

    def fix_text_whitespaces(self, text):
        """
        Remove espaços em excesso no texto.

        Args:
            text (str): O texto a ser corrigido.

        Returns:
            str: Texto após remoção de espaços em excesso.
        """
        return " ".join(text.split())

    def fix_url_escape_chars(self, text):
        """
        Remove caracteres de escape de URL.

        Args:
            text (str): O texto a ser corrigido.

        Returns:
            str: Texto após remoção de caracteres de escape de URL.
        """
        return re.sub(r"([\n\r\t]+)", "", text)

    def remove_text_doubt_markers(self, text):
        """
        Remove marcadores de dúvida do texto.

        Args:
            text (str): O texto a ser corrigido.

        Returns:
            str: Texto após remoção de marcadores de dúvida.
        """
        return re.sub(r"(\(\?\))", " ", text)

    def remove_text_escape_chars(self, text):
        """
        Remove caracteres de escape do texto.

        Args:
            text (str): O texto a ser corrigido.

        Returns:
            str: Texto após remoção de caracteres de escape.
        """
        return re.sub(r"([\n\r\t]+)", " ", text)

    def uppercase_text(self, text):
        """
        Converte o texto para letras maiúsculas.

        Args:
            text (str): O texto a ser convertido.

        Returns:
            str: Texto em letras maiúsculas.
        """
        return text.upper()
