import re
from typing import List


def split_text_with_regex(text: str, separator: str = "\n\n", keep_separator: bool = True) -> list[str]:
    # Now that we have the separator, split the text
    if separator:
        if keep_separator:
            # The parentheses in the pattern keep the delimiters in the result.
            _splits = re.split(f"({re.escape(separator)})", text)
            splits = [_splits[i - 1] + _splits[i] for i in range(1, len(_splits), 2)]
            if len(_splits) % 2 != 0:
                splits += _splits[-1:]
        else:
            splits = re.split(separator, text)
    else:
        splits = list(text)
    return [s for s in splits if (s not in {"", "\n"})]

def split_sentences( text: str) -> List[str]:
    """Split text into sentences using enhanced regex patterns.

    Handles various cases including:
    - Standard sentence endings across multiple writing systems
    - Quotations and parentheses
    - Common abbreviations
    - Decimal numbers
    - Ellipsis
    - Lists and enumerations
    - Special punctuation
    - Common honorifics and titles

    Args:
        text: Input text to be split into sentences

    Returns:
        List of sentences
    """
    # Define sentence ending punctuation marks from various writing systems
    sent_endings = (
        r'[!.?։؟۔܀܁܂߹।॥၊။።፧፨᙮᜵᜶᠃᠉᥄᥅᪨᪩᪪᪫᭚᭛᭞᭟᰻᰼᱾᱿'
        r'‼‽⁇⁈⁉⸮⸼꓿꘎꘏꛳꛷꡶꡷꣎꣏꤯꧈꧉꩝꩞꩟꫰꫱꯫﹒﹖﹗！．？𐩖𐩗'
        r'𑁇𑁈𑂾𑂿𑃀𑃁𑅁𑅂𑅃𑇅𑇆𑇍𑇞𑇟𑈸𑈹𑈻𑈼𑊩𑑋𑑌𑗂𑗃𑗉𑗊𑗋𑗌𑗍𑗎𑗏𑗐𑗑𑗒'
        r'𑗓𑗔𑗕𑗖𑗗𑙁𑙂𑜼𑜽𑜾𑩂𑩃𑪛𑪜𑱁𑱂𖩮𖩯𖫵𖬷𖬸𖭄𛲟𝪈｡。]'
    )

    # Common abbreviations and titles that don't end sentences
    abbrevs = (
        r"(?:Mr|Mrs|Ms|Dr|Prof|Sr|Jr|vs|etc|viz|al|Gen|Col|Fig|Lt|Mt|St"
        r"|etc|approx|appt|apt|dept|est|min|max|misc|no|ps|seq|temp|etal"
        r"|e\.g|i\.e|vol|vs|cm|mm|km|kg|lb|ft|pd|hr|sec|min|sq|fx|Feb|Mar"
        r"|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)"
    )

    # First, protect periods in known abbreviations
    text = re.sub(rf"({abbrevs})\.", r"\1@POINT@", text, flags=re.IGNORECASE)

    # Protect decimal numbers
    text = re.sub(r"(\d+)\.(\d+)", r"\1@POINT@\2", text)

    # Protect ellipsis
    text = re.sub(r"\.\.\.", "@ELLIPSIS@", text)

    # Protect email addresses and websites
    text = re.sub(r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", r"@EMAIL@\1@EMAIL@", text)
    text = re.sub(r"(https?://[^\s]+)", r"@URL@\1@URL@", text)

    # Handle parentheses and brackets
    text = re.sub(r'\([^)]*\.[^)]*\)', lambda m: m.group().replace('.', '@POINT@'), text)
    text = re.sub(r'\[[^\]]*\.[^\]]*\]', lambda m: m.group().replace('.', '@POINT@'), text)

    # Handle quotations with sentence endings
    text = re.sub(rf'({sent_endings})"(\s+[A-Z])', r'\1"\n\2', text)

    # Handle standard sentence endings
    text = re.sub(rf'({sent_endings})(\s+[A-Z"]|\s*$)', r'\1\n\2', text)

    # Handle lists and enumerations
    text = re.sub(r'(\d+\.)(\s+[A-Z])', r'\1\n\2', text)
    text = re.sub(r'([a-zA-Z]\.)(\s+[A-Z])', r'\1\n\2', text)

    # Restore protected periods and symbols
    text = text.replace("@POINT@", ".")
    text = text.replace("@ELLIPSIS@", "...")
    text = re.sub(r'@EMAIL@([^@]+)@EMAIL@', r'\1', text)
    text = re.sub(r'@URL@([^@]+)@URL@', r'\1', text)

    # Split into sentences
    sentences = [s.strip() for s in text.split('\n') if s.strip()]

    return sentences
