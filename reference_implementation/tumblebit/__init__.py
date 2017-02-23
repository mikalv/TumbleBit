# -*- coding: utf-8 -*-

"""
Tumblebit
~~~~~~~~~

This module has:
    - the ctype declarations for interfacing
      with Libressl.
    - Helper methods to convert back from structures
"""


import os
import sys
import logging
import ctypes
import ctypes.util
import platform


###########################################################################
## CTypes -- Function Definitions
###########################################################################

########################################################
## Standard C Library
########################################################

_libc = ctypes.cdll.LoadLibrary(ctypes.util.find_library('libc'))

_libc.fopen.restype = ctypes.c_void_p
_libc.fopen.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

_libc.fclose.restype = ctypes.c_int
_libc.fclose.argtypes = [ctypes.c_void_p]

########################################################
## LibreSSL
########################################################

# Change path to where libressl library is
if platform.system() == "Darwin":

    # Was libressl installed using homebrew?
    path = "/usr/local/opt/libressl/lib/libssl.dylib"
    if not os.path.isfile(path):
        # Maybe built from source
        path = "/usr/local/lib/libssl.dylib"

else:
    path = "/usr/local/lib/libssl.so"

if not os.path.isfile(path):
    sys.exit("Error: didn't find libressl in your system.")

_ssl = ctypes.cdll.LoadLibrary(path)
_ssl.SSL_load_error_strings()


class LibreSSLException(OSError):
    """
    Represents an error that originated from LibreSSL
    """
    pass


# Taken from python-bitcoinlib key.py
# Thx to Sam Devlin for the ctypes magic 64-bit fix
def _check_res_void_p(val, func, args):
    """Checks if the returned pointer is void"""
    if val == 0:
        errno = _ssl.ERR_get_error()
        errmsg = ctypes.create_string_buffer(120)
        _ssl.ERR_error_string_n(errno, errmsg, 120)
        msg = str(func.__name__) + '(' + ','.join(args) + '): '
        raise LibreSSLException(errno, msg + str(errmsg.value))

    return ctypes.c_void_p(val)


def _print_ssl_error():
    """Prints out the ssl error"""
    errno = _ssl.ERR_get_error()
    errmsg = ctypes.create_string_buffer(120)
    _ssl.ERR_error_string_n(errno, errmsg, 120)
    raise LibreSSLException(errno, str(errmsg.value))


#####################################
## Constants
#####################################

RSA_F4 = 65537
RSA_NO_PADDING = 3

#####################################
## BN
#####################################

##################
## BN
##################

_ssl.BN_new.errcheck = _check_res_void_p
_ssl.BN_new.restype = ctypes.c_void_p
_ssl.BN_new.argtypes = None

_ssl.BN_free.restype = None
_ssl.BN_free.argtypes = [ctypes.c_void_p]

_ssl.BN_num_bits.restype = ctypes.c_int
_ssl.BN_num_bits.argtypes = [ctypes.c_void_p]

_ssl.BN_set_word.restype = ctypes.c_int
_ssl.BN_set_word.argtypes = [ctypes.c_void_p, ctypes.c_ulong]

_ssl.BN_gcd.restype = ctypes.c_int
_ssl.BN_gcd.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                        ctypes.c_void_p, ctypes.c_void_p]

_ssl.BN_ucmp.restype = ctypes.c_int
_ssl.BN_ucmp.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

##################
## Conversions
##################

_ssl.BN_bn2bin.restype = ctypes.c_int
_ssl.BN_bn2bin.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

_ssl.BN_bin2bn.errcheck = _check_res_void_p
_ssl.BN_bin2bn.restype = ctypes.c_void_p
_ssl.BN_bin2bn.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p]

##################
## BN_CTX
##################

_ssl.BN_new.errcheck = _check_res_void_p
_ssl.BN_new.restype = ctypes.c_void_p
_ssl.BN_new.argtypes = None

_ssl.BN_CTX_new.errcheck = _check_res_void_p
_ssl.BN_CTX_new.restype = ctypes.c_void_p
_ssl.BN_CTX_new.argtypes = None

_ssl.BN_CTX_free.restype = None
_ssl.BN_CTX_free.argtypes = [ctypes.c_void_p]

