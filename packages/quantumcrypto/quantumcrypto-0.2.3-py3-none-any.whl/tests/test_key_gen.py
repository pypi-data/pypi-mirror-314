"""
Keygen test cases.
"""

import unittest
from unittest.mock import patch
from quantumcrypto.utils.functions import (
    _k_pke_key_gen,
    _ml_kem_gey_gen_internal,
    ml_kem_gey_gen,
    ml_kem_encaps
)
from quantumcrypto.utils.parameters import P512


class TestKeyGen(unittest.TestCase):
    """
    Keygen tests.
    """

    def test_tpke_key_gen_creates_right_length_keys(self):
        """
        T_pke_keygen creates appropriate length and type of keys.
        """
        k = 2
        n1 = 3
        encryption_key, decryption_key = _k_pke_key_gen(
            "randbyts".encode()*4, k, n1)

        # length = 384*k + 32
        self.assertEqual(800, len(encryption_key))
        self.assertEqual(True, isinstance(encryption_key, bytes))

        # length = 384*k
        self.assertEqual(768, len(decryption_key))
        self.assertEqual(True, isinstance(decryption_key, bytes))

    def test_tpke_key_gen_improper_random_bytes(self):
        """
        Test improper random bytes raises error.
        """
        k = 2
        n1 = 3
        with self.assertRaises(ValueError) as error:
            _k_pke_key_gen(
                "randbyts".encode()*3, k, n1)

        self.assertEqual(
            "KeyGen requires 32 random bytes",
            str(error.exception))

    def test_ml_kem_key_gen_internal_creates_right_length_keys(self):
        """
        Ml kem keygen internal creates appropriate length and type of keys.
        """
        k = 2
        n1 = 3
        ek, dk = _ml_kem_gey_gen_internal(
            "randbyt1".encode()*4, "randbyt2".encode()*4, k, n1)

        # length = 384*k + 32
        self.assertEqual(800, len(ek))
        self.assertEqual(True, isinstance(ek, bytes))

        # length = 768*k+96
        self.assertEqual(768*2+96, len(dk))
        self.assertEqual(True, isinstance(dk, bytes))

    def test_ml_kem_key_gen_creates_right_length_keys(self):
        """
        Ml kem keygen creates appropriate length and type of keys.
        """
        k = 2
        n1 = 3
        ek, dk = ml_kem_gey_gen(k, n1)

        # length = 384*k + 32
        self.assertEqual(800, len(ek))
        self.assertEqual(True, isinstance(ek, bytes))

        # length = 768*k+96
        self.assertEqual(768*2+96, len(dk))
        self.assertEqual(True, isinstance(dk, bytes))

    def test_ml_kem_key_gen_improper_random_bytes(self):
        """
        Ml kem keygen raises error if received improper amount of random bytes.
        """
        k = 2
        n1 = 3
        mock_output = "randbyt1".encode()*3
        with patch('quantumcrypto.utils.functions.token_bytes', return_value=mock_output):
            with self.assertRaises(ValueError) as error:
                ml_kem_gey_gen(k, n1)

        self.assertEqual(
            "Random byte generation failed",
            str(error.exception))

    def test_ml_kem_encaps_raises_error(self):
        """
        Ml kem encaps raises error if received improper amount of random bytes.
        """
        mock_output = "randbyt1".encode()*3
        mock_enc_key = "mock".encode()*100
        with patch('quantumcrypto.utils.functions.token_bytes', return_value=mock_output):
            with self.assertRaises(ValueError) as error:
                ml_kem_encaps(mock_enc_key, P512)

        self.assertEqual(
            "Random byte generation failed",
            str(error.exception))
