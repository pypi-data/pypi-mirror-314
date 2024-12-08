import PyPDF2


def pdf2chunks(filename: str, split_by="paragraphs"):
    """Breaks down a local pdf file into smaller chunks"""
    reader = PyPDF2.PdfReader(filename)
    chunks = []
    for page_number in range(len(reader.pages)):
        page_text = reader.pages[page_number].extract_text().replace("\n", " ")

        if split_by == "pages":
            chunks.append(
                {"document": page_text, "location": page_number, "source": filename}
            )
        elif split_by == "paragraphs":
            # Then split it by new lines and further break down if it's larger than the size requirements
            docs_long = page_text.split("\n")
            docs = []

            substring_length = 1000

            for doc in docs_long:
                if len(doc) <= substring_length:
                    docs += [doc]
                else:
                    docs += [
                        doc[i : i + substring_length]
                        for i in range(0, len(doc), substring_length)
                    ]

            for doc in docs:
                if len(doc) > 64:
                    chunks.append(
                        {"document": doc, "location": page_number, "source": filename}
                    )
    return chunks
