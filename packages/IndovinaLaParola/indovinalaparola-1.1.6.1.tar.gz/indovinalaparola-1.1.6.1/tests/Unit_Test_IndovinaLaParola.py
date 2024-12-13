import secrets
import unittest
from unittest.mock import patch

class TestIndovinaLaParolaUnit(unittest.TestCase):
    def test_selezione_parola(self):
        # Test che la parola segreta sia selezionata dalla lista
        parole = ["python", "computer", "gioco", "programmazione", "matematica"]
        with patch('secrets.choice', return_value="python"):
            parola_segreta = secrets.choice(parole)
            self.assertIn(parola_segreta, parole)
            self.assertEqual(parola_segreta, "python")

    def test_lettere_indovinate(self):
        # Test della logica per aggiornare le lettere indovinate
        parola_segreta = "python"
        lettere_indovinate = [""] * len(parola_segreta)
        lettera = "p"

        for i, carattere in enumerate(parola_segreta):
            if carattere == lettera:
                lettere_indovinate[i] = lettera

        self.assertEqual(lettere_indovinate, ["p", "", "", "", "", ""])