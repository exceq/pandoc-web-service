class GeneratePdfMessage:
    file_id: int
    markdown: str

    def __init__(self, file_id: int, markdown: str):
        self.file_id = file_id
        self.markdown = markdown
