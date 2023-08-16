from congresso_em_texto.preprocessing.text import TextPreprocessor


class SpeechPreprocessor(TextPreprocessor):
    """
    Classe para pré-processamento de discursos.
    """

    def fix(self, speech):
        """
        Aplica correções e pré-processamento ao discurso.

        Args:
            speech (dict): Dados do discurso.

        Returns:
            dict: Dados do discurso após correções e pré-processamento.
        """
        for key in speech.keys():
            speech[key] = self.remove_text_escape_chars(speech[key])
            speech[key] = self.remove_text_doubt_markers(speech[key])
            speech[key] = self.fix_text_whitespaces(speech[key])
            speech[key] = self.fix_text_brackets(speech[key])

        speech["orador"] = self.uppercase_text(speech["orador"])

        return speech

    def get_filename(self, event_id):
        """
        Obtém o nome de arquivo para o discurso.

        Args:
            event_id (str): ID do evento.

        Returns:
            str: Nome do arquivo gerado para o discurso.
        """
        return f"{event_id.replace('/', '-')}.csv"
