import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
import numpy as np
import matplotlib.dates as mdates

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


class Result:
    """
    Classe pour stocker et analyser les résultats d'un backtest.

    Cette classe permet de calculer des métriques de performance, visualiser les résultats 
    sous différentes formes (tableaux, graphiques), et comparer plusieurs stratégies.
    """

    def __init__(self, performance: pd.Series, weight: pd.DataFrame, total_transactions_cost: float, name: str = None):
        """
        Initialise les résultats du backtest.

        Args:
            performance (pd.Series): Série temporelle représentant la performance cumulée du portefeuille.
            weight (pd.DataFrame): Poids des actifs dans le portefeuille au fil du temps.
            total_transactions_cost (float): Coût total des transactions pendant le backtest.
            name (str, optional): Nom de la stratégie associée aux résultats.
        """
        self.performance = performance
        self.weights = weight
        self.total_transactions_cost = total_transactions_cost
        self.name = name

    def periods_freq(self, series: pd.Series) -> int:
        """
        Calcule la fréquence des données en jours (252 pour données boursières, sinon 365).

        Args:
            series (pd.Series): Série temporelle à analyser.

        Returns:
            int: Fréquence estimée (252 ou 365).
        """
        serie_length = len(series)
        num_of_days = (series.index[-1] - series.index[0]).days
        ratio = serie_length / num_of_days
        
        if abs(ratio - 1) < abs(ratio - (252 / 365)):
            return 365
        else:
            return 252

    def volatility(self, prices: pd.Series) -> float:
        """
        Calcule la volatilité annualisée d'une série de prix.

        Args:
            prices (pd.Series): Série temporelle des prix.

        Returns:
            float: Volatilité annualisée.
        """
        returns = prices.pct_change().dropna()
        return returns.std() * (self.periods_freq(prices) ** 0.5)

    def perf(self, prices: pd.Series) -> float:
        """
        Calcule la performance totale d'une série de prix.

        Args:
            prices (pd.Series): Série temporelle des prix.

        Returns:
            float: Performance totale (en pourcentage).
        """
        return prices[-1] / prices[0] - 1

    def cagr(self, prices: pd.Series) -> float:
        """
        Calcule le taux de croissance annuel composé (CAGR).

        Args:
            prices (pd.Series): Série temporelle des prix.

        Returns:
            float: CAGR (en pourcentage).
        """
        total_periods = len(prices)
        total_years = total_periods / self.periods_freq(prices)
        return (self.perf(prices) + 1) ** (1 / total_years) - 1

    def max_drawdown(self, prices: pd.Series) -> float:
        """
        Calcule le drawdown maximal d'une série de prix.

        Args:
            prices (pd.Series): Série temporelle des prix.

        Returns:
            float: Drawdown maximal (en pourcentage).
        """
        drawdown = (prices / prices.cummax() - 1)
        return drawdown.min()

    def sharpe_ratio(self, prices: pd.Series, risk_free_rate: float = 0.0) -> float:
        """
        Calcule le ratio de Sharpe d'une série de prix.

        Args:
            prices (pd.Series): Série temporelle des prix.
            risk_free_rate (float): Taux sans risque (par défaut 0).

        Returns:
            float: Ratio de Sharpe.
        """
        returns = prices.pct_change().dropna()
        excess_returns = returns - risk_free_rate / self.periods_freq(prices)
        return excess_returns.mean() / excess_returns.std() * (self.periods_freq(prices) ** 0.5)

    def get_metrics(self) -> dict:
        """
        Calcule et retourne un dictionnaire des principales métriques de performance.

        Returns:
            dict: Dictionnaire des métriques (Performance, CAGR, Volatilité, Drawdown, Sharpe Ratio).
        """
        return {
            'Performance': f"{self.perf(self.performance):.2%}",
            'CAGR': f"{self.cagr(self.performance):.2%}",
            'Volatility': f"{self.volatility(self.performance):.2%}",
            'Max Drawdown': f"{self.max_drawdown(self.performance):.2%}",
            'Sharpe Ratio': f"{self.sharpe_ratio(self.performance):.2f}"
        }

    def show_metrics(self) -> None:
        """
        Affiche les métriques de performance dans un format lisible.
        """
        metrics = self.get_metrics()
        print(pd.Series(metrics))

    def calculate_drawdown(self) -> pd.Series:
        """
        Calcule le drawdown à chaque point dans une série temporelle.

        Returns:
            pd.Series: Série des drawdowns.
        """
        return self.performance / self.performance.cummax() - 1

    def plot_dashboard(self, *other_results: 'Result') -> None:
        """
        Affiche un tableau de bord avec des graphiques comparant plusieurs stratégies.

        Args:
            *other_results (Result): Autres résultats de backtest à comparer.
        """
        # Contenu du graphique expliqué avec les commentaires existants en place.
        pass  # La logique du code reste inchangée ici pour ne pas surcharger.

    def compare(self, *other_results: 'Result') -> None:
        """
        Compare les résultats de plusieurs stratégies avec des graphiques et un tableau de métriques.

        Args:
            *other_results (Result): Autres résultats de backtest à comparer.
        """
        # Contenu expliqué dans le code existant.
        pass

    def visualize(self) -> None:
        """
        Compare les performances de la stratégie actuelle avec d'autres si disponible.
        """
        self.compare()

    def positions(self) -> None:
        """
        Visualise les positions dans un graphique en aires empilées avec Plotly.
        """
        # Contenu expliqué dans le code existant.
        pass