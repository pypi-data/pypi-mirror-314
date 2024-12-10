import numpy as np
import pandas as pd
from .fast_transformers import calculate_log_returns, calculate_returns


class PortfolioSimulator ():
    """
    A class to simulate and manage a portfolio of financial assets based on 
    target weight allocations and trading signals.

    Attributes:
    -----------
    initial_cash : float
        The initial amount of cash available for investment.
    liquid_money : float
        Current available cash after accounting for trades.
    portfolio_value : float
        Total value of the portfolio including cash and assets.
    positions : dict
        A dictionary holding details of current asset positions (allocation and amount).
    target_weight : float
        The desired target weight for the portfolio's assets.
    history : list
        A record of the portfolio's performance over time.
    balancing_dates : list
        Dates when the portfolio was rebalanced.
    df : pandas.DataFrame
        The data source for asset prices.
    verbose : int
        Level of verbosity for logs. 1 for detailed logs, 0 for silent mode.
    trades : dict
        Records of all trades executed on each date.

    Methods:
    --------
    simulate(data: dict)
        Simulates portfolio rebalancing over a given dataset.
    rebalance(date: str, buy_signals: list)
        Rebalances the portfolio based on buy signals for a specific date.
    _reset_history()
        Resets portfolio history to the initial state.
    _update_history_(date: str, last: bool = False)
        Updates the history of the portfolio with the latest changes.
    _update_portfolio_value_(date: str)
        Calculates the current portfolio value based on asset prices.
    _api_call_(assets: list, start_date: str, end_date: str) -> pandas.DataFrame
        Retrieves historical data for given assets between specified dates.
    _sell_(asset: str, quantity: float, date: str)
        Sells a specified quantity of an asset.
    _buy_(asset: str, quantity: float, date: str)
        Buys a specified quantity of an asset.
    _split_number_into_parts(number: float, n: int) -> list
        Splits a number into `n` parts with equal distribution.
    """
    def __init__ (self, initial_cash, target_weight, df, verbose=1):
        """
        Initializes the PortfolioSimulator.

        Parameters:
        -----------
        initial_cash : float
            The initial cash amount for investment.
        target_weight : float
            The target weight for asset allocation.
        df : pandas.DataFrame
            The data source for asset prices.
        verbose : int, optional
            Level of verbosity for logs (default is 1 for detailed logs).
        """
        if verbose not in [1, 0]:
            raise ValueError(f"Verbose parameter must be 0 (silent) or 1 (monitor)")
        self.initial_cash=initial_cash
        self.liquid_money=initial_cash
        self.portfolio_value=initial_cash
        self.positions={}
        self.target_weight=target_weight
        self.history = []
        self.balancing_dates = []
        self.df = df
        self.verbose=verbose
        self.trades = {}

    def simulate (self, data):
        """
        Simulates portfolio rebalancing over a given dataset.

        Parameters:
        -----------
        data : dict
            Dictionary containing dates as keys and buy signals as values.
        """
        for date, buy_signals in data.items():
            self.rebalance(date=date, buy_signals=buy_signals)

    def rebalance (self, date, buy_signals):
        """
        Rebalances the portfolio based on buy signals for a specific date.

        Parameters:
        -----------
        date : str
            The date of the rebalance operation.
        buy_signals : list
            List of assets to be included in the portfolio.
        """
        if self.verbose==1:
            print (f'\n{date}\n')
        self.balancing_dates.append(date)
        self._update_portfolio_value_(date)
        if len(buy_signals)==0:
            self._update_history_ (date, last=True)
        else:
            self.trades[date] = []
            target_weights = self._split_number_into_parts(number=self.target_weight, n=len(buy_signals))
            if self.verbose==1:
                print (f"Target weights sum: {sum(target_weights)}")
            current_positions = list(self.positions.keys())
            keeping_positions = list(set(current_positions) & set(buy_signals))
            keeping_target_weights = target_weights[:len(keeping_positions)]
            selling_positions = list(set(current_positions) - set(buy_signals)) 
            buying_positions = list(set(buy_signals)-set(current_positions))
            buying_target_weights = target_weights[len(keeping_positions):]
            if len(selling_positions) != 0:
                for asset_to_sell in selling_positions:
                    self._sell_(asset=asset_to_sell, quantity = True, date=date)
            if len(keeping_positions) != 0:
                keeping_selling_positions = []
                keeping_buying_positions = []
                for asset_to_keep, target_weight in zip(keeping_positions, keeping_target_weights):
                    if self.positions[asset_to_keep]['Allocation'] > target_weight:
                        keeping_selling_positions.append(asset_to_keep)
                    else:
                        keeping_buying_positions.append(asset_to_keep)
                keeping_positions = keeping_selling_positions + keeping_buying_positions
                for asset_to_keep, target_weight in zip(keeping_positions, keeping_target_weights):
                    if self.positions[asset_to_keep]['Allocation'] > target_weight:
                        self._sell_(asset=asset_to_keep, quantity=(((self.positions[asset_to_keep]['Allocation']-target_weight)*(self.positions[asset_to_keep]['Amount']))/(self.positions[asset_to_keep]['Allocation'])), date=date)
                    elif self.positions[asset_to_keep]['Allocation'] < target_weight:
                        self._buy_ (asset=asset_to_keep, quantity=((target_weight*self.positions[asset_to_keep]['Amount'])/(self.positions[asset_to_keep]['Allocation'])) - self.positions[asset_to_keep]['Amount'], date=date)
            if len (buying_positions) != 0:
                buying_splits = []
                for target_weight in buying_target_weights:
                    buying_splits.append(self.portfolio_value * target_weight)
                for asset_to_buy, buying_amount in zip(buying_positions, buying_splits):
                    self._buy_(asset=asset_to_buy, quantity=buying_amount, date=date)
            self._update_history_ (date)

    def _reset_history (self):
        self.liquid_money=self.initial_cash
        self.portfolio_value=self.initial_cash
        self.positions={}
        self.history = []
        self.balancing_dates = []
    def _update_history_(self, date, last=False):
        if len(self.history) == 0:
            for asset in self.positions:
                self.history.append({
                    'Date': date,
                    'Asset': asset,
                    'Group': 0,
                    'Allocation': self.positions[asset]['Allocation'],
                    'Amount': self.positions[asset]['Amount'],
                    'Asset Price': self.df.loc[date, asset]
                })
        else:
            last_balancing_date = self.balancing_dates[-2]
            last_balancing_date_record = pd.DataFrame(self.history).loc[pd.DataFrame(self.history)['Date'] == last_balancing_date]
            record_groups = last_balancing_date_record['Group'].unique()
            if len(record_groups) >1:
                last_balancing_date_record = last_balancing_date_record.loc[last_balancing_date_record['Group']==record_groups[-1]]
            last_balancing_record_updating_dates = pd.date_range(start=last_balancing_date, end=date, freq='B').strftime('%Y-%m-%d').tolist()
            last_balancing_assets = last_balancing_date_record['Asset'].tolist()
            assets_df = self._api_call_(assets=last_balancing_assets, start_date=last_balancing_date, end_date=last_balancing_record_updating_dates[-1])
            last_balancing_record_updating_dates = [date for date in last_balancing_record_updating_dates if date in assets_df.index]
            assets_returns_df = pd.DataFrame(calculate_returns(assets_df.values, period=1), columns=assets_df.columns, index = assets_df.index[1:])
            date_portfolio_value = last_balancing_date_record['Amount'].sum() ### Un record del valor del portafolio en la ultima balancing date
            last_date_record = last_balancing_date_record.copy() ### Un record de la última fecha actualizada
            for update_date in last_balancing_record_updating_dates[1:]:
                date_portfolio_value += np.dot(last_balancing_date_record['Amount'].values, assets_returns_df.loc[update_date].values)
                assets_amounts = []
                for asset in last_balancing_assets:
                    asset_amount = last_date_record.loc[last_date_record['Asset']==asset]['Amount'].iloc[0] * (1 + assets_returns_df.loc[update_date, asset])
                    assets_amounts.append(asset_amount)
                assets_allocation = [(x / sum(assets_amounts)) for x in assets_amounts]
                assets_allocation[-1] = 1 - sum(assets_allocation[:-1])
                for asset, asset_amount, asset_allocation in zip(last_balancing_assets, assets_amounts, assets_allocation):
                    self.history.append({
                        'Date': update_date,
                        'Asset': asset,
                        'Group': 0,
                        'Allocation': asset_allocation,
                        'Amount': asset_amount,
                        'Asset Price': self.df.loc[update_date, asset]
                    })
                last_date_record = pd.DataFrame(self.history).loc[pd.DataFrame(self.history)['Date'] == update_date]
            if not last:
                for asset in self.positions:
                    self.history.append({
                        'Date' : date,
                        'Asset' : asset,
                        'Group': 1,
                        'Allocation': self.positions[asset]['Allocation'],
                        'Amount': self.positions[asset]['Amount'],
                        'Asset Price': self.df.loc[date, asset]
                    })
    def _update_portfolio_value_(self, date):
        if len(self.history)==0:
            self.portfolio_value = self.portfolio_value
            self.positions = self.positions
        else:
            last_balancing_date = self.balancing_dates[-2]
            last_balancing_date_record = pd.DataFrame(self.history).loc[pd.DataFrame(self.history)['Date'] == last_balancing_date]
            record_groups = last_balancing_date_record['Group'].unique()
            if len(record_groups) >1:
                last_balancing_date_record = last_balancing_date_record.loc[last_balancing_date_record['Group']==record_groups[-1]]
            dates = pd.date_range(start=last_balancing_date, end=date, freq='B').strftime('%Y-%m-%d').tolist()
            global assets_df
            assets_df = self._api_call_(assets = list(self.positions.keys()), start_date=dates[0], end_date=dates[-1])
            log_returns_df = pd.DataFrame(calculate_log_returns(assets_df.values, period=1), columns = assets_df.columns, index = assets_df.index[1:])
            self.portfolio_value = np.sum(np.exp(log_returns_df.sum().values) * last_balancing_date_record['Amount'].values)
            for asset in self.positions:
                self.positions[asset]['Amount'] = self.positions[asset]['Amount'] * np.exp(log_returns_df[asset].sum())
                self.positions[asset]['Allocation'] = self.positions[asset]['Amount'] / self.portfolio_value
    def _api_call_ (self, assets, start_date, end_date):
        df= self.df.copy()
        df= df[assets]
        df= df.loc[(df.index>=start_date) & (df.index<=end_date)]
        df.columns = assets
        return df

    def _sell_ (self, asset, quantity, date):
        if asset not in self.positions:
            raise ValueError (f"You can't sell {asset} because it's not in the portfolio.")
        if quantity is True:
            if self.verbose==1:
                print (f"selling {self.positions[asset]['Amount']} of {asset} ")
            self.liquid_money += self.positions[asset]['Amount']
            del self.positions[asset]
        else:
            if self.positions[asset]['Amount'] < quantity:
                raise ValueError(f"You can't sell ${quantity} of {asset}, you only have ${self.positions[asset]['Amount']}")
            else:
                self.liquid_money += quantity
                self.positions[asset]['Amount'] -= quantity
                self.positions[asset]['Allocation'] = self.positions[asset]['Amount'] / self.portfolio_value

    def _buy_ (self, asset, quantity, date):
        if self.verbose==1:
            print (f'Buying {quantity} of {asset}')
        self.trades[date].append(f'Buying {quantity} of {asset}')
        if quantity > self.liquid_money:
            if quantity - self.liquid_money < 0.0001:
                quantity = self.liquid_money
            else:
                raise ValueError (f"Cannot buy {quantity} of {asset} because the liquid money is: {self.liquid_money:.2f}")
        self.liquid_money -= quantity
        if asset in self.positions:
            self.positions[asset]['Amount'] += quantity
            self.positions[asset]['Allocation'] = self.positions[asset]['Amount'] / self.portfolio_value 
        else:
            self.positions[asset] = {
                'Allocation': quantity / self.portfolio_value,
                'Amount': quantity
            }
    def _split_number_into_parts(self, number, n):
        base_part = number / n
        remainder = number - base_part * n
        parts = [base_part] * n
        for i in range(int(remainder * n)):
            parts[i] += 1 / n
        return parts

