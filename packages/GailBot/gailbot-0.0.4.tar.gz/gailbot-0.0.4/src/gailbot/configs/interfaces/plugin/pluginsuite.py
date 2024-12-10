# -*- coding: utf-8 -*-
# @Author: Jason Y. Wu
# @Date:   2023-07-17 19:21:51
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-09 18:34:34
from dataclasses import dataclass


@dataclass
class PLUGIN_CONFIG:
    HILAB_BUCKET = "gailbot-plugin-suite-official"
    EN_KEY = b"25T_bNAjTALUgva1C-au0IKwESptsLAztLRVVEyCtZs="
    ENCRYPTED_API_ID = b"gAAAAABkU5CF3GwKfqwPBvgG4fibAHjZ2hE1pQdEb8Nkw06YubGZ9_mekBRgMiRXPrXo7C_6i-uuBpisZyL3FpFwg8zXvxR9_jrPocUkMjSmyHFJQUYojys="
    ENCRYPTED_API_KEY = b"gAAAAABkU5CF1Q_ebrx9OTuW0WWQypQKTk25JPPIrRGAyoDLgweyh-2tDnD4CdmUE_xpprxVMttgvz7FzR2sDMn6jJ3EyYNxUCHgudOBkwPoYYM7a6fMheNLlyT3x_SzszpnxfF2y7-m"
    THREAD_NUM = 3
    REQUIREMENT = "requirements.txt"
    OFFICIAL = ".gb_official"
    CONFIG = "suite_info.toml"
    FORMAT = "format.md"
    HILAB_SUITE_ZIP = "https://gailbot-official-plugin-suite.s3.us-east-2.amazonaws.com/HiLabSuite.zip"
    OFFICIAL_KEY = b"KM1V0_HijdrehPVsFueXISED2Jxs0S_rR9zKAJzcW3A="
    OFFICIAL_ENKEY = b"q6LGp_5jjEQyZu3ydl88H2adl_RRZCyw4IMXqYXnga8="