_ssl.BN_CTX_start.restype = None
_ssl.BN_CTX_start.argtypes = [ctypes.c_void_p]

_ssl.BN_CTX_end.restype = None
_ssl.BN_CTX_end.argtypes = [ctypes.c_void_p]

_ssl.BN_CTX_get.errcheck = _check_res_void_p
_ssl.BN_CTX_get.restype = ctypes.c_void_p
_ssl.BN_CTX_get.argtypes = [ctypes.c_void_p]

##################
## Operations
##################

_ssl.BN_mod_inverse.errcheck = _check_res_void_p
_ssl.BN_mod_inverse.restype = ctypes.c_void_p
_ssl.BN_mod_inverse.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                ctypes.c_void_p, ctypes.c_void_p]


_ssl.BN_mod_mul.restype = ctypes.c_int
_ssl.BN_mod_mul.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                            ctypes.c_void_p, ctypes.c_void_p,
                            ctypes.c_void_p]

_ssl.BN_mod_exp.restype = ctypes.c_int
_ssl.BN_mod_exp.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                            ctypes.c_void_p, ctypes.c_void_p,
                            ctypes.c_void_p]

##################
## BN_BLINDING
##################

_ssl.BN_BLINDING_new.errcheck = _check_res_void_p
_ssl.BN_BLINDING_new.restype = ctypes.c_void_p
_ssl.BN_BLINDING_new.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                 ctypes.c_void_p]

_ssl.BN_BLINDING_free.restype = None
_ssl.BN_BLINDING_free.argtypes = [ctypes.c_void_p]

_ssl.BN_BLINDING_invert_ex.restype = ctypes.c_int
_ssl.BN_BLINDING_invert_ex.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                       ctypes.c_void_p, ctypes.c_void_p]

_ssl.BN_BLINDING_convert_ex.restype = ctypes.c_int
_ssl.BN_BLINDING_convert_ex.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                        ctypes.c_void_p, ctypes.c_void_p]

#####################################
## RSA
#####################################

_ssl.RSA_new.errcheck = _check_res_void_p
_ssl.RSA_new.restype = ctypes.c_void_p
_ssl.RSA_new.argtypes = None

_ssl.RSA_free.restype = None
_ssl.RSA_free.argtypes = [ctypes.c_void_p]

_ssl.i2d_RSAPublicKey.restype = ctypes.c_int
_ssl.i2d_RSAPublicKey.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

_ssl.RSA_generate_key_ex.restype = ctypes.c_int
_ssl.RSA_generate_key_ex.argtypes = [ctypes.c_void_p, ctypes.c_int,
                                     ctypes.c_void_p, ctypes.c_void_p]

_ssl.RSA_blinding_on.restype = ctypes.c_int
_ssl.RSA_blinding_on.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

_ssl.RSA_size.restype = ctypes.c_int
_ssl.RSA_size.argtypes = [ctypes.c_void_p]

_ssl.RSA_private_encrypt.restype = ctypes.c_int
_ssl.RSA_private_encrypt.argtypes = [ctypes.c_int, ctypes.c_char_p,
                                     ctypes.c_void_p, ctypes.c_void_p,
                                     ctypes.c_int]

_ssl.RSA_public_encrypt.restype = ctypes.c_int
_ssl.RSA_public_encrypt.argtypes = [ctypes.c_int, ctypes.c_char_p,
                                    ctypes.c_void_p, ctypes.c_void_p,
                                    ctypes.c_int]

_ssl.RSA_private_decrypt.restype = ctypes.c_int
_ssl.RSA_private_decrypt.argtypes = [ctypes.c_int, ctypes.c_void_p,
                                     ctypes.c_void_p, ctypes.c_void_p,
                                     ctypes.c_int]

_ssl.RSA_public_decrypt.restype = ctypes.c_int
_ssl.RSA_public_decrypt.argtypes = [ctypes.c_int, ctypes.c_void_p,
                                    ctypes.c_void_p, ctypes.c_void_p,
                                    ctypes.c_int]

#####################################
## BIO
#####################################

_ssl.BIO_new_file.errcheck = _check_res_void_p
_ssl.BIO_new_file.restype = ctypes.c_void_p
_ssl.BIO_new_file.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