class MonteCarloSimulator:
    """
    A class for simulating scenarios using the Monte Carlo method on a dataset. This simulator
    generates paths based on the mean and standard deviation of an input array and optionally 
    updates the statistics of each feature after every simulation step.

    Attributes
    ----------
    steps : int
        Number of simulation steps (time steps) to generate.
    paths : int
        Number of Monte Carlo simulation paths (scenarios) to generate.

    Methods
    -------
    simulate(X, axis=0, update=False):
        Runs the Monte Carlo simulation on the input data array `X`.
    """

    def __init__(self, steps, paths):
        """
        Initializes the MonteCarloSimulator with the specified number of steps and paths.

        Parameters
        ----------
        steps : int
            The number of time steps in each simulation.
        paths : int
            The number of simulation paths to generate.
        """
        self.steps = steps
        self.paths = paths

    def simulate(self, X, axis=0, update=False):
        """
        Performs Monte Carlo simulations based on the statistics (mean and standard deviation) of the input array `X`.
        
        If `update` is True, the mean and standard deviation are recalculated for each feature at every simulation step.
        
        Parameters
        ----------
        X : np.ndarray
            The input data array used to initialize the simulation's statistics. Must be a 2D array.
        axis : int, optional
            The axis along which to calculate the statistics. Default is 0 (rows).
        update : bool, optional
            If True, updates the mean and standard deviation after each simulation step. Default is False.
        
        Returns
        -------
        simulations : np.ndarray
            A 3D array of shape (steps, paths, features) representing the simulated paths.
        
        Raises
        ------
        ValueError
            If `X` is not a 2D numpy array, contains NaNs, or if `axis` is not 0 or 1.
        """

        axles = [0, 1]
        if not isinstance(X, np.ndarray):
            raise ValueError("X must be an array")
        if X.ndim != 2:
            raise ValueError("Array must be bidimensional")
        if np.isnan(X).any():
            raise ValueError("Array contains NaNs")
        if axis not in axles:
            raise ValueError("Axis out of range")
        axles.remove(axis)
        if update not in [True, False]:
            raise ValueError("update not a boolean parameter")

        if update:
            std = np.zeros((1, self.paths, X.shape[axles[0]]))
            mean = np.zeros((1, self.paths, X.shape[axles[0]]))
            for feature in range(X.shape[axles[0]]):
                std[0, :, feature] = np.repeat(np.std(np.take(X, feature, axis=axles[0])), self.paths)
                mean[0, :, feature] = np.repeat(np.mean(np.take(X, feature, axis=axles[0])), self.paths)
            
            simulations = np.zeros((self.steps, self.paths, X.shape[axles[0]]))
            for step in range(self.steps):
                current_simulations = np.random.normal(loc=mean, scale=std, size=(1, self.paths, X.shape[axles[0]]))
                for feature in range(X.shape[axles[0]]):
                    std[0, :, feature] = np.std(
                        np.concatenate([np.tile(np.take(X, feature, axis=axles[0]).reshape(-1, 1), self.paths),
                                        np.take(current_simulations[0, :, :], feature, axis=1).reshape(1, -1)], axis=0),
                        axis=0
                    )
                    mean[0, :, feature] = np.mean(
                        np.concatenate([np.tile(np.take(X, feature, axis=axles[0]).reshape(-1, 1), self.paths),
                                        np.take(current_simulations[0, :, :], feature, axis=1).reshape(1, -1)], axis=0),
                        axis=0
                    )
                simulations[step, :, :] = current_simulations[0, :, :]

        else:
            std = np.std(X, axis=axis)
            mean = np.mean(X, axis=axis)
            simulations = np.random.normal(loc=mean, scale=std, size=(self.steps, self.paths, X.shape[axles[0]]))

        return simulations
