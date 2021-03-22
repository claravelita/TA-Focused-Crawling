string_with_nonASCII = "àa string withé fuünny charactersß."


encoded_string = string_with_nonASCII.encode("ascii", "replace")

decode_string = encoded_string.decode()


print(decode_string)