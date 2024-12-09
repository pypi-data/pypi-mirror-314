from dataclasses import dataclass
from typing import Mapping

FORUM_ABBREVIATIONS: Mapping[int, str] = {
    1: "RIP",
    21: "55555",
    22: "SH/SC",
    25: "11111",
    26: "FYAD",
    27: "ADTRW",
    31: "CC",
    43: "GM",
    44: "GAMES",
    46: "D&D",
    61: "SAMART",
    90: "TCC",
    91: "AI",
    122: "SAS",
    124: "PI",
    130: "TVIV",
    132: "TFR",
    144: "BSS",
    150: "NMD",
    151: "CD",
    158: "A/T",
    161: "GWS",
    167: "PYF",
    179: "YLLS",
    182: "TBB",
    188: "QCS",
    192: "IYG",
    210: "DIY",
    215: "PHIZ",
    218: "GIP",
    241: "LAN",
    242: "P/C",
    255: "RGD",
    268: "BYOB",
    269: "C-SPAM",
    272: "RSF",
    273: "GBS",
    686: "SAD",
}


@dataclass
class Forum:
    id: int
    name: str

    @property
    def abbreviation(self) -> str:
        return FORUM_ABBREVIATIONS[self.id]
