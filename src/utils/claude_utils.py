def extract_text(blocks):
    return "\n".join(
        block.text for block in blocks if block.type == "text"
    )