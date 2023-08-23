import difflib

from congresso_em_texto.preprocessing.date import DatePreprocessor
from congresso_em_texto.preprocessing.text import TextPreprocessor
from congresso_em_texto.utils.constants import COMMITTEES, URLS


class EventPreprocessor(DatePreprocessor, TextPreprocessor):
    """
    Classe para pré-processamento de informações de eventos.
    """
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
        """
        Aplica correções e pré-processamento aos dados do evento.

        Args:
            event (dict): Dados do evento.
            house (str): A casa legislativa ("senate" ou "chamber").
            origin (str): A origem dos dados ("plenary" ou "committee").

        Returns:
            dict: Dados do evento após correções e pré-processamento.
        """
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
        """  
        Aplica correções e pré-processamento específicos para eventos do plenário.

        Args:
            event (dict): Dados do evento.
      
        Returns:
            dict: Dados do evento após correções e pré-processamento específicos da câmara.
        """
        event["ambiente_legislativo"] = "Plenário"
        event["categoria_ambiente"] = "Plenário"

        return event

    def fix_chamber_committee_event(self, event):
        """
        Aplica correções e pré-processamento específicos para eventos das comissões.

        Args:
            evento (dict): Dados do evento.

        Returns:
            dict: Dados do evento após correções e pré-processamento específicos para plenários da câmara.
        """
        event["categoria_ambiente"] = "Comissão"

        if "congresso nacional" in event["categoria_evento"]:
            event["categoria_evento"] = "Sessão do Congresso Nacional"

        if "Fórum" in event["categoria_evento"]:
            event["categoria_evento"] = "Fórum"

        for substring in ["Ap c/", "ap /", "Audiência pública"]:
            if substring in event["categoria_evento"]:
                event["categoria_evento"] = "Audiência pública"

        if "Outro " in event["categoria_evento"]:
            event["categoria_evento"] = "Outros"

        standing_committees = COMMITTEES.to_list("chamber")
        committee = event["ambiente_legislativo"]

        match = difflib.get_close_matches(
            word=committee,
            possibilities=standing_committees,
        )

        if match:
            event["ambiente_legislativo"] = match[0]

        return event
