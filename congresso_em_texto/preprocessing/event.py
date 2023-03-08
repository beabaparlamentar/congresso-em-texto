import difflib

from congresso_em_texto.preprocessing.date import DatePreprocessor
from congresso_em_texto.preprocessing.text import TextPreprocessor
from congresso_em_texto.utils.constants import COMMITTEES, URLS


class EventPreprocessor(DatePreprocessor, TextPreprocessor):
    def fix(self, event, house, origin):
        for key in event.keys():
            if key == "discursos":
                event[key] = self.fix_url_escape_chars(event[key])
            elif key == "data":
                event[key] = self.fix_text_whitespaces(event[key])
                event[key] = self.fix_date_pattern(event[key])
            else:
                if key == "categoria_evento":
                    event[key] = self.capitalize_text(event[key])

                event[key] = self.remove_text_escape_chars(event[key])
                event[key] = self.fix_text_whitespaces(event[key])
                event[key] = self.fix_text_brackets(event[key])

        if house == "chamber":
            event = self.fix_chamber_event(event, origin)

        return event

    def fix_chamber_event(self, event, origin):
        event["casa_legislativa"] = "Câmara dos Deputados"
        event["discursos"] = URLS.get_speech_url("chamber") + event["discursos"]

        if not event["categoria_evento"]:
            event["categoria_evento"] = "Outros"

        if origin == "plenary":
            event = self.fix_chamber_plenary_event(event)
        elif origin == "committee":
            event = self.fix_chamber_committee_event(event)

        return event

    def fix_chamber_plenary_event(self, event):
        event["ambiente_legislativo"] = "Plenário"
        event["categoria_ambiente"] = "Plenário"

        return event

    def fix_chamber_committee_event(self, event):
        event["categoria_ambiente"] = "Comissão"

        if "Ap c/" in event["categoria_evento"]:
            event["categoria_evento"] = "Audiência pública"

        standing_committees = COMMITTEES.to_list("chamber")
        committee = event["ambiente_legislativo"]

        match = difflib.get_close_matches(
            word=committee,
            possibilities=standing_committees,
        )

        if match:
            event["ambiente_legislativo"] = match[0]

        return event
