import re
import numpy as np

from buildupp.configuration import Config
from buildupp.utils import myplot

class Blend:

    @staticmethod
    def compute_surface(diameter):
        surface = 4 * np.pi * (diameter / 2) ** 2
        return surface

    @staticmethod
    def compute_volume(diameter):
        volume = 4 / 3 * np.pi * (diameter / 2) ** 3
        return volume

    def __init__(self,
                 composition: str,
                 config: Config = Config(),):

        self.config = config
        self.prop = self.config.powder_properties

        self.composition = composition
        self.pairs = self.get_pairs()

        self.density_gpcm3 = self.get_density(units="g/cm3")
        self.ssa_bet_m2pg = self.get_ssa_bet(units="m2/g")

        self.psd_dict = self.get_psd_dict()
        self.psd_diameters_mum = self.psd_dict.get("diameters_mum", 0)
        self.psd_fractions_pc = self.psd_dict.get("fractions_pc", 0)
        self.psd_cumulatives_pc = self.psd_dict.get("cumulatives_pc", 0)

        self.d10 = np.interp(
            10, self.psd_cumulatives_pc, self.psd_diameters_mum
        )  # 10% cumulative fraction
        self.d50 = np.interp(
            50, self.psd_cumulatives_pc, self.psd_diameters_mum
        )  # 50% cumulative fraction
        self.d90 = np.interp(
            90, self.psd_cumulatives_pc, self.psd_diameters_mum
        )  # 90% cumulative fraction

        self.ds = self.compute_ds()
        self.ssa_from_psd_m2pg = self.compute_ssa_from_psd(units="m2/g")

        self.rouf = self.compute_rou_over_F()

    def get_pairs(self) -> list:
        """For a given (blend) composition,
        extract pairs of powder fraction and powder ID
        Example:
            extract_pairs('85opc15ls') -> [('85', 'opc'), ('15', 'ls')]

        Args:
            composition (str): The composition of the blend, e.g '85opc15ls' or '55opc45mk'

        Returns:
            list: list of tuples (fraction (str), powder ID (str))
        """

        if self.composition == "lc355" or self.composition == "lc3":
            pairs = [("53.4", "opc"), ("1.6", "gyps"), ("15", "ls"), ("30", "mk")]
        elif self.composition == "lc3_1to1":
            pairs = [("53.4", "opc"), ("1.6", "gyps"), ("22.5", "ls"), ("22.5", "mk")]
        else:
            pairs = re.findall(r"(\d+)([a-zA-Z-]+)", self.composition)

        return pairs

    def get_psd_dict(self):
        """Compute and return the weighted PSD (Particle Size Distribution) values.

        Returns:
            dict: A dictionary containing weighted diameters, fractions, and cumulative percentages.
        """
        # Initialize empty lists to store weighted values
        weighted_diameter = []
        weighted_fraction = []
        weighted_cumulative = []

        # Loop through each material in the pairs
        for num, mat in self.pairs:
            # Load PSD data for the material using the Config object
            psd_df = self.config.get_psd_data(mat)
            
            # Convert fraction to float (the amount of material in the blend)
            num = float(num)  # Convert the amount to a float

            # Make sure the PSD dataframe has the necessary columns
            if not all(col in psd_df.columns for col in ["diameter_mum", "fraction_pc", "cumulative_pc"]):
                raise ValueError(f"Missing required PSD columns for material: {mat}")

            # Weight the PSD values by the material fraction
            diameter = (num / 100) * psd_df["diameter_mum"].values
            frac = (num / 100) * psd_df["fraction_pc"].values
            cumul = (num / 100) * psd_df["cumulative_pc"].values

            # Append the weighted values to the lists
            weighted_diameter.extend(diameter)
            weighted_fraction.extend(frac)
            weighted_cumulative.extend(cumul)

        # Convert the lists to numpy arrays
        weighted_diameter = np.array(weighted_diameter)
        weighted_fraction = np.array(weighted_fraction)
        weighted_cumulative = np.array(weighted_cumulative)

        return {
            "diameters_mum": weighted_diameter,
            "fractions_pc": weighted_fraction,
            "cumulatives_pc": weighted_cumulative,
        }

    def get_density(self, units="g/cm3") -> float:
        """Return the density in the specified unit.

        Args:
            units (str): The desired unit of density. Options: 'g/cm3', 'g/m3'.

        Returns:
            float: The density in the specified unit.
        """

        if self.composition == "lc355" or self.composition == "lc3":
            total_density = (
                0.534 * self.prop["opc"]["density_gpcm3"]
                + 0.016 * self.prop["gyps"]["density_gpcm3"]
                + 0.15 * self.prop["ls"]["density_gpcm3"]
                + 0.3 * self.prop["mk"]["density_gpcm3"]
            )

        elif self.composition == "lc3_1to1":
            total_density = (
                0.534 * self.prop["opc"]["density_gpcm3"]
                + 0.016 * self.prop["gyps"]["density_gpcm3"]
                + 0.225 * self.prop["ls"]["density_gpcm3"]
                + 0.225 * self.prop["mk"]["density_gpcm3"]
            )

        else:
            total_density = 0
            for num, mat in self.pairs:
                num = float(num)
                mat_density = self.prop.get(mat).get("density_gpcm3", 0)
                total_density += (num / 100) * float(mat_density)

        if units == "g/cm3":
            return total_density

        elif units == "g/m3":
            return total_density * 1_000_000  # 1 g/cm3 = 1,000,000 g/m3

        else:
            raise ValueError("Unsupported unit. Use 'g/cm3' or 'g/m3'")

    def get_ssa_bet(self, units="m2/g") -> float:
        """Return the BET SSA in the specified unit.

        Args:
            units (str): The desired unit of density.
                         Options: 'gm2/g' (default).

        Returns:
            float: The BET SSA in the specified unit.
        """

        if self.composition == "lc355" or self.composition == "lc3":
            total_ssa = (
                0.534 * self.prop["opc"]["ssa_bet_m2pg"]
                + 0.016 * self.prop["gyps"]["ssa_bet_m2pg"]
                + 0.15 * self.prop["ls"]["ssa_bet_m2pg"]
                + 0.3 * self.prop["mk"]["ssa_bet_m2pg"]
            )
        elif self.composition == "lc3_1to1":
            total_ssa = (
                0.534 * self.prop["opc"]["ssa_bet_m2pg"]
                + 0.016 * self.prop["gyps"]["ssa_bet_m2pg"]
                + 0.225 * self.prop["ls"]["ssa_bet_m2pg"]
                + 0.225 * self.prop["mk"]["ssa_bet_m2pg"]
            )
        else:
            total_ssa = 0
            for num, mat in self.pairs:
                num = float(num)
                mat_ssa = self.prop.get(mat).get("ssa_bet_m2pg", 0)
                total_ssa += (num / 100) * float(mat_ssa)

        if units == "m2/g":
            return total_ssa

        else:
            raise NotImplementedError("Specified units not implemented. Use m2/g.")

    def compute_ds(self, decimals=1):
        """Calculate the weighted average surface diameter based on PSD data.

        Args:
            decimals (int): The number of decimal places to round the result
                            Default is 1 decimal place.

        Returns:
            float: The weighted average surface diameter rounded to the specified number of decimal places.
        """
        s_tot = 0  # Total surface area sum
        sum_sidi = 0  # Weighted sum of surface area times diameter

        for diameter, fraction in zip(self.psd_diameters_mum, self.psd_fractions_pc):

            if np.isnan(diameter) or np.isnan(fraction):
                continue

            di = diameter  # Current diameter
            si = self.compute_surface(diameter=di)

            s_tot += si * fraction
            sum_sidi += si * di * fraction

        d_s = sum_sidi / s_tot

        return round(d_s, decimals)

    def compute_ssa_from_psd(self, units="m2/g", decimals=5):
        s_tot_m2 = 0
        v_tot_cm3 = 0

        for diameter, fraction in zip(self.psd_diameters_mum, self.psd_fractions_pc):

            di_surface = diameter * fraction * 1 / (1000 * 1000)  # mum into m
            di_volume = diameter * fraction * 1 / (1000 * 10)  # mum into cm

            si_m2 = self.compute_surface(diameter=di_surface)
            vi_cm3 = self.compute_volume(diameter=di_volume)

            s_tot_m2 += si_m2
            v_tot_cm3 += vi_cm3

        mass_g = self.get_density(units="g/cm3") * v_tot_cm3
        ssa = s_tot_m2 / mass_g

        if units == "m2/g":
            return round(ssa, decimals)

        else:
            raise NotImplementedError("Specified units not implemented. Use m2/g.")

    def compute_rou_over_F(self):
        """
        Computes the ratio between roughness factor and form factor
        according to The needle model from Ouzia (CCR 2019)
        """
        s_spe = self.ssa_bet_m2pg
        M = self.density_gpcm3 * 1e6  # in m3

        # last entry contains nan for some reason
        rs = self.psd_diameters_mum[:-1] * 1e-6 / 2  # radius in m
        pofr = self.psd_fractions_pc[:-1]

        num = 0
        denom = 0

        for i in range(len(rs)):
            # Skip if rs or pofr is NaN
            if np.isnan(rs[i]) or np.isnan(pofr[i]):
                continue  # Skip this iteration

            num += rs[i] ** 3 * pofr[i]
            denom += rs[i] ** 2 * pofr[i]

        # Handle zero denominator case
        if denom == 0:
            print("Error: Denominator is zero, returning error code -1")
            return -1  # Return an error code (-1) when the denominator is zero

        rouf = round(1 / 3 * s_spe * M * num / denom, 2)
        return rouf

    def plot_psd_fractions(self, ax=None, lbl=True, type="semilogx", **kwargs):

        myplot(
            ax=ax,
            x=self.psd_diameters_mum,
            y=self.psd_fractions_pc,
            xlbl=rf"diameter [$\mu$m]",
            ylbl=rf"diff. [%]",
            lbl=lbl,
            type=type,
            **kwargs,
        )

    def plot_psd_cumulatives(self, ax=None, lbl=True, type="semilogx", **kwargs):

        myplot(
            ax=ax,
            x=self.psd_diameters_mum,
            y=self.psd_cumulatives_pc,
            xlbl=rf"diameter [$\mu$m]",
            ylbl=rf"cumul. [%]",
            lbl=lbl,
            type=type,
            **kwargs,
        )
