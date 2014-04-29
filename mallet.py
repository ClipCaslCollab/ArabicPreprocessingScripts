import os
from subprocess import call, check_output


class Mallet:

    def __init__(self, binary):
        self._binary = binary

    def import_file(self, path, output, lang):
        if lang == "ar":
            os.system(self._binary + ' import-file --input ' + path + ' --keep-sequence --token-regex \'[\p{L}\p{P}]*\p{L}\' --output ' + output)
        elif lang == "en":
            os.system(self._binary + ' import-file --input ' + path + ' --keep-sequence --output ' + output)

    def import_dir(self, path, output):
        os.system(self._binary + ' import-dir --input ' + path + ' --keep-sequence --token-regex \'[\p{L}\p{P}]*\p{L}\' --output ' + output)

