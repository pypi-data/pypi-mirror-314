from buildupp.configuration import Config

class Compound:
    """
    Compound is a compound of a chemical reaction.
    Allows to access data in the chemistry database (ini format).

    The database format is as follows:
    [compound_name]
    molar_mass_gpmol = value
    density_gpcm3 = value
    formation_enthalpy_Jpmol = value
    ref = source

    Example INI structure:
    [CH]
    molar_mass_gpmol = 74
    density_gpcm3 = 2.24
    formation_enthalpy_Jpmol = -985000
    ref = matschei_ccr_2007

    The database can be accessed using self.chemdat_dict.
    Example: self.chemdat_dict['CH']['density_gpcm3']
    """

    def __init__(self, config: Config = Config()) -> None:

        self.chemdat_dict = config.chemdat_dict

    def formation_enthalpy_Jpmol(self, compound):
        """Get the formation enthalpy of the compound (in J/mol)."""
        return self.chemdat_dict[compound]['formation_enthalpy_jpmol']

    def molar_mass_gpmol(self, compound):
        """Get the molar mass of the compound (in g/mol)."""
        return self.chemdat_dict[compound]['molar_mass_gpmol']

    def density_gpcm3(self, compound):
        """Get the density of the compound (in g/cm³)."""
        return self.chemdat_dict[compound]['density_gpcm3']


