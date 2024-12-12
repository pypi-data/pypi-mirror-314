import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
from scipy.optimize import curve_fit

from pranzo import Analyzer
from buildupp.blend import Blend
from buildupp.hydration import Hydration

from buildupp.configuration import Config
from buildupp.utils import myplot


class Experiment:

    @staticmethod
    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx

    @staticmethod
    def convert_wc_to_decimal(s):
        match = re.search(r"wc(\d+)", s)
        if match:
            number = int(match.group(1))
            # Convert to decimal
            decimal_value = number / 100
            return decimal_value
        else:
            return None

    C3S_hydration = {
        "reactants": {"solids": {"C3S": 1}, "liquids": {"H": 3.43}},
        "products": {"solids": {"C1.67SH2.1": 1, "CH": 1.33}, "liquids": {}},
    }

    water_density_gpcm3 = 1

    def __init__(
        self,
        params: dict = None,
        config: Config = Config(),
        tstart: float = None,
        tmax: float = None,
        chemical_reaction: dict = None,
    ) -> None:

        self.config = config
        self.params = self.config.systems_measured.default[0] if params is None else params

        self.df = self.params.get("db_entry")
        self.onset_time_s = self.params.get("onset_time_s", 7500)
        self.calo_rescale = self.params.get("rescale_heat", 1)
        self.composition = self.params.get("composition", "100opc")
        self.blend = Blend(self.composition)
        self.wc = self.convert_wc_to_decimal(self.params.get("wc_string", "wc36"))
        self.mk_content_str = self.params.get("mk_content_string", "0mk")
        self.mk_content = float(re.findall(r"\d+\.?\d*", self.mk_content_str)[0])

        self.tstart = self.params.get("tstart", 3600) if tstart is None else tstart
        self.tmax = self.params.get("tmax", 4 * 3500) if tmax is None else tmax

        self.chemical_reaction = (
            self.params.get("chemical_reaction", self.C3S_hydration)
            if chemical_reaction is None
            else chemical_reaction
        )

        try:
            self.hydration = Hydration(
                chem_reaction=self.chemical_reaction, config=self.config
            )
        except FileNotFoundError:
            print(f"Cannot locate config file chemistry_database.ini")

        self.ssa_m2pg = self.blend.ssa_bet_m2pg
        self.solids_density_gpcm3 = self.blend.density_gpcm3
        self.volfrac = 1 / (
            1
            + self.wc * self.solids_density_gpcm3 / self.water_density_gpcm3
        )

        self.anlzr = Analyzer(self.df)
        self.calo = self.anlzr.calo
        self.rheo = self.anlzr.rheo.phase("p2")

        self.t = np.linspace(self.tstart, self.tmax, 10000)
        h = self.calo.interpolate("norm_heat_flow_Wpgbinder", self.t)
        H = self.calo.interpolate("norm_heat_Jpgbinder", self.t)
        self.G = self.rheo.interpolate("storage_modulus_Pa", self.t, cutoff=0.008)

        self.h, self.H = h * self.calo_rescale, H * self.calo_rescale
        self.onset_idx = self.find_nearest(self.t, self.onset_time_s)

        self.DH = self.H - self.H[self.onset_idx]
        self.G0 = self.G[self.onset_idx]
        self.Gtilde = self.G / self.G[self.onset_idx]

        self.Dm_tot_gpgbinder = self.DH * self.hydration.mu_tot_gpJ
        self.Dm_s_gpgbinder = self.DH * self.hydration.mu_s_gpJ
        self.Dm_l_gpgbinder = self.DH * self.hydration.mu_l_gpJ

        self.DV_tot_cm3pgbinder = self.DH * self.hydration.nu_tot_cm3pJ
        self.DV_s_cm3pgbinder = self.DH * self.hydration.nu_s_cm3pJ
        self.DV_l_cm3pgbinder = self.DH * self.hydration.nu_l_cm3pJ
        self.DV_s_products_cm3pgbinder = self.DH * self.hydration.nu_s_products_cm3pJ

        self.DHperSgrain_Jpm2 = self.DH / self.ssa_m2pg
        self.DVproductsperSgrain_cm3pm2 = self.DV_s_products_cm3pgbinder / self.ssa_m2pg
        self.DVproductsperVgrain = self.DV_s_cm3pgbinder * self.solids_density_gpcm3

        # compute Dphi
        wc = self.wc
        rho_w = self.hydration.chemdat_dict["H"]["density_gpcm3"]
        rho_b = self.blend.density_gpcm3
        DVs = self.DV_s_cm3pgbinder
        DVtot = self.DV_tot_cm3pgbinder
        Dphi_nom = DVs * (1 / rho_b + wc / rho_w) - DVtot / rho_b
        Dphi_denom = (1 / rho_b + wc / rho_w) ** 2 + DVtot * (1 / rho_b + wc / rho_w)
        self.Dphi = Dphi_nom / Dphi_denom


    def plot_ht(self, ax=None, lbl=True, s=0, e=-1, **kwargs):
        """
        plots heat flow [mW/g] vs. time [s]

        Args:
            ax: define custom axis
            lbl: displays axes labels, default is True
            s: start index, default is 0
            e: end index, default is -1
        """

        line = myplot(
            ax=ax,
            x=self.t * self.anlzr.nft,
            y=self.h * self.anlzr.nfh,
            xlbl=rf"time [{self.anlzr.ut}]",
            ylbl=rf"h [{self.anlzr.uh}]",
            lbl=lbl,
            s=s,
            e=e,
            **kwargs,
        )

        return line

    def plot_Ht(self, ax=None, lbl=True, s=0, e=-1, **kwargs):
        """
        plots cumulative heat [J/g binder] vs. time [s]

        Args:
            ax: define custom axis
            lbl: displays axes labels, default is True
            s: start index, default is 0
            e: end index, default is -1
        """

        line = myplot(
            ax=ax,
            x=self.t * self.anlzr.nft,
            y=self.H * self.anlzr.nfH,
            xlbl=rf"time [{self.anlzr.ut}]",
            ylbl=rf"H [{self.anlzr.uH}]",
            lbl=lbl,
            s=s,
            e=e,
            **kwargs,
        )

        return line

    def plot_DHt(self, ax=None, lbl=True, s=0, e=-1, **kwargs):
        """
        plots cumul heat - cumul heat onset [J/g binder] vs. time [s]

        Args:
            ax: define custom axis
            lbl: displays axes labels, default is True
            s: start index, default is 0
            e: end index, default is -1
        """

        line = myplot(
            ax=ax,
            x=self.t * self.anlzr.nft,
            y=self.DH * self.anlzr.nfH,
            xlbl=rf"time [{self.anlzr.ut}]",
            ylbl=rf"$\Delta$H [{self.anlzr.uH}]",
            lbl=lbl,
            s=s,
            e=e,
            **kwargs,
        )

        return line

    def plot_Gt(self, ax=None, lbl=True, s=0, e=-1, **kwargs):
        """
        plots storage modulus [MPa] vs. time [s]

        Args:
            ax: define custom axis
            lbl: displays axes labels, default is True
            s: start index, default is 0
            e: end index, default is -1
        """

        line = myplot(
            ax=ax,
            x=self.t * self.anlzr.nft,
            y=self.G * self.anlzr.nfG,
            xlbl=rf"time [{self.anlzr.ut}]",
            ylbl=rf"G' [{self.anlzr.uG}]",
            lbl=lbl,
            s=s,
            e=e,
            **kwargs,
        )

        return line

    def plot_Gtildet(self, ax=None, lbl=True, **kwargs):
        """
        plots normalized storage modulus [-] vs. time [s]

        Args:
            ax: define custom axis
            lbl: displays axes labels, default is True
            s: start index, default is 0
            e: end index, default is -1
        """

        line = myplot(
            ax=ax,
            x=self.t * self.anlzr.nft,
            y=self.Gtilde,
            xlbl=rf"time [{self.anlzr.ut}]",
            ylbl=r"$\tilde{G}$ [-]",
            lbl=lbl,
            **kwargs,
        )

        return line

    def plot_GDH(self, ax=None, lbl=True, s=0, e=-1, **kwargs):
        """
        plots storage modulus [MPa]
        vs. change in heat [J/g binder]

        Args:
            ax: define custom axis
            lbl: displays axes labels, default is True
            s: start index, default is 0
            e: end index, default is -1
        """

        line = myplot(
            ax=ax,
            x=self.DH * self.anlzr.nfH,
            y=self.G * self.anlzr.nfG,
            xlbl=rf"H-H$_0$ [{self.anlzr.uH}]",
            ylbl=rf"G' [{self.anlzr.uG}]",
            lbl=lbl,
            s=s,
            e=e,
            **kwargs,
        )

        return line

    def plot_GtildeDH(self, ax=None, lbl=True, s=0, e=-1, **kwargs):
        """
        plots normalized storage modulus [-]
        vs. change in heat [J/g binder]

        Args:
            ax: define custom axis
            lbl: displays axes labels, default is True
            s: start index, default is 0
            e: end index, default is -1
        """
        G = "G"
        Gtilde = rf"$\tilde{{{G}}}$"

        line = myplot(
            ax=ax,
            x=self.DH * self.anlzr.nfH,
            y=self.Gtilde,
            xlbl=rf"$\Delta$H [{self.anlzr.uH}]",
            ylbl=rf"{Gtilde} [-]",
            lbl=lbl,
            s=s,
            e=e,
            **kwargs,
        )

        return line

    def plot_GDHperSgrain(self, ax=None, lbl=True, s=0, e=-1, **kwargs):
        """
        plots storage modulus [MPa]
        vs. change in heat per initial grain surface [J/m2]

        Args:
            ax: define custom axis
            lbl: displays axes labels, default is True
            s: start index, default is 0
            e: end index, default is -1
        """

        line = myplot(
            ax=ax,
            x=self.DHperSgrain_Jpm2 * self.anlzr.nfH,
            y=self.G * self.anlzr.nfG,
            xlbl=rf"H-H$_0$ [J/m$^2$]",
            ylbl=rf"G' [{self.anlzr.uG}]",
            lbl=lbl,
            s=s,
            e=e,
            **kwargs,
        )

        return line

    def plot_GtildeDHperSgrain(self, ax=None, lbl=True, s=0, e=-1, **kwargs):
        """
        plots normalized storage modulus [-]
        vs. change in heat per initial grain surface [J/m2]

        Args:
            ax: define custom axis
            lbl: displays axes labels, default is True
            s: start index, default is 0
            e: end index, default is -1
        """
        G = "G"
        Gtilde = rf"$\tilde{{{G}}}$"

        line = myplot(
            ax=ax,
            x=self.DHperSgrain_Jpm2,
            y=self.Gtilde,
            xlbl=rf"$\Delta$H [J/m$^2$]",
            ylbl=rf"{Gtilde} [-]",
            lbl=lbl,
            s=s,
            e=e,
            **kwargs,
        )

        return line

    def plot_GDVproducts(self, ax=None, lbl=True, s=0, e=-1, **kwargs):
        """
        plots storage modulus [MPa]
        vs. change in volume  of products per initial grain surface [cm3/ g binder]

        Args:
            ax: define custom axis
            lbl: displays axes labels, default is True
            s: start index, default is 0
            e: end index, default is -1
        """

        line = myplot(
            ax=ax,
            x=self.DV_products_cm3pgbinder,
            y=self.G * self.anlzr.nfG,
            xlbl=r"V$^{\mathrm{prod}}$-V$_0$$^\mathrm{prod}$ [cm$^3$/g]",
            ylbl=rf"G' [{self.anlzr.uG}]",
            lbl=lbl,
            s=s,
            e=e,
            **kwargs,
        )

        return line

    def plot_GtildeDVproducts(self, ax=None, lbl=True, s=0, e=-1, **kwargs):
        """
        plots normalized storage modulus [-]
        vs. change in volume of products per unit binder [cm3/g binder]

        Args:
            ax: define custom axis
            lbl: displays axes labels, default is True
            s: start index, default is 0
            e: end index, default is -1
        """
        G = "G"
        Gtilde = rf"$\tilde{{{G}}}$"

        line = myplot(
            ax=ax,
            x=self.DV_products_cm3pgbinder,
            y=self.Gtilde,
            xlbl=r"V$^{\mathrm{prod}}$-V$_0$$^\mathrm{prod}$ [cm$^3$/g]",
            ylbl=rf"{Gtilde} [-]",
            lbl=lbl,
            s=s,
            e=e,
            **kwargs,
        )

        return line

    def plot_GDVproductsperSgrain(self, ax=None, lbl=True, s=0, e=-1, **kwargs):
        """
        plots storage modulus [MPa]
        vs. change in volume per initial grain surface [cm3/m2]

        Args:
            ax: define custom axis
            lbl: displays axes labels, default is True
            s: start index, default is 0
            e: end index, default is -1
        """

        line = myplot(
            ax=ax,
            x=self.DVproductsperSgrain_cm3pm2,
            y=self.G * self.anlzr.nfG,
            xlbl=r"(V$^{\mathrm{prod}}$-V$_0$$^\mathrm{prod}$) / S$_{\mathrm{grain}}$ [cm$^3$/m$^2$]",
            ylbl=rf"G' [{self.anlzr.uG}]",
            lbl=lbl,
            s=s,
            e=e,
            **kwargs,
        )

        return line

    def plot_GtildeDVproductsperSgrain(self, ax=None, lbl=True, s=0, e=-1, **kwargs):
        """
        plots normalized storage modulus [-]
        vs. change in volume of products per initial grain surface [cm3/m2]

        Args:
            ax: define custom axis
            lbl: displays axes labels, default is True
            s: start index, default is 0
            e: end index, default is -1
        """
        G = "G"
        Gtilde = rf"$\tilde{{{G}}}$"

        line = myplot(
            ax=ax,
            x=self.DVproductsperSgrain_cm3pm2,
            y=self.Gtilde,
            xlbl=r"(V$^{\mathrm{prod}}$-V$_0$$^\mathrm{prod}$) / S$_{\mathrm{grain}}$ [cm$^3$/m$^2$]",
            ylbl=rf"{Gtilde} [-]",
            lbl=lbl,
            s=s,
            e=e,
            **kwargs,
        )

        return line

    def plot_GDVproductsperVgrain(self, ax=None, lbl=True, s=0, e=-1, **kwargs):
        """
        plots storage modulus [MPa]
        vs. change in volume per initial grain volume

        Args:
            ax: define custom axis
            lbl: displays axes labels, default is True
            s: start index, default is 0
            e: end index, default is -1
        """

        line = myplot(
            ax=ax,
            x=self.DVproductsperVgrain,
            y=self.G * self.anlzr.nfG,
            xlbl=r"(V$^{\mathrm{prod}}$-V$_0$$^\mathrm{prod}$) / V$_{\mathrm{grain}}$ [-]",
            ylbl=rf"G' [{self.anlzr.uG}]",
            lbl=lbl,
            s=s,
            e=e,
            **kwargs,
        )

        return line

    def plot_GtildeDVproductsperVgrain(self, ax=None, lbl=True, s=0, e=-1, **kwargs):
        """
        plots normalized storage modulus [-]
        vs. change in volume of products per initial grain volume

        Args:
            ax: define custom axis
            lbl: displays axes labels, default is True
            s: start index, default is 0
            e: end index, default is -1
        """

        G = "G"
        Gtilde = rf"$\tilde{{{G}}}$"

        line = myplot(
            ax=ax,
            x=self.DVproductsperVgrain,
            y=self.Gtilde,
            xlbl=r"(V$^{\mathrm{prod}}$-V$_0$$^\mathrm{prod}$) / V$_{\mathrm{grain}}$ [-]",
            ylbl=rf"{Gtilde} [-]",
            lbl=lbl,
            s=s,
            e=e,
            **kwargs,
        )

        return line

    def get_fit_params(self, fit, x="DH", y="G", xx0_bound=0, period=None):
        """
        Fit parameters for specified x and y data using a given fitting function.

        This method retrieves x and y values based on the specified keys,
        finds the nearest index for a given boundary, and performs curve fitting
        using the provided fitting function. The fitting can be performed on
        different segments of the data based on the specified period.
        induction = up to the boundary
        acceleration = from the boundary onwards

        Parameters:
            fit : callable
                The fitting function to use for curve fitting. It should take
                x values as the first argument and any additional parameters
                as subsequent arguments.

            x : str, optional
                The key for the x values to be used for fitting.
                Default is "DH". Options include:
                - "DH"
                - "DHperSgrain"
                - "G"
                - "Gtilde"
                - "DV"
                - "DVproductsperSgrain"

            y : str, optional
                The key for the y values to be used for fitting.
                Default is "G". Options are similar to x.

            xx0_bound : float, optional
                The boundary value for segmenting the data. The nearest index
                to this value will be found in the x values. Default is 0.

            period : str or None, optional
                Specifies the segment of the data to fit:
                - None: Fit on the entire dataset.
                - "induct": Fit on the data up to the boundary.
                - "accel": Fit on the data after the boundary.

        Returns:
            np.ndarray
                The optimal parameters for the fit obtained from the curve fitting.

        Raises:
            ValueError: If the specified x or y keys do not exist in the conversion_dict.
        """

        conversion_dict = {
            "DH": self.DH,
            "DHperSgrain": self.DHperSgrain_Jpm2,
            "G": self.G,
            "Gtilde": self.Gtilde,
            "DV": self.DV_s_products_cm3pgbinder,
            "DVproductsperSgrain": self.DVproductsperSgrain_cm3pm2,
        }

        x_values = conversion_dict.get(x, None)
        y_values = conversion_dict.get(y, None)

        idx_bound = self.find_nearest(array=x_values, value=xx0_bound)

        if period == "induct":
            x_fit = x_values[:idx_bound]
            y_fit = y_values[:idx_bound]
        elif period == "accel":
            x_fit = x_values[idx_bound:]
            y_fit = y_values[idx_bound:]
        else:  # period is None or any other value
            x_fit = x_values
            y_fit = y_values

        p, _ = curve_fit(fit, x_fit, y_fit)

        return p

    def plot_Dphi_t(self, ax=None, lbl=True, s=0, e=-1, **kwargs):
        """
        plots change in solid volme fraction over time

        Args:
            ax: define custom axis
            lbl: displays axes labels, default is True
            s: start index, default is 0
            e: end index, default is -1
        """

        line = myplot(
            ax=ax,
            x=self.t * self.anlzr.nft,
            y=self.Dphi,
            xlbl=rf"time [{self.anlzr.ut}]",
            ylbl=r"$\Delta \phi$ [-]",
            lbl=lbl,
            s=s,
            e=e,
            **kwargs,
        )

        return line

    def plot_Dphi_DH(self, ax=None, lbl=True, s=0, e=-1, **kwargs):
        """
        plots change in solid volme fraction against
        changes in cumulative heat

        Args:
            ax: define custom axis
            lbl: displays axes labels, default is True
            s: start index, default is 0
            e: end index, default is -1
        """

        line = myplot(
            ax=ax,
            x=self.DH * self.anlzr.nfH,
            y=self.Dphi,
            xlbl=rf"$\Delta$H [{self.anlzr.uH}]",
            ylbl=r"$\Delta \phi$ [-]",
            lbl=lbl,
            s=s,
            e=e,
            **kwargs,
        )

        return line

    def draw_onset(
        self,
        ax_ht,
        ax_HH0t,
        ax_Gt,
        cross_color="k",
        cross_fntsz=5,
        cross_alpha=0.7,
        line_color="0.3",
        line_style="-",
        line_width=0.4,
        line_alpha=0.4,
        line_prolong=1,
    ):

        # add cross at onset in h-t
        ax_ht.text(
            self.t[self.onset_idx] * self.anlzr.nft,
            self.h[self.onset_idx] * self.anlzr.nfh,
            "x",
            color=cross_color,
            alpha=cross_alpha,
            fontsize=cross_fntsz,
            horizontalalignment="center",
            verticalalignment="center",
        )

        ax_HH0t.text(
            self.t[self.onset_idx] * self.anlzr.nft,
            self.DH[self.onset_idx],
            "x",
            color=cross_color,
            alpha=cross_alpha,
            fontsize=cross_fntsz,
            horizontalalignment="center",
            verticalalignment="center",
        )

        ax_Gt.text(
            self.t[self.onset_idx] * self.anlzr.nft,
            self.G[self.onset_idx] * self.anlzr.nfG,
            "x",
            color=cross_color,
            alpha=cross_alpha,
            fontsize=cross_fntsz,
            horizontalalignment="center",
            verticalalignment="center",
        )

        #### vlines through time evolutions
        xy_ht = (
            self.t[self.onset_idx] * self.anlzr.nft,
            self.h[self.onset_idx] * self.anlzr.nfh,
        )
        xy_Gt = (
            self.t[self.onset_idx] * self.anlzr.nft,
            self.G[self.onset_idx] * self.anlzr.nfG,
        )
        con = ConnectionPatch(
            xyA=xy_ht,
            xyB=xy_Gt,
            coordsA="data",
            coordsB="data",
            axesA=ax_ht,
            axesB=ax_Gt,
            color=line_color,
            lw=line_width,
            linestyle=line_style,
            alpha=line_alpha,
        )
        ax_Gt.add_artist(con)

        #### longer lines for "onset" text
        xy_ht_1 = (
            self.t[self.onset_idx] * self.anlzr.nft,
            self.h[self.onset_idx] * self.anlzr.nfh,
        )
        xy_ht_2 = (self.t[self.onset_idx] * self.anlzr.nft, line_prolong)
        bmp = ConnectionPatch(
            xyA=xy_ht_1,
            xyB=xy_ht_2,
            coordsA="data",
            coordsB="data",
            axesA=ax_ht,
            axesB=ax_ht,
            color=line_color,
            lw=line_width,
            linestyle=line_style,
            alpha=line_alpha,
        )
        ax_ht.add_artist(bmp)

    def text_onset_H0_G0(
        self,
        ax_ht,
        ax_HH0t,
        ax_Gt,
        text_color="k",
        text_fontsize=6,
        text_alpha=0.8,
        onset_xy=[2.1, 1],
        H0_xy=[2.1, 1],
        G0_xy=[2.1, 1],
    ):

        ## onset, H0 and G0 texts
        ax_ht.text(
            onset_xy[0],
            onset_xy[1],
            "onset",
            color=text_color,
            fontsize=text_fontsize,
            alpha=text_alpha,
        )

        ax_HH0t.text(
            H0_xy[0],
            H0_xy[1],
            r"H$_{\mathrm{0}}$",
            color=text_color,
            fontsize=text_fontsize,
            alpha=text_alpha,
        )

        ax_Gt.text(
            G0_xy[0],
            G0_xy[1],
            r"G$_{\mathrm{0}}'$",
            color=text_color,
            fontsize=text_fontsize,
            alpha=text_alpha,
        )
