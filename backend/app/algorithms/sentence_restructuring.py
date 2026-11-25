import random
import re
from typing import List
from backend.app.algorithms.base import BaseAugmenter

class SentenceRestructuringAugmenter(BaseAugmenter):
    def __init__(self):
        super().__init__("sentence_restructuring")

    def _transform_introductory_clause(self, text: str) -> str:
        # Match "In the event that X, Y." <-> "If X, Y."
        if text.startswith("In the event that "):
            return "If " + text[len("In the event that "):]
        elif text.startswith("If "):
            return "In the event that " + text[len("If "):]
        
        # Match "In no event shall X be liable for Y." -> "Neither party shall under any circumstances be liable for Y."
        if text.startswith("In no event shall "):
            rest = text[len("In no event shall "):]
            return "Under no circumstances shall " + rest
        elif text.startswith("Under no circumstances shall "):
            return "In no event shall " + text[len("Under no circumstances shall "):]

        # Match "To the maximum extent permitted by applicable law, X"
        prefix = "To the maximum extent permitted by applicable law,"
        if text.startswith(prefix):
            remainder = text[len(prefix):].strip()
            if remainder:
                # Transpose prefix to end
                remainder = remainder[0].upper() + remainder[1:].rstrip(".")
                return f"{remainder}, to the maximum extent permitted by applicable law."
        
        # Match "Upon written notice, either party may terminate..."
        m_upon = re.match(r"^(Upon [^,]+),\s*(.+)$", text)
        if m_upon:
            intro = m_upon.group(1).lower()
            main_clause = m_upon.group(2).rstrip(".")
            main_capitalized = main_clause[0].upper() + main_clause[1:]
            return f"{main_capitalized}, {intro}."

        # Match "Subject to [^,]+,\s*(.+)"
        m_subj = re.match(r"^(Subject to [^,]+),\s*(.+)$", text)
        if m_subj:
            intro = m_subj.group(1).lower()
            main_clause = m_subj.group(2).rstrip(".")
            main_capitalized = main_clause[0].upper() + main_clause[1:]
            return f"{main_capitalized}, {intro}."

        # Match "Except as [^,]+,\s*(.+)"
        m_except = re.match(r"^(Except as [^,]+),\s*(.+)$", text)
        if m_except:
            intro = m_except.group(1).lower()
            main_clause = m_except.group(2).rstrip(".")
            main_capitalized = main_clause[0].upper() + main_clause[1:]
            return f"{main_capitalized}, {intro}."

        # Transposition of concluding adverbial phrase to front if ends with ", without prior written consent." etc.
        m_tail = re.search(r"^(.*),\s*(without [^.]+)\.$", text)
        if m_tail:
            body = m_tail.group(1)
            tail = m_tail.group(2)
            tail_cap = tail[0].upper() + tail[1:]
            body_low = body[0].lower() + body[1:]
            return f"{tail_cap}, {body_low}."

        return text

    def generate(self, text: str, n: int = 1, seed: int = 42) -> List[str]:
        rng = random.Random(seed)
        transformed = self._transform_introductory_clause(text)
        
        # If no regex matched, generate minor grammatical syntactic variations
        results = []
        for i in range(n):
            if transformed != text:
                results.append(transformed)
            else:
                # Alternative restructuring: active / agreement clause
                alt = text
                if " agrees to " in text:
                    alt = text.replace(" agrees to ", " shall ")
                elif " shall maintain " in text:
                    alt = text.replace(" shall maintain ", " agrees to maintain ")
                elif " shall defend and indemnify " in text:
                    alt = text.replace(" shall defend and indemnify ", " shall indemnify and defend ")
                elif " shall be governed by, and construed in accordance with, " in text:
                    alt = text.replace(
                        " shall be governed by, and construed in accordance with, ",
                        " shall be construed and governed in accordance with "
                    )
                elif " exclusive jurisdiction and venue " in text:
                    alt = text.replace(" exclusive jurisdiction and venue ", " venue and exclusive jurisdiction ")
                elif " without giving effect to " in text:
                    alt = text.replace(" without giving effect to ", " without regard to ")
                elif " without regard to " in text:
                    alt = text.replace(" without regard to ", " without giving effect to ")
                elif " will " in text and " will not " not in text:
                    alt = text.replace(" will ", " shall ")
                elif " shall " in text and " shall not " not in text:
                    alt = text.replace(" shall ", " will ")
                
                results.append(alt)

        return results
