from pathlib import Path
from random import choice
import re
from warnings import warn

class PhraseGenerator:

    def __init__(self):
        pass

    def import_wordlist(self):
        """Returns the eef_wordlist.txt from memory"""
        word_list_filename = "eef_wordlist.txt"
        absolute_path = Path(__file__).parent.joinpath(word_list_filename)
        if absolute_path.exists():
            try:
                return absolute_path.read_text()
            except Exception as e:
                print(e)
        else:
            raise Exception(f"Path not found: {absolute_path}")

    def select_random_words(self, wordlist: str, wordcount: int) -> list:
        """Randomizes words from eef_wordlist"""
        # Don't wanna allow a simple password
        if wordcount < 1:
            raise Exception("wordcount must be 1 or more.")

        # A passphrase is probably hard to remember after 10
        # even for people with good memory (heh)
        wordcount_limit = 10
        if wordcount > wordcount_limit:
            raise Exception(f"wordcount limit reached, received {wordcount}, limit is {wordcount_limit}.")

        if wordcount < 3:
            warn(
                "Warning: using two words or less is considered unsafe.",
                category=UserWarning,
                stacklevel=2
            )

        try:
            pattern = r"\d{5}\s+(\w+)"
            matches = re.findall(pattern, wordlist)

            if not matches:
                raise ValueError(f"No words matching the pattern: {pattern}")

            rand_wordlist = [choice(matches) for _ in range(wordcount)]
            return rand_wordlist

        except re.error as e:
            print(f"Regex error: {e}")
        except ValueError as e:
            print(f"ValueError: {e}")
        except Exception as e:
            print(f"An unexpected error: {e}")

    def format_passphrase(self, final_wordlist: list, delmimiter=" ") -> str:
        """Finialize the passphrase using the words randomized."""
        return f"{delmimiter}".join(final_wordlist)
