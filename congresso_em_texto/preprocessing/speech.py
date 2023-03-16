from congresso_em_texto.preprocessing.text import TextPreprocessor


class SpeechPreprocessor(TextPreprocessor):
    def fix(self, speech):
        for key in speech.keys():
            speech[key] = self.remove_text_escape_chars(speech[key])
            speech[key] = self.remove_text_doubt_markers(speech[key])
            speech[key] = self.fix_text_whitespaces(speech[key])
            speech[key] = self.fix_text_brackets(speech[key])

        speech["orador"] = self.uppercase_text(speech["orador"])

        return speech

    def get_filename(self, event_id):
        return f"{event_id.replace('/', '-')}.csv"
