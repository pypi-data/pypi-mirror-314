from abc import ABC, abstractmethod
from enum import Enum

import datetime

from .constants import OPCENTEN, OPCENTEN_BRACKETS, EXCESS_RATES, KWARTTARIEF_MAX


class EnergySource(Enum):
    BENZINE = "benzine"
    DIESEL = "diesel"
    LPG = "overige"
    LPG_G3 = "lpg_g3"
    ELEKTRICITEIT = "elektriciteit"
    OVERIGE = "overige"


class Vehicle(ABC):
    """
    Abstract base class representing a generic vehicle.

    Attributes:
        rounded_weight (int): The weight of the vehicle, rounded down to the nearest hundred kilograms.
        energy_source (EnergySource): The type of energy source used by the vehicle (e.g., benzine, diesel, electric).
        manufacturing_year (int, optional): The year the vehicle was manufactured. Defaults to None.

    Args:
        weight (int): The weight of the vehicle in kilograms.
        energy_source (EnergySource): An instance of the `EnergySource` enum representing the vehicle's fuel type.
        manufacturing_year (int, optional): The year the vehicle was manufactured. Defaults to None.
    """

    def __init__(
        self, weight: int, energy_source: EnergySource, manufacturing_year: int = None
    ):
        self.rounded_weight = 100 * int(weight / 100)
        self.energy_source = energy_source
        self.manufacturing_year = manufacturing_year
        self.calculation_year = None

    def set_calculation_year(self, year: int):
        self.calculation_year = year

    @abstractmethod
    def calculate_base_tax(self) -> float:
        """Abstract method to calculate base tax."""
        return

    @abstractmethod
    def calculate_total_tax(self, year: int, province: str) -> float:
        """Abstract method to calculate the total tax, optionally using province."""
        return

    def is_historic(self) -> bool:
        """Oldtimer ruling applies when vehicle is registered 40 years ago"""
        oldtimer_deadline = datetime.date.today().year - 40
        if self.manufacturing_year:
            return self.manufacturing_year <= oldtimer_deadline
        return False

    def apply_historic_tax_discount(self, tax: float) -> float:
        return 0 if self.is_historic() else tax

    def is_kwarttarief(self) -> bool:
        """kwarttarief ruling applies when a vehicle is registered before 1988 up until it is 40 years old"""
        if self.manufacturing_year:
            return self.manufacturing_year < 1988
        return False

    def apply_kwarttarief_discount(self, tax: float) -> float:
        if self.is_kwarttarief() and self.energy_source == EnergySource.BENZINE:
            return min(tax * 0.25, KWARTTARIEF_MAX[self.calculation_year])
        return tax

    def is_electric(self) -> bool:
        return self.energy_source == EnergySource.ELEKTRICITEIT

    def apply_electric_tax_discount(self, tax: float) -> float:
        if self.is_electric():
            if self.calculation_year < 2025:
                return 0  # No tax for electric cars before 2025
            if self.calculation_year == 2025:
                tax *= 0.25  # 25% of base tax
            elif 2026 <= self.calculation_year <= 2029:
                tax *= 0.75  # 75% of base tax

        return tax

    def apply_low_emission_tax_discount(self, tax: float, low_emission: bool) -> float:
        if low_emission:
            if self.calculation_year < 2025:
                return tax * 0.5 
            elif self.calculation_year == 2025:
                return tax * 0.75
            else:
                return tax
        return tax

    def calculate_multiplier(self, cut_off: int = 900, step: int = 100) -> int:
        """Calculate the added tax based on weight of vehicle

        Args:
            weight (int): Rounded weight of vehicle
            cut_off (int, optional): amount of weight from where to start counting. Defaults to 900.
            step (int, optional): Steps to divide by. Defaults to 100.

        Returns:
            int: Amount of times the extra tax will be added
        """
        if self.rounded_weight > cut_off:
            return round((self.rounded_weight - cut_off) // step)
        return 0

    def calculate_opcenten(self, province: str, year: int) -> float:
        """Calculate the provincional added taxes

        Args:
            weight (int): Rounded weight of vehicle
            province (str): Name of the province
            year (int): Year of calculation

        Returns:
            float: Amount of tax added
        """
        opcenten_brackets = OPCENTEN_BRACKETS
        excess_rate = EXCESS_RATES["opcenten"]
        cutoff = 900
        base_rate = 0

        # Apply excess rate for weights above the cutoff
        if self.rounded_weight >= cutoff:
            multiplier = self.calculate_multiplier(cutoff) - 1
            rate = opcenten_brackets[-1][1]  # Use the last bracket's rate as the base
            base_rate = rate + (multiplier * excess_rate)
        else:
            for max_weight, rate in opcenten_brackets:
                if self.rounded_weight <= max_weight:
                    base_rate = rate
                    break

        return base_rate * (OPCENTEN[province][year] / 100)
