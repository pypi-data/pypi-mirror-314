from licitpy.parsers.tender import TenderParser

parsers = TenderParser()


def _extract_view_state(html: str) -> str:
    return parsers.get_view_state(html)


__all__ = ["_extract_view_state"]
