from dataclasses import dataclass


@dataclass(frozen=True)
class SelectorsNamespace:
    CHAMBER_PLENARY_EVENT = {
        "data": "td:nth-child(1)::text",
        "id_evento": "td:nth-child(2)::text",
        "categoria_evento": "td:nth-child(3)::text",
        "discursos": "td:nth-child(4) a::attr(href)",
    }
    CHAMBER_COMMITTEE_EVENT = {
        "data": "td:nth-child(1)::text",
        "id_evento": "td:nth-child(2)::text",
        "categoria_evento": "td:nth-child(3)::text",
        "ambiente_legislativo": "td:nth-child(5)::text",
        "discursos": "td:nth-child(4) a::attr(href)",
    }
    OTHERS = {
        "chamber_events": "table tbody tr",
        "content": "body",
    }

    def get(self, name, house=None, origin=None, type=None):
        if type == "event":
            if house == "chamber" and origin == "committee":
                return self.CHAMBER_COMMITTEE_EVENT.get(name, "")
            elif house == "chamber" and origin == "plenary":
                return self.CHAMBER_PLENARY_EVENT.get(name, "")

        return self.OTHERS.get(name, "")


SELECTORS = SelectorsNamespace()
