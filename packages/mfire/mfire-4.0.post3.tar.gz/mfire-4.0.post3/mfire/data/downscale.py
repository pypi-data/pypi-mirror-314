"""
adjust all data to some data (temperature mainly) over a finess grid
"""
import numpy as np
from pydantic import BaseModel as PydanticBaseModel

from mfire.settings import get_logger
from mfire.settings.constants import (
    DOWNSCALABLE_PARAMETERS,
    DOWNSCALE_REPLACE,
    DOWNSCALE_SOURCE,
)
from mfire.utils import mfxarray as xr
from mfire.utils import xr as xr_utils

# Logging
LOGGER = get_logger(name=__name__)


class DownScale(PydanticBaseModel):
    """
    fonctions de "mise en cohérence" fournie par le projet Alpha (L.Roger)
    d'après le document projetALPHA_principeselaborationVP_V3.0.3.odt
    """

    downscaling: dict
    grid_name: str

    def lpn(self):
        """adjust lpn"""
        lpn = self.downscaling["LPN__SOL"]["data"]
        altitude = self.downscaling["ALTITUDE__SOL"]["data"]
        precip = self.downscaling["PRECIP__SOL"]["data"]
        t = self.downscaling[DOWNSCALE_SOURCE]["data"]
        # Si VP(LPN) < 0 alors VP(LPN) = 0
        lpn = lpn.where(~(lpn < 0), 0)
        # Si VP(T) ≤ 0°C et VP(RR) > 0 et si VP(LPN) > relief, alors VP(LPN) = relief
        lpn_zone = lpn.isel(valid_time=0)
        alti_zone = altitude.where(lpn_zone, drop=True)
        vt = lpn.valid_time
        _, alti_t = xr.broadcast(vt, alti_zone)
        lpn = lpn.where(~((precip > 0) & (t <= 0) & (lpn > alti_t)), alti_t)
        self.downscaling["LPN__SOL"]["data"] = lpn

    def risqueorage_rr(self, risque_orage, precip):
        """adjust thunderstrom from precipitation"""
        # Si RR = 0 et VP(RISQUE_ORAGE) = 12 ou 13, alors VP(RISQUE_ORAGE) = 11
        return risque_orage.where(
            ~((precip == 0) & ((risque_orage == 12) | (risque_orage == 13))), 11
        )

    def risque_orage(self):
        """adjust thunderstrom"""
        risque_orage = self.downscaling["RISQUE_ORAGE__SOL"]["data"]
        precip = self.downscaling["PRECIP__SOL"]["data"]
        self.downscaling["RISQUE_ORAGE__SOL"]["data"] = self.risqueorage_rr(
            risque_orage, precip
        )

    def ptype_rr(self, ptype, precip):
        """adjust precipitation type from precipitation"""
        bruine = 0.4
        # - Si VP(RR) = 0, alors VP(PTYPE) = 0
        ptype = ptype.where(~(precip == 0), 0)
        # - Si VP(RR) > 0 et VP(PTYPE) = 0, alors VP(PTYPE) = 201
        ptype = ptype.where(~((precip > 0) & (ptype == 0)), 201)
        # - Si VP(RR) > seuil bruine et VP(PTYPE) = 11, alors VP(PTYPE) = 1
        ptype = ptype.where(~((precip > bruine) & (ptype == 11)), 1)
        # - Si VP(RR) > seuil bruine  et VP(PTYPE) = 12, alors VP(PTYPE) = 3
        ptype = ptype.where(~((precip > bruine) & (ptype == 12)), 3)
        return ptype

    def ptype_orage(self, ptype, risque_orage):
        """adjust precipitation type from thunderstrom"""
        # - si RISQUE_ORAGE ≥ 11 et VP(PTYPE) = 3 ou 11 ou 12, alors VP(PTYPE) = 1
        ptype = ptype.where(
            ~((risque_orage >= 11) & ((ptype == 3) | (ptype == 11) | (ptype == 12))), 1
        )
        return ptype

    def ptype_t(self, ptype, t):
        """adjust precipitation type from temperature"""
        deg0 = 273.15
        deg1 = deg0 + 1
        deg3 = deg0 + 3
        # - Si VP(T) > 3°C et VP(PTYPE) = 5 ou 6 ou 7 ou 193, alors VP(PTYPE) = 1
        ptype = ptype.where(
            ~(
                (t > deg3)
                & ((ptype == 5) | (ptype == 6) | (ptype == 7) | (ptype == 193))
            ),
            1,
        )
        # - Si VP(T) > 3°C et VP(PTYPE) = 205 ou 206 ou 207 ou 213,
        # alors VP(PTYPE) = 201
        ptype = ptype.where(
            ~(
                (t > deg3)
                & ((ptype == 205) | (ptype == 206) | (ptype == 207) | (ptype == 213))
            ),
            201,
        )
        # - Si VP(T) > 1°C et VP(PTYPE) = 3 ou 8, alors VP(PTYPE) = 1
        ptype = ptype.where(~((t > deg1) & ((ptype == 3) | (ptype == 8))), 1)
        # - Si VP(T) > 1°C et VP(PTYPE) = 12, alors VP(PTYPE) = 11
        ptype = ptype.where(~((t > deg1) & (ptype == 12)), 11)
        return ptype

    def ptype_tlpn(self, ptype, t, lpn, altitude):
        """adjust precipitation type from temperature and snow limit"""

        deg0 = 273.15
        deg3 = deg0 + 3
        # - Si VP(T) > 0°C  et VP(PTYPE) = 1 ou 11 et VP(LPN) ≤ altitude du point +10m,
        #    alors VP(PTYPE) = 7
        ptype = ptype.where(
            ~((t > deg0) & ((ptype == 1) | (ptype == 11)) & (lpn < altitude + 10)), 7
        )
        # Si VP(T) > 0°C  et VP(PTYPE) = 201
        #  et VP(LPN) ≤ altitude du point de grille +10m,
        # alors VP(PTYPE) = 207
        ptype = ptype.where(~((t > deg0) & (ptype == 201) & (lpn < altitude + 10)), 207)
        # Si 0°C ≤ VP(T) ≤  3°C  et VP(PTYPE) = 5 ou 6 ou 193
        # et VP(LPN) >  altitude du point de grille,
        # alors VP(PTYPE) = 1
        ptype = ptype.where(
            ~(
                (t >= deg0)
                & (t <= deg3)
                & ((ptype == 5) | (ptype == 6) | (ptype == 193))
                & (lpn > altitude)
            ),
            1,
        )
        # Si 0°C ≤ VP(T) ≤  3°C  et VP(PTYPE) = 205 ou 206 ou 213
        # et VP(LPN) >  altitude du point de grille,
        # alors VP(PTYPE) =  201
        ptype = ptype.where(
            ~(
                (t >= deg0)
                & (t <= deg3)
                & ((ptype == 205) | (ptype == 206) | (ptype == 213))
                & (lpn > altitude)
            ),
            201,
        )
        return ptype

    def ptype_tpost(self, ptype, t):
        """adjust precipitation type from temperature : post-processing"""

        deg0 = 273.15
        # - Si VP(T) < 0°C et VP(PTYPE) = 1 ou 11 ou 7, alors VP(PTYPE) = 6
        ptype = ptype.where(
            ~((t < deg0) & ((ptype == 1) | (ptype == 11) | (ptype == 7))), 6
        )
        # - Si VP(T) < 0°C et VP(PTYPE) = 201 ou 207, alors VP(PTYPE) = 206
        ptype = ptype.where(~((t < deg0) & ((ptype == 201) | (ptype == 207))), 206)
        return ptype

    def ptype_post(self, ptype):
        """adjust precipitation type : post-processing"""

        # - Si VP(PTYPE) = 9 ou 10, alors VP(PTYPE) = 1
        ptype = ptype.where(~((ptype == 9) | (ptype == 10)), 1)
        return ptype

    def ptype(self):
        """adjust precipitation type"""

        ptype = self.downscaling["PTYPE__SOL"]["data"]
        precip = self.downscaling["PRECIP__SOL"]["data"]
        risque_orage = self.downscaling["RISQUE_ORAGE__SOL"]["data"]
        t = self.downscaling[DOWNSCALE_SOURCE]["data"]
        lpn = self.downscaling["LPN__SOL"]["data"]
        altitude = self.downscaling["ALTITUDE__SOL"]["data"]
        ptype = self.ptype_rr(ptype, precip)
        ptype = self.ptype_orage(ptype, risque_orage)
        ptype = self.ptype_t(ptype, t)
        ptype = self.ptype_tlpn(ptype, t, lpn, altitude)
        ptype = self.ptype_tpost(ptype, t)
        ptype = self.ptype_post(ptype)
        self.downscaling["PTYPE__SOL"]["data"] = ptype

    def eau(self):
        """adjust liquid water"""

        ptype = self.downscaling["PTYPE__SOL"]["data"]
        precip = self.downscaling["PRECIP__SOL"]["data"]
        eau = self.downscaling["EAU__SOL"]["data"]
        eau = eau.where(
            ~(
                (ptype == 3)
                | (ptype == 9)
                | (ptype == 10)
                | (ptype == 11)
                | (ptype == 12)
                | (ptype == 1)
                | (ptype == 201)
                | (ptype == 7)
                | (ptype == 207)
            ),
            precip,
        )
        eau = eau.where(
            ~(
                (ptype == 0)
                | (ptype == 5)
                | (ptype == 6)
                | (ptype == 8)
                | (ptype == 193)
                | (ptype == 205)
                | (ptype == 206)
                | (ptype == 213)
            ),
            0,
        )
        self.downscaling["EAU__SOL"]["data"] = eau

    def neipot(self):
        """adjust snow"""

        deg0 = 273.15
        rho_min = 50  # kg.m-3
        rho_a = 109  # kg.m-3
        rho_b = 6  # kg.m-3.K-1
        rho_c = 26  # kg.m-7/2.s1/2
        ptype = self.downscaling["PTYPE__SOL"]["data"]
        precip = self.downscaling["PRECIP__SOL"]["data"]
        ff = self.downscaling["FF__HAUTEUR10"]["data"]
        t = self.downscaling[DOWNSCALE_SOURCE]["data"]
        neipot = self.downscaling["NEIPOT__SOL"]["data"]
        neipot = neipot.where(
            ~(
                (ptype == 0)
                | (ptype == 3)
                | (ptype == 9)
                | (ptype == 10)
                | (ptype == 11)
                | (ptype == 12)
                | (ptype == 1)
                | (ptype == 201)
                | (ptype == 7)
                | (ptype == 207)
            ),
            0,
        )
        static = precip / rho_min
        dynamic = precip / (rho_a + rho_b * (t - deg0) + rho_c * np.sqrt(ff))
        neige = xr.where(static < dynamic, static, dynamic)
        neipot = neipot.where(
            ~(
                (ptype == 5)
                | (ptype == 6)
                | (ptype == 8)
                | (ptype == 193)
                | (ptype == 205)
                | (ptype == 206)
                | (ptype == 213)
            ),
            neige,
        )
        self.downscaling["NEIPOT__SOL"]["data"] = neipot

    def wwmf_violent(self, wwmf, risque_orage, ptype, raf, precip):
        """adjust weather from storm"""

        # Si [(VP(RISQUE_ORAGE) = 12 ou 13) et VP(FF_RAF_10m) ≥ 100 km/h
        # et (VP(PTYPE) = 10 ou VP(RR)>=50mm/h)]
        # alors VP(WWMF) = 99 orages violents
        kmh100 = 27.778  # m.s-1
        # GPL_TODO : precip par heure ????
        return wwmf.where(
            ~(
                ((risque_orage == 12) | (risque_orage == 13))
                & (raf >= kmh100)
                & ((ptype == 10) | (precip > 50))
            ),
            99,
        )

    def wwmf_orage(self, wwmf, risque_orage, ptype):
        """adjust weather from thunderstorm"""
        # Si (VP(RISQUE_ORAGE) > 11 et VP(PTYPE) = 9 ou 10)
        # alors VP(WWMF) = 98 orages avec grêle
        wwmf = wwmf.where(~((risque_orage > 11) & ((ptype == 9) | (ptype == 10))), 98)
        # Si (VP(RISQUE_ORAGE) > 11 et VP(PTYPE) = 5,6,7,8,193,205,206,207,213)
        #    alors VP(WWMF) = 97 orages avec neige
        wwmf = wwmf.where(
            ~(
                (risque_orage > 11)
                & (
                    (ptype == 5)
                    | (ptype == 6)
                    | (ptype == 7)
                    | (ptype == 8)
                    | (ptype == 193)
                    | (ptype == 205)
                    | (ptype == 206)
                    | (ptype == 207)
                    | (ptype == 213)
                )
            ),
            97,
        )
        # Si (VP(RISQUE_ORAGE) >11 et VP(PTYPE) = 1 ou 201)
        # alors VP(WWMF) = 93 orages avec pluie
        wwmf = wwmf.where(~((risque_orage > 11) & ((ptype == 1) | (ptype == 201))), 93)
        # Si (VP(RISQUE_ORAGE) = 11 et VP(PTYPE) ≠ 0)
        # alors VP(WWMF) = 92 averses orageuses
        wwmf = wwmf.where(~((risque_orage == 11) & (ptype != 0)), 92)
        # Si (VP(RISQUE_ORAGE) = 11 et VP(PTYPE) = 0)
        # alors VP(WWMF) = 91 orages possibles
        wwmf = wwmf.where(~((risque_orage == 11) & (ptype == 0)), 91)
        return wwmf

    def wwmf_ptype(self, wwmf, ptype):
        """adjust weather from precipitation type"""
        # il faut RESPECTER l'ORDRE ! ! !

        # Si VP(PTYPE) = 11 alors VP(WWMF) = 40 bruine
        wwmf = wwmf.where(~(ptype == 11), 40)
        # Si (VP(PTYPE) = 207 et VP(NEBUL) ≥ 90 %)
        # alors VP(WWMF) = 78 averses de pluie et neige mêlées avec ciel couvert
        # Si (VP(PTYPE) = 207 et VP(NEBUL) < 90 %)
        # alors VP(WWMF) = 77 averses de pluie et neige mêlées
        # GPL_TODO : prendre en compte de la Nebul
        wwmf = wwmf.where(~(ptype == 207), 77)
        # Si VP(PTYPE) = 7  alors VP(WWMF) = 58 pluie et neige mêlées
        wwmf = wwmf.where(~(ptype == 7), 58)
        # Si VP(PTYPE) = 9  alors  VP(WWMF) = 84 averses de grésil
        wwmf = wwmf.where(~(ptype == 9), 84)
        # Si VP(PTYPE) = 12  alors VP(WWMF) = 49 bruine verglaçante
        wwmf = wwmf.where(~(ptype == 12), 49)
        # Si VP(PTYPE) = 3 alors VP(WWMF) = 59 pluie verglaçante
        wwmf = wwmf.where(~(ptype == 3), 59)
        # Si VP(PTYPE) = 10 alors VP(WWMF) = 85 averses de grêle
        wwmf = wwmf.where(~(ptype == 10), 85)
        return wwmf

    def wwmf_precip(self, wwmf, precip, ptype):
        """adjust weather from precipitation"""
        fort = 7.6
        faible = 2.5
        # il faut RESPECTER l'ORDRE ! ! !

        # JJ1 Si (VP(PTYPE) = 1 et VP(RR) < seuil faible)
        # alors VP(WWMF) = 51 pluie faible
        # J2+ Si (VP(PTYPE) = 1,3,12 et VP(RR) < seuil faible)
        # alors VP(WWMF) = 51 pluie faible
        wwmf = wwmf.where(
            ~(((ptype == 1) | (ptype == 3) | (ptype == 12)) & (precip < faible)), 51
        )
        # Si (VP(PTYPE) = 201 et VP(NEBUL) ≥ 90 % et VP(RR) < seuil faible)
        # alors VP(WWMF) = 72 rares averses avec ciel couvert
        # Si (VP(PTYPE) = 201 et VP(NEBUL) < 90 % et VP(RR) < seuil faible)
        # alors VP(WWMF) = 71 rares averses
        wwmf = wwmf.where(~((ptype == 201) & (precip < faible)), 71)
        # JJ1 Si (VP(PTYPE) = 1 et VP(RR) ≥ seuil faible)
        # alors VP(WWMF) = 52 pluie modérée
        # J2+ Si (VP(PTYPE) = 1, 3, 12 et VP(RR) ≥ seuil faible)
        # alors VP(WWMF) = 52 pluie modérée
        wwmf = wwmf.where(
            ~(
                ((ptype == 1) | (ptype == 3) | (ptype == 12))
                & (precip >= faible)
                & (precip < fort)
            ),
            52,
        )
        # Si (VP(PTYPE) = 201 et VP(NEBUL) ≥ 90 % et VP(RR) ≥ seuil faible)
        # alors VP(WWMF) = 73 averses avec ciel couvert
        # Si (VP(PTYPE) = 201 et VP(NEBUL) <90 % et VP(RR) ≥ seuil faible)
        # alors VP(WWMF) = 70 averses
        # GPL_TODO : prendre en compte de la Nebul
        wwmf = wwmf.where(~((ptype == 201) & (precip >= faible) & (precip < fort)), 70)
        # JJ1 Si (VP(PTYPE) = 1,201 et VP(RR) ≥ seuil fort)
        # alors VP(WWMF) = 53 pluie forte
        # J2+ Si (VP(PTYPE) = 1, 3, 12, 201 et VP(RR) ≥  seuil fort)
        # alors VP(WWMF) = 53 pluie forte
        # Si (VP(PTYPE) = 1, 3, 12, 201 et VP(RR) ≥  seuil fort)
        # alors VP(WWMF) = 53 pluie forte
        wwmf = wwmf.where(
            ~(
                ((ptype == 1) | (ptype == 3) | (ptype == 12) | (ptype == 201))
                & (precip >= fort)
            ),
            53,
        )
        # Si (VP(PTYPE) = 5,6,8,193 et VP(RR) < seuil faible)
        # alors VP(WWMF) =  61 neige faible
        wwmf = wwmf.where(
            ~(
                ((ptype == 5) | (ptype == 6) | (ptype == 8) | (ptype == 193))
                & (precip < faible)
            ),
            61,
        )
        # Si (VP(PTYPE) = 205,206,213 et VP(NEBUL) ≥ 90 % et VP(RR) < seuil faible)
        # alors VP(WWMF) = 82 rares averses de neige avec ciel couvert
        # Si (VP(PTYPE) = 205,206,213 et VP(NEBUL) < 90 % et VP(RR) < seuil faible)
        # alors VP(WWMF) = 81 rares averses de neige
        # GPL_TODO : prendre en compte de la Nebul
        wwmf = wwmf.where(
            ~(((ptype == 205) | (ptype == 206) | (ptype == 213)) & (precip < faible)),
            81,
        )
        # Si (VP(PTYPE) = 5,6,8,193 et VP(RR) ≥ seuil faible)
        # alors VP(WWMF) = 62 neige modérée
        wwmf = wwmf.where(
            ~(
                ((ptype == 5) | (ptype == 6) | (ptype == 8) | (ptype == 193))
                & (precip >= faible)
                & (precip < fort)
            ),
            62,
        )
        # Si (VP(PTYPE) = 205,206,213 et VP(NEBUL) ≥ 90 % et VP(RR) ≥ seuil faible)
        # alors VP(WWMF) = 83 averses de neige avec ciel couvert
        # Si (VP(PTYPE) = 205,206,213 et VP(NEBUL)<90 % et VP(RR) ≥ seuil faible)
        # alors  VP(WWMF) =  80 averses de neige
        # GPL_TODO : prendre en compte de la Nebul
        wwmf = wwmf.where(
            ~(
                ((ptype == 205) | (ptype == 206) | (ptype == 213))
                & (precip >= faible)
                & (precip < fort)
            ),
            80,
        )
        # Si (VP(PTYPE) = 5,6,8,193,205,206,213 et VP(RR) ≥ seuil fort)
        # alors VP(WWMF) = 63 neige forte
        wwmf = wwmf.where(
            ~(
                (precip >= fort)
                & (
                    (ptype == 5)
                    | (ptype == 6)
                    | (ptype == 8)
                    | (ptype == 193)
                    | (ptype == 205)
                    | (ptype == 206)
                    | (ptype == 213)
                )
            ),
            63,
        )
        return wwmf

    def wwmf(self):
        """adjust weather"""

        ptype = self.downscaling["PTYPE__SOL"]["data"]
        precip = self.downscaling["PRECIP__SOL"]["data"]
        risque_orage = self.downscaling["RISQUE_ORAGE__SOL"]["data"]
        raf = self.downscaling["RAF__HAUTEUR10"]["data"]
        wwmf = self.downscaling["WWMF__SOL"]["data"]
        # il faut RESPECTER l'ORDRE ! ! !
        # precip puis ptype à cause de ptype=3|12
        wwmf = self.wwmf_precip(wwmf, precip, ptype)
        wwmf = self.wwmf_ptype(wwmf, ptype)
        wwmf = self.wwmf_orage(wwmf, risque_orage, ptype)
        wwmf = self.wwmf_violent(wwmf, risque_orage, ptype, raf, precip)
        # GPL_TODO : TYPE_FG et NEBUL
        # GPL_TODO : J4+
        self.downscaling["WWMF__SOL"]["data"] = wwmf

    def add_altitude(self):
        """add altitude to data list"""
        altitude = xr_utils.ArrayLoader.load_altitude(grid_name=self.grid_name)
        self.downscaling.update({"ALTITUDE__SOL": {"data": altitude}})

    def interpolate(self, mask):
        """interpolate data as temperature over finess grid"""
        for param in DOWNSCALABLE_PARAMETERS:
            if param in self.downscaling:
                data = self.downscaling[param]["data"]
                data = xr_utils.interpolate_to_new_grid(data, self.grid_name)
                if mask is not None:
                    data = data.where(mask, drop=True)
                self.downscaling[param]["data"] = data

    def remove_t_altitude(self):
        """remove temporary data from list to export"""
        self.downscaling.pop("ALTITUDE__SOL")
        self.downscaling.pop(DOWNSCALE_SOURCE)

    def fill_missing(self):
        """replace t_as with t when missing"""
        data = self.downscaling.get(DOWNSCALE_REPLACE, {}).get("data", None)
        mask = self.downscaling.get(DOWNSCALE_SOURCE, {}).get("data", None)
        if data is None:
            if mask is None:
                raise ValueError(
                    f"Neither {DOWNSCALE_REPLACE} nor {DOWNSCALE_SOURCE} available"
                )
            return {"data": mask}
        data = xr_utils.interpolate_to_new_grid(data, self.grid_name)
        if mask is None:
            return {"data": data}
        return {"data": mask.combine_first(data)}

    def down_scaling_data(self):
        """
        l'ordre est important puisque les codes sont modifiés à chaque étape
        risque_orage
        ptype
        eau
        neipot
        wwmf
        """
        self.downscaling[DOWNSCALE_SOURCE] = self.fill_missing()
        self.interpolate(self.downscaling[DOWNSCALE_SOURCE]["data"])
        self.add_altitude()
        self.lpn()
        self.risque_orage()
        self.ptype()
        self.eau()
        self.neipot()
        self.wwmf()
        self.remove_t_altitude()
