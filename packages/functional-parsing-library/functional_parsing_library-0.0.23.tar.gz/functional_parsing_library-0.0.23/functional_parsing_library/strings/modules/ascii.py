from string import ascii_lowercase as ascii_lowercase_letters, ascii_uppercase as ascii_uppercase_letters
from functional_parsing_library.strings.modules.char_in import char_in

ascii_lowercase = char_in(ascii_lowercase_letters)

ascii_uppercase = char_in(ascii_uppercase_letters)

ascii_letter = ascii_lowercase | ascii_uppercase
