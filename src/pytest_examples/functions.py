from math import sqrt

import numpy as np
import pandas as pd


def is_prime(number: int) -> bool:
    """Check if the given number is a prime number.

    Args:
        number: The number to check.

    Returns:
        True if the number is a prime number. False otherwise.
    """
    if not isinstance(number, int):
        raise TypeError("Number must be an integer.")
    if number <= 1:
        return False
    for i in range(2, int(sqrt(number)) + 1):
        if number % i == 0:
            return False
    return True


# Copied from stat-finansregnskapet/Inndata/UT_dapla/UT11_Valutaomvurderinger.py
def valuta_omv(inndata: pd.DataFrame, val_data: pd.DataFrame) -> pd.DataFrame:
    """Valuta omvurdering.

    Args:
        inndata: Dataframe with inndata
        val_data: Dataframe with exchange rates

    Returns:
        A dataframe with reassessed values.
    """
    koblet = pd.merge(
        inndata,
        val_data[["valuta", "periode", "obs_value", "obs_value_last"]],
        on=["valuta", "periode"],
        how="left",
    )

    # Denne må tilpasses, siden altinn skal ha andre nivåer enn filrapp (objekt, sektor)
    gruppert = koblet.groupby(["rapp_orgnr", "post", "und_post", "objekt", "valuta"])

    val_omv = []

    for _, group in gruppert:
        sortert = group.sort_values("periode")
        sortert["beh_endr"] = sortert["verdi_lf"].transform(lambda x: x - x.shift())
        sortert["beh_val"] = sortert["verdi_lf"] / sortert["obs_value_last"]
        sortert["beh_endr_val"] = sortert["beh_val"].transform(lambda x: x - x.shift())
        sortert["val_beh_trans_nok"] = sortert["beh_endr_val"] * sortert["obs_value"]
        # Omvurderinger settes til 0 hvis beholdningsendring er 0
        sortert["restbest_omv"] = np.where(
            sortert["beh_endr"] != 0,
            sortert["beh_endr"] - sortert["val_beh_trans_nok"],
            0,
        )
        val_omv.append(sortert)

    # Endre return hvis vi bare vil ha ut en summering av omvurderingene
    # Hvis det ikke er data returneres et tomt datasett
    try:
        return pd.concat(val_omv)
    except ValueError:
        print("WARNING! Empty DataFrame returned")
        return koblet
