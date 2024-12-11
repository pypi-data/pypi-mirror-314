import click
from generator import PhraseGenerator


@click.command()
@click.option('--words', default=4, type=int, help='Number of words for the returned passphrase.')
@click.option('--delimiter', default=" ", help='Separation character for the words.')
def cli(words, delimiter):
    """PhraseCraft is a secure passphrase generator CLI."""
    phrasecraft_object = PhraseGenerator()
    # Imports the word list "eef_wordlist.txt", asks for 5 random words
    wordlist = phrasecraft_object.import_wordlist()
    random_words = phrasecraft_object.select_random_words(wordlist, words)

    # Outputs the passphrase
    pass_phrase = phrasecraft_object.format_passphrase(random_words, delimiter)

    print(pass_phrase)

if __name__ == "__main__":
    cli()