_ssl.BIO_free_all.restype = None
_ssl.BIO_free_all.argtypes = [ctypes.c_void_p]

#####################################
## PEM
#####################################

_ssl.PEM_write_bio_RSAPublicKey.restype = ctypes.c_int
_ssl.PEM_write_bio_RSAPublicKey.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

_ssl.PEM_write_bio_RSAPrivateKey.restype = ctypes.c_int
_ssl.PEM_write_bio_RSAPrivateKey.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                             ctypes.c_void_p,
                                             ctypes.c_char_p, ctypes.c_int,
                                             ctypes.c_void_p, ctypes.c_void_p]

_ssl.PEM_read_RSAPublicKey.errcheck = _check_res_void_p
_ssl.PEM_read_RSAPublicKey.restype = ctypes.c_void_p
_ssl.PEM_read_RSAPublicKey.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                       ctypes.c_void_p, ctypes.c_void_p]

_ssl.PEM_read_RSAPrivateKey.errcheck = _check_res_void_p
_ssl.PEM_read_RSAPrivateKey.restype = ctypes.c_void_p
_ssl.PEM_read_RSAPrivateKey.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                        ctypes.c_void_p, ctypes.c_void_p]


#####################################
## ChaCha
#####################################

class ChaCha_ctx(ctypes.Structure):
    _fields_ = [("input", ctypes.c_uint * 16),
                ("ks", ctypes.c_wchar * 64),
                ("unused", ctypes.c_ubyte)]

_ssl.ChaCha_set_key.restype = None
_ssl.ChaCha_set_key.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                ctypes.c_uint]

_ssl.ChaCha_set_iv.restype = None
_ssl.ChaCha_set_iv.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                               ctypes.c_void_p]

_ssl.ChaCha.restype = None
_ssl.ChaCha.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                        ctypes.c_void_p, ctypes.c_uint]

#####################################
## EC
#####################################

class ECDSA_SIG_st(ctypes.Structure):
    _fields_ = [("r", ctypes.c_void_p),
                ("s", ctypes.c_void_p)]
    def __del__(self):
        _ssl.BN_free(self.r)
        _ssl.BN_free(self.s)


_ssl.ECDSA_SIG_free.restype = None
_ssl.ECDSA_SIG_free.argtypes = [ctypes.c_void_p]

_ssl.d2i_ECDSA_SIG.restype = ctypes.c_void_p
_ssl.d2i_ECDSA_SIG.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_long]

_ssl.i2d_ECDSA_SIG.restype = ctypes.c_int
_ssl.i2d_ECDSA_SIG.argtypes = [ctypes.c_void_p, ctypes.c_void_p]


###########################################################################
## Helpers
###########################################################################


def _free_bn(x):
    """Frees a BN instance if it's not None."""
    if x is not None:
        _ssl.BN_free(x)


def BN_num_bytes(bn):
    """Returns the number of bytes in a BN instance."""
    return (_ssl.BN_num_bits(bn) + 7) // 8


def BNToBin(bn, size):
    """
    Converts a bn instance to a byte string of length "size".

    We make the assumption that all bin representations of BIGNUMs will be the
    same length. In semi-rare cases the bignum use than data_len bytes.  Such
    cases mean that less than data_len bytes will be written into bin, thus bin
    will contain uninitialized values. We fix this by packeting zeros in the
    front of bignum. Zeros won't impact the magnitude of bin, but will ensure
    that all bytes are initalized.

    Args:
        bn: A bn(BIGNUM) instance
        size: An int that represnts the requested size of the output string.

    Returns:
        A byte string containing the data from bn of length "size"

    """
    if bn is None:
        return None

    data = ctypes.create_string_buffer(size)
    offset = size - BN_num_bytes(bn)

    ret = _ssl.BN_bn2bin(bn, ctypes.byref(data, offset))
    if ret == 0:
        return None

    for i in range(offset):
        data[i] = 0

    return data.raw[:size]

def BinToBN(s):
    """
    Converts a binary string into a BN instance.

    Returns:
        A BN instance, or none if the conversion failed.
    """
    bn = _ssl.BN_new()

    ret = _ssl.BN_bin2bn(s, len(s), bn)

    if ret is None:
        return None

    return bn