class Hydration(Compound):
    """
    Hydration reaction is based on a dictionary containing
    the chemical equation with the stoichiometric coefficients
    and on a INI file containing the enthalpies of formation of the
    reactants and products.

    Args:
      - chem_reaction: dict

        example dict for C3S hydration:

        C3S_hydration = {'reactants':{'solids':{'C3S':1},
                                    'liquids':{'H':3.43}},
                        'products':{'solids':{'C1.67SH2.1':1, 'CH':1.33},
                                    'liquids':{}}}

      - db: ini file containing the enthalpies of formation
        For the format of the ini file, see class Compound
    """

    def __init__(self, chem_reaction: dict, config: Config = Config()) -> None:
        super().__init__(config=config)


        self.chemical_reaction = chem_reaction

        ## returns dict, e.g. {'C3S':1}
        self.reactants_solid = chem_reaction["reactants"]["solids"]
        self.reactants_liquid = chem_reaction["reactants"]["liquids"]
        self.products_solid = chem_reaction["products"]["solids"]
        self.products_liquid = chem_reaction["products"]["liquids"]

        self.DH0reaction_Jpmol = self.compute_DH0reaction_Jpmol()

        self.mtotchange_gpmol = self.compute_mtotchange_gpmol()
        self.mschange_gpmol = self.compute_mschange_gpmol()
        self.mlchange_gpmol = self.compute_mlchange_gpmol()
        self.mschange_products_gpmol = self.compute_mschange_products_gpmol()

        self.Vtot_change_cm3pmol = self.compute_Vtot_change_cm3pmol()
        self.Vs_change_cm3pmol = self.compute_Vs_change_cm3pmol()
        self.Vl_change_cm3pmol = self.compute_Vl_change_cm3pmol()
        self.Vs_change_products_cm3pmol = self.compute_Vs_change_products_cm3pmol()

        self.mu_tot_gpJ = self.compute_mu_tot_gpJ()
        self.mu_s_gpJ = self.compute_mu_s_gpJ()
        self.mu_l_gpJ = self.compute_mu_l_gpJ()
        self.mu_s_products_gpJ = self.compute_mu_s_products_gpJ()

        self.nu_tot_cm3pJ = self.compute_nu_tot_cm3pJ()
        self.nu_s_cm3pJ = self.compute_nu_s_cm3pJ()
        self.nu_l_cm3pJ = self.compute_nu_l_cm3pJ()
        self.nu_s_products_cm3pJ = self.compute_nu_s_products_cm3pJ()

    def compute_DH0reaction_Jpmol(self):
        """Compute the enthalpy of reaction Delta H^0_{reaction} from Hess's law

        Computes the heat generated (sign depends if endo- or exothremic)
        by the reaction for the formation of 1 mol of product.

        For the default C3S hydration, it computes it for the
        formation of 1 mol of C-S-H.
        """

        # DH_reaction = SUM(n_prod DH_prod) - SUM(n_reactants DH_reactants)
        DH_reaction = 0

        # products_solid[compound] gives the number of moles of compound in the products that are solids
        for compound in self.products_solid:
            DH_reaction += self.products_solid[
                compound
            ] * self.formation_enthalpy_Jpmol(compound)
        for compound in self.products_liquid:
            DH_reaction += self.products_liquid[
                compound
            ] * self.formation_enthalpy_Jpmol(compound)
        for compound in self.reactants_solid:
            DH_reaction -= self.reactants_solid[
                compound
            ] * self.formation_enthalpy_Jpmol(compound)
        for compound in self.reactants_liquid:
            DH_reaction -= self.reactants_liquid[
                compound
            ] * self.formation_enthalpy_Jpmol(compound)

        return DH_reaction

    def compute_mtotchange_gpmol(self):
            """Compute the total mass change for 1 mol of product.

            For the default C3S hydration, it computes it for the
            formation of 1 mol of C-S-H.
            """

            mtot_change = 0

            for compound in self.products_solid:
                mtot_change += self.products_solid[compound] * self.molar_mass_gpmol(compound)
            
            for compound in self.products_liquid:
                mtot_change += self.products_liquid[compound] * self.molar_mass_gpmol(compound)

            for compound in self.reactants_solid:
                mtot_change -= self.reactants_solid[compound] * self.molar_mass_gpmol(
                    compound
                )

            for compound in self.reactants_liquid:
                mtot_change -= self.reactants_liquid[compound] * self.molar_mass_gpmol(
                    compound
                )

            return mtot_change
    
    def compute_mschange_gpmol(self):
        """Compute the mass change of solids for 1 mol of product.

        For the default C3S hydration, it computes it for the
        formation of 1 mol of C-S-H.
        """

        ms_change = 0

        for compound in self.products_solid:
            ms_change += self.products_solid[compound] * self.molar_mass_gpmol(compound)
        for compound in self.reactants_solid:
            ms_change -= self.reactants_solid[compound] * self.molar_mass_gpmol(
                compound
            )

        return ms_change
    
    def compute_mlchange_gpmol(self):
        """Compute the mass change of liquids for 1 mol of product.

        For the default C3S hydration, it computes it for the
        formation of 1 mol of C-S-H.
        """

        ml_change = 0

        for compound in self.products_liquid:
            ml_change += self.products_liquid[compound] * self.molar_mass_gpmol(compound)
        for compound in self.reactants_liquid:
            ml_change -= self.reactants_liquid[compound] * self.molar_mass_gpmol(
                compound
            )

        return ml_change
    
    def compute_mschange_products_gpmol(self):
        """Compute the mass change of products for 1 mol of product.

        For the default C3S hydration, it computes it for the
        formation of 1 mol of C-S-H.
        """

        ms_change_products = 0

        for compound in self.products_liquid:
            ms_change_products += self.products_solid[compound] * self.molar_mass_gpmol(compound)

        return ms_change_products

    def compute_mu_tot_gpJ(self):
        """Compute mu_s, giving the total mass change of solids
        (in g) for 1 joule of reaction.
        """

        mu_tot = self.mtotchange_gpmol / abs(self.DH0reaction_Jpmol)
        return mu_tot
    
    def compute_mu_s_gpJ(self):
        """Compute mu_s, giving the total mass change of solids
        (in g) for 1 joule of reaction.
        """

        mu_s = self.mschange_gpmol / abs(self.DH0reaction_Jpmol)
        return mu_s
    
    def compute_mu_l_gpJ(self):
        """Compute mu_l, giving the mass change of liquids
        (in g) for 1 joule of reaction.
        """

        mu_l = self.mlchange_gpmol / abs(self.DH0reaction_Jpmol)
        return mu_l
    
    def compute_mu_s_products_gpJ(self):
        """Compute mu_s_products, giving the mass change of solid products
        (in g) for 1 joule of reaction.
        """

        mu_s_products = self.mschange_gpmol / abs(self.DH0reaction_Jpmol)
        return mu_s_products
    
    def compute_Vtot_change_cm3pmol(self):
        """Compute the change in total volume
        (in cm3) for 1 mol of product.

        For the default C3S hydration, it computes it for the
        formation of 1 mol of C-S-H.
        """
        Vtot_change = 0

        for compound in self.products_solid:
            Vtot_change += (
                self.products_solid[compound]
                * self.molar_mass_gpmol(compound)
                / self.density_gpcm3(compound)
            )
        
        for compound in self.products_liquid:
            Vtot_change += (
                self.products_liquid[compound]
                * self.molar_mass_gpmol(compound)
                / self.density_gpcm3(compound)
            )

        for compound in self.reactants_solid:
            Vtot_change -= (
                self.reactants_solid[compound]
                * self.molar_mass_gpmol(compound)
                / self.density_gpcm3(compound)
            )

        for compound in self.reactants_liquid:
            Vtot_change -= (
                self.reactants_liquid[compound]
                * self.molar_mass_gpmol(compound)
                / self.density_gpcm3(compound)
            )

        return Vtot_change

    def compute_Vs_change_cm3pmol(self):
        """Compute the total change in volume of solids
        (in cm3) for 1 mol of product.

        For the default C3S hydration, it computes it for the
        formation of 1 mol of C-S-H.
        """
        Vs_change = 0

        for compound in self.products_solid:
            Vs_change += (
                self.products_solid[compound]
                * self.molar_mass_gpmol(compound)
                / self.density_gpcm3(compound)
            )

        for compound in self.reactants_solid:
            Vs_change -= (
                self.reactants_solid[compound]
                * self.molar_mass_gpmol(compound)
                / self.density_gpcm3(compound)
            )

        return Vs_change
    
    def compute_Vl_change_cm3pmol(self):
        """Compute the total change in volume of liquids
        (in cm3) for 1 mol of product.

        For the default C3S hydration, it computes it for the
        formation of 1 mol of C-S-H.
        """
        Vl_change = 0

        for compound in self.products_liquid:
            Vl_change += (
                self.products_liquid[compound]
                * self.molar_mass_gpmol(compound)
                / self.density_gpcm3(compound)
            )

        for compound in self.reactants_liquid:
            Vl_change -= (
                self.reactants_liquid[compound]
                * self.molar_mass_gpmol(compound)
                / self.density_gpcm3(compound)
            )

        return Vl_change

    def compute_Vs_change_products_cm3pmol(self):
        """Compute the change in volume of solid products (in cm3)
        for 1 mol of product.

        For the default C3S hydration, it computes it for the
        formation of 1 mol of C-S-H.
        """
        Vs_change_products = 0

        for compound in self.products_solid:
            Vs_change_products += (
                self.products_solid[compound]
                * self.molar_mass_gpmol(compound)
                / self.density_gpcm3(compound)
            )

        return Vs_change_products

    def compute_nu_tot_cm3pJ(self):
        """Compute nu, giving the total volume change (in cm3)
        for 1 joule of reaction.
        """

        nu_tot = self.Vtot_change_cm3pmol / abs(self.DH0reaction_Jpmol)
        return nu_tot
    
    def compute_nu_s_cm3pJ(self):
        """Compute nu, giving the volume change of all solids (in cm3)
        for 1 joule of reaction.
        """

        nu_s = self.Vs_change_cm3pmol / abs(self.DH0reaction_Jpmol)
        return nu_s
    
    def compute_nu_l_cm3pJ(self):
        """Compute nu, giving the volume change of liquids (in cm3)
        for 1 joule of reaction.
        """

        nu_l = self.Vl_change_cm3pmol / abs(self.DH0reaction_Jpmol)
        return nu_l
    
    def compute_nu_s_products_cm3pJ(self):
        """Compute nu_s_products, giving the volume change of solid
        products (in cm3) for 1 joule of reaction.
        """

        nu_s_products = self.compute_Vs_change_products_cm3pmol() / abs(self.DH0reaction_Jpmol)
        return nu_s_products
