import unittest
from unittest.mock import patch
from IndovinaLaParola.IndovinaLaParola import IndovinaLaParola


class TestIndovinaLaParolaIntegration(unittest.TestCase):
    @patch('builtins.input', side_effect=['p', 'y', 't', 'h', 'o', 'n'])
    @patch('builtins.print')  # Mocka la print per verificare il flusso
    def test_gioco_vittoria(self, mock_print, mock_input):
        # Simula una partita vincente
        with patch('secrets.choice', return_value="python"):
            IndovinaLaParola()

        # Verifica che il messaggio di vittoria sia stampato
        mock_print.assert_any_call("Complimenti! Hai indovinato la parola: python")

    @patch('builtins.input', side_effect=['a', 'b', 'c', 'd', 'e', 'f'])
    @patch('builtins.print')
    def test_gioco_sconfitta(self, mock_print, mock_input):
        # Simula una partita perdente
        with patch('secrets.choice', return_value="python"):
            IndovinaLaParola()

        # Verifica che il messaggio di sconfitta sia stampato
        mock_print.assert_any_call("Peccato! Hai finito i tentativi. La parola era: python")

