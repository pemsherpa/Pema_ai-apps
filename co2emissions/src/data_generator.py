import numpy as np
import pandas as pd
from scipy.optimize import fsolve


target_emissions_statistics = {
    'total_scope1': {
        'num_observations': 13956,
        'mean': 3.37,
        'median': 0.08,
        'std_deviation': 13.59,
        'jqbera_p_value': 0.001
    },
    'total_scope2': {
        'num_observations': 13956,
        'mean': 0.79,
        'median': 0.14,
        'std_deviation': 3.42,
        'jqbera_p_value': 0.001
    },
    'total_scope3': {
        'num_observations': 8260,
        'mean': 13.33,
        'median': 0.05,
        'std_deviation': 65.60,
        'jqbera_p_value': 0.001
    },
    'total_emissions': {
        'num_observations': 13956,
        'mean': 4.16,
        'median': 0.30,
        'std_deviation': 14.88,
        'jqbera_p_value': 0.001
    }
}

target_feature_statistics = {
    'revenue': {
        'num_observations': 13956,
        'mean': 16988.08,
        'median': 5891.07,
        'std_deviation': 34207.83,
        'jqbera_p_value': 0.001
    },
    'employees': {
        'num_observations': 13956,
        'mean': 42745.57,
        'median': 16702,
        'std_deviation': 83232,
        'jqbera_p_value': 0.001
    },
    'total_assets': {
        'num_observations': 13956,
        'mean': 47182.20,
        'median': 10390.12,
        'std_deviation': 111607.80,
        'jqbera_p_value': 0.001
    },
    'net_property': {
        'num_observations': 13956,
        'mean': 7213.24,
        'median': 1806,
        'std_deviation': 17946.58,
        'jqbera_p_value': 0.001
    },
    'intangible_assets': {
        'num_observations': 13956,
        'mean': 2635.44,
        'median': 401.07,
        'std_deviation': 7623.83,
        'jqbera_p_value': 0.001
    },
    'leverage': {
        'num_observations': 13956,
        'mean': 20.84,
        'median': 18.07,
        'std_deviation': 19.32,
        'jqbera_p_value': 0.001
    },
    'capital_expenditure': {
        'num_observations': 13956,
        'mean': 64.22,
        'median': 27.20,
        'std_deviation': 153.47,
        'jqbera_p_value': 0.001
    },
    'gross_margin': {
        'num_observations': 13956,
        'mean': 49.90,
        'median': 43.69,
        'std_deviation': 29.49,
        'jqbera_p_value': 0.001
    },
    'fuel_intensity': {
        'num_observations': 13956,
        'mean': 429.18,
        'median': 456,
        'std_deviation': 223.45,
        'jqbera_p_value': 0.020
    }
}


class DataStatistics:
    """ Manage statistics for target variables and features."""
    def __init__(self, target_emissions=target_emissions_statistics, target_features=target_feature_statistics):
        self.target_emissions = target_emissions
        self.target_features = target_features

    def get_feature_keys(self):
        return list(self.target_features.keys())


class DistributionGenerator:
    """ Generate distributions based on predefined statistics."""
    @staticmethod
    def solve_lognormal_params(mean, std_dev):
        """ Calculate mu and sigma for a log-normal distribution. """
        def equations(p):
            mu, sigma = p
            mean_eq = np.exp(mu + sigma**2 / 2) - mean
            std_eq = np.sqrt((np.exp(sigma**2) - 1) * np.exp(2 * mu + sigma**2)) - std_dev
            return (mean_eq, std_eq)
        return fsolve(equations, (np.log(mean), 1))

    @staticmethod
    def generate_distribution(stats, n):
        """ Generate distribution data based on given statistics. """
        mean = stats['mean']
        std_deviation = stats['std_deviation']
        median = stats['median']
        
        if abs(mean - median) > mean * 0.1:  # If mean and median difference is large, use log-normal
            mu, sigma = DistributionGenerator.solve_lognormal_params(mean, std_deviation)
            data = np.random.lognormal(mean=mu, sigma=sigma, size=n)
        else:
            data = np.random.normal(loc=mean, scale=std_deviation, size=n)
        return data


class DataGenerator:
    """ Generate synthetic data for emissions and features."""
    def __init__(self, stats):
        self.stats = stats

    def generate_feature_vars(self, n=1):
        """ Generate a DataFrame for all provided features and their statistics. """
        df = pd.DataFrame()
        for feature, stats in self.stats.target_features.items():
            df[feature] = DistributionGenerator.generate_distribution(stats, n)
        # df.to_csv('synthetic_features.csv')
        return df

    def generate_target_vars(self, num_years=6, num_companies=100, seed=42):
        np.random.seed(seed)
        years = np.tile(np.arange(2023 - num_years, 2023), num_companies)
        company_ids = np.repeat(np.arange(num_companies), num_years)
        data = {
            'company_id': company_ids,
            'year': years,
            'stationary_combustion': np.random.normal(120, 20, num_years * num_companies),
            'mobile_sources': np.random.normal(80, 10, num_years * num_companies),
            'refrigeration': np.random.normal(30, 6, num_years * num_companies),
            'fire_suppression': np.random.normal(20, 4, num_years * num_companies),
            'purchased_gases': np.random.normal(40, 8, num_years * num_companies),
            'electricity': np.random.normal(500, 200, num_years * num_companies),
            'steam': np.random.normal(200, 100, num_years * num_companies),
            'waste': np.random.normal(60, 12, num_years * num_companies),
            'business_travel': np.random.normal(80, 16, num_years * num_companies),
            'commuting': np.random.normal(70, 14, num_years * num_companies),
            'upstream_distribution': np.random.normal(90, 18, num_years * num_companies)
        }
        df = pd.DataFrame(data)
        # df.to_csv('synthetic_target.csv')
        return df

    def generate_example_data(self, num_years=6, num_companies=100, seed=42):
        target_df = self.generate_target_vars(num_years, num_companies, seed)
        features_df = self.generate_feature_vars(num_years * num_companies)
        combined_df = pd.concat([target_df, features_df], axis=1)
        return combined_df
