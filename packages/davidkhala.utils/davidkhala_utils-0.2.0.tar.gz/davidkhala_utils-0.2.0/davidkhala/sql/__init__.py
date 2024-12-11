from sqlparse import split, format


class SQL:
    def __init__(self, sql: str):
        self.sql = sql

    def split(self) -> list[str]:
        return split(format(self.sql, strip_comments=True))