#!/usr/bin/env python3
"""
Risk Profile Assessment System for Agent Chopra
Comprehensive risk assessment and company recommendation engine
"""

import os
import json
import yfinance as yf
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from database.models import RiskLevel, Sector

@dataclass
class RiskProfile:
    """Risk profile data structure"""
    first_name: str
    last_name: str
    score: int  # 1-10
    level: RiskLevel
    description: str
    allocation: Dict[str, float]
    max_position_size: float
    recommended_sectors: List[Sector]
    avoid_sectors: List[Sector]
    trading_strategy: str = "Conservative"
    automated_trading_enabled: bool = False
    max_daily_trades: int = 3
    stop_loss_percentage: float = 5.0

@dataclass
class StockRecommendation:
    """Stock recommendation with risk analysis"""
    symbol: str
    company_name: str
    sector: Sector
    risk_rating: int
    recommendation_strength: float  # 0-1
    target_allocation: float
    reasoning: str
    current_price: float
    target_price: float

class RiskProfiler:
    """Comprehensive risk profiling and assessment system"""

    def __init__(self):
        self.risk_profiles = self._initialize_risk_profiles()
        self.sector_risk_ratings = self._initialize_sector_risks()
        self.stock_universe = self._initialize_stock_universe()

    def _initialize_risk_profiles(self) -> Dict[int, RiskProfile]:
        """Initialize risk profile definitions"""
        return {
            1: RiskProfile(
                first_name="",
                last_name="",
                score=1,
                level=RiskLevel.VERY_LOW,
                description="Ultra-conservative investor seeking capital preservation",
                allocation={"bonds": 70, "cash": 20, "stocks": 10},
                max_position_size=0.05,
                recommended_sectors=[Sector.UTILITIES, Sector.CONSUMER_STAPLES],
                avoid_sectors=[Sector.TECHNOLOGY, Sector.ENERGY, Sector.CONSUMER_DISCRETIONARY]
            ),
            2: RiskProfile(
                first_name="",
                last_name="",
                score=2,
                level=RiskLevel.LOW,
                description="Conservative investor with minimal risk tolerance",
                allocation={"bonds": 60, "stocks": 30, "cash": 10},
                max_position_size=0.08,
                recommended_sectors=[Sector.UTILITIES, Sector.CONSUMER_STAPLES, Sector.HEALTHCARE],
                avoid_sectors=[Sector.TECHNOLOGY, Sector.ENERGY]
            ),
            3: RiskProfile(
                first_name="",
                last_name="",
                score=3,
                level=RiskLevel.LOW_MODERATE,
                description="Cautious investor with slight growth orientation",
                allocation={"stocks": 40, "bonds": 50, "cash": 10},
                max_position_size=0.10,
                recommended_sectors=[Sector.HEALTHCARE, Sector.CONSUMER_STAPLES, Sector.UTILITIES, Sector.FINANCIALS],
                avoid_sectors=[Sector.ENERGY, Sector.MATERIALS]
            ),
            4: RiskProfile(
                first_name="",
                last_name="",
                score=4,
                level=RiskLevel.MODERATE,
                description="Balanced investor seeking steady growth",
                allocation={"stocks": 50, "bonds": 40, "cash": 10},
                max_position_size=0.12,
                recommended_sectors=[Sector.HEALTHCARE, Sector.FINANCIALS, Sector.CONSUMER_STAPLES, Sector.INDUSTRIALS],
                avoid_sectors=[Sector.ENERGY]
            ),
            5: RiskProfile(
                first_name="",
                last_name="",
                score=5,
                level=RiskLevel.MODERATE_HIGH,
                description="Growth-oriented investor with moderate risk tolerance",
                allocation={"stocks": 60, "bonds": 30, "cash": 10},
                max_position_size=0.15,
                recommended_sectors=[Sector.TECHNOLOGY, Sector.HEALTHCARE, Sector.FINANCIALS, Sector.INDUSTRIALS],
                avoid_sectors=[]
            ),
            6: RiskProfile(
                first_name="",
                last_name="",
                score=6,
                level=RiskLevel.HIGH,
                description="Growth investor comfortable with market volatility",
                allocation={"stocks": 70, "bonds": 20, "cash": 10},
                max_position_size=0.18,
                recommended_sectors=[Sector.TECHNOLOGY, Sector.HEALTHCARE, Sector.CONSUMER_DISCRETIONARY, Sector.FINANCIALS],
                avoid_sectors=[]
            ),
            7: RiskProfile(
                first_name="",
                last_name="",
                score=7,
                level=RiskLevel.HIGH_AGGRESSIVE,
                description="Aggressive growth investor",
                allocation={"stocks": 80, "bonds": 15, "cash": 5},
                max_position_size=0.20,
                recommended_sectors=[Sector.TECHNOLOGY, Sector.CONSUMER_DISCRETIONARY, Sector.HEALTHCARE, Sector.INDUSTRIALS],
                avoid_sectors=[]
            ),
            8: RiskProfile(
                first_name="",
                last_name="",
                score=8,
                level=RiskLevel.AGGRESSIVE,
                description="High-risk investor seeking maximum growth",
                allocation={"stocks": 90, "bonds": 5, "cash": 5},
                max_position_size=0.25,
                recommended_sectors=[Sector.TECHNOLOGY, Sector.CONSUMER_DISCRETIONARY, Sector.ENERGY, Sector.MATERIALS],
                avoid_sectors=[]
            ),
            9: RiskProfile(
                first_name="",
                last_name="",
                score=9,
                level=RiskLevel.VERY_AGGRESSIVE,
                description="Very high-risk investor with growth focus",
                allocation={"stocks": 95, "bonds": 0, "cash": 5},
                max_position_size=0.30,
                recommended_sectors=[Sector.TECHNOLOGY, Sector.ENERGY, Sector.MATERIALS, Sector.CONSUMER_DISCRETIONARY],
                avoid_sectors=[]
            ),
            10: RiskProfile(
                first_name="",
                last_name="",
                score=10,
                level=RiskLevel.EXTREME,
                description="Maximum risk tolerance, speculative investor",
                allocation={"stocks": 100, "bonds": 0, "cash": 0},
                max_position_size=0.35,
                recommended_sectors=[Sector.TECHNOLOGY, Sector.ENERGY, Sector.MATERIALS, Sector.CONSUMER_DISCRETIONARY],
                avoid_sectors=[]
            )
        }

    def _initialize_sector_risks(self) -> Dict[Sector, int]:
        """Initialize sector risk ratings (1-10)"""
        return {
            Sector.UTILITIES: 2,
            Sector.CONSUMER_STAPLES: 3,
            Sector.HEALTHCARE: 4,
            Sector.TELECOMMUNICATIONS: 4,
            Sector.REAL_ESTATE: 5,
            Sector.FINANCIALS: 6,
            Sector.INDUSTRIALS: 6,
            Sector.CONSUMER_DISCRETIONARY: 7,
            Sector.MATERIALS: 8,
            Sector.TECHNOLOGY: 8,
            Sector.ENERGY: 9
        }

    def _initialize_stock_universe(self) -> Dict[str, Dict]:
        """Initialize stock universe with risk ratings"""
        return {
            # Conservative Stocks (Risk 1-3)
            "JNJ": {"name": "Johnson & Johnson", "sector": Sector.HEALTHCARE, "risk": 2},
            "PG": {"name": "Procter & Gamble", "sector": Sector.CONSUMER_STAPLES, "risk": 2},
            "KO": {"name": "Coca-Cola", "sector": Sector.CONSUMER_STAPLES, "risk": 2},
            "NEE": {"name": "NextEra Energy", "sector": Sector.UTILITIES, "risk": 3},
            "SO": {"name": "Southern Company", "sector": Sector.UTILITIES, "risk": 2},

            # Moderate Stocks (Risk 4-6)
            "MSFT": {"name": "Microsoft", "sector": Sector.TECHNOLOGY, "risk": 4},
            "AAPL": {"name": "Apple", "sector": Sector.TECHNOLOGY, "risk": 5},
            "JPM": {"name": "JPMorgan Chase", "sector": Sector.FINANCIALS, "risk": 5},
            "V": {"name": "Visa", "sector": Sector.FINANCIALS, "risk": 4},
            "UNH": {"name": "UnitedHealth", "sector": Sector.HEALTHCARE, "risk": 4},
            "HD": {"name": "Home Depot", "sector": Sector.CONSUMER_DISCRETIONARY, "risk": 5},
            "WMT": {"name": "Walmart", "sector": Sector.CONSUMER_STAPLES, "risk": 3},

            # Growth Stocks (Risk 7-8)
            "GOOGL": {"name": "Alphabet", "sector": Sector.TECHNOLOGY, "risk": 6},
            "AMZN": {"name": "Amazon", "sector": Sector.CONSUMER_DISCRETIONARY, "risk": 7},
            "TSLA": {"name": "Tesla", "sector": Sector.CONSUMER_DISCRETIONARY, "risk": 8},
            "NVDA": {"name": "NVIDIA", "sector": Sector.TECHNOLOGY, "risk": 8},
            "META": {"name": "Meta Platforms", "sector": Sector.TECHNOLOGY, "risk": 7},
            "NFLX": {"name": "Netflix", "sector": Sector.CONSUMER_DISCRETIONARY, "risk": 7},

            # High Risk Stocks (Risk 9-10)
            "ARKK": {"name": "ARK Innovation ETF", "sector": Sector.TECHNOLOGY, "risk": 9},
            "COIN": {"name": "Coinbase", "sector": Sector.FINANCIALS, "risk": 10},
            "RIVN": {"name": "Rivian", "sector": Sector.CONSUMER_DISCRETIONARY, "risk": 10},
            "PLTR": {"name": "Palantir", "sector": Sector.TECHNOLOGY, "risk": 9},

            # ETFs for diversification
            "SPY": {"name": "SPDR S&P 500", "sector": Sector.FINANCIALS, "risk": 5},
            "QQQ": {"name": "Invesco QQQ", "sector": Sector.TECHNOLOGY, "risk": 6},
            "VTI": {"name": "Vanguard Total Stock", "sector": Sector.FINANCIALS, "risk": 5},
            "TLT": {"name": "iShares 20+ Year Treasury", "sector": Sector.FINANCIALS, "risk": 3},
            "GLD": {"name": "SPDR Gold Shares", "sector": Sector.MATERIALS, "risk": 4}
        }

    def assess_risk_profile(self, user_data: Dict) -> Tuple[int, RiskProfile]:
        """
        Assess user's risk profile based on 3-question questionnaire

        Args:
            user_data: Dictionary containing user information including:
                - q1_risk_tolerance: int (1-10)
                - q2_investment_experience: int (1-10)
                - q3_time_horizon: int (1-10)
                - first_name: str
                - last_name: str
                - trading_strategy: str
                - automated_trading: bool

        Returns:
            Tuple of (risk_score, risk_profile)
        """
        # Calculate weighted average of the 3 questions
        risk_tolerance = user_data.get('q1_risk_tolerance', 5)
        experience = user_data.get('q2_investment_experience', 5)
        time_horizon = user_data.get('q3_time_horizon', 5)

        # Weighted scoring: Risk tolerance is most important
        weighted_score = (
            risk_tolerance * 0.5 +  # 50% weight
            experience * 0.3 +      # 30% weight
            time_horizon * 0.2      # 20% weight
        )

        # Round to nearest integer for final score
        final_score = max(1, min(10, round(weighted_score)))
            'expert': 3
        }
        score += exp_scores.get(experience, 0)

        # Time horizon scoring
        time_horizon = user_data.get('time_horizon', 'medium')
        horizon_scores = {
            'short': 0,
            'medium': 1,
            'long': 2,
            'very_long': 3
        }
        score += horizon_scores.get(time_horizon, 1)

        # Risk tolerance scoring
        risk_tolerance = user_data.get('risk_tolerance', 'moderate')
        tolerance_scores = {
            'very_low': 0,
            'low': 1,
            'moderate': 2,
            'high': 3,
            'very_high': 4
        }
        score += tolerance_scores.get(risk_tolerance, 2)

        # Extract the 5 key risk assessment answers
        q1 = user_data.get('q1_loss_comfort', 5)  # 1=very uncomfortable, 10=very comfortable
        q2 = user_data.get('q2_volatility_tolerance', 5)  # 1=very low tolerance, 10=high tolerance
        q3 = user_data.get('q3_investment_experience', 5)  # 1=beginner, 10=expert
        q4 = user_data.get('q4_time_horizon', 5)  # 1=short term, 10=long term
        q5 = user_data.get('q5_income_stability', 5)  # 1=unstable, 10=very stable

        # Calculate weighted average (equal weights for simplicity)
        risk_score = round((q1 + q2 + q3 + q4 + q5) / 5)

        # Ensure score is within 1-10 range
        final_score = max(1, min(10, risk_score))

        # Get the base risk profile
        base_profile = self.risk_profiles[final_score]

        # Create personalized risk profile with user data
        personalized_profile = RiskProfile(
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
            score=final_score,
            level=base_profile.level,
            description=base_profile.description,
            allocation=base_profile.allocation,
            max_position_size=base_profile.max_position_size,
            recommended_sectors=base_profile.recommended_sectors,
            avoid_sectors=base_profile.avoid_sectors,
            trading_strategy=user_data.get('trading_strategy', 'Conservative'),
            automated_trading_enabled=user_data.get('automated_trading', False),
            max_daily_trades=user_data.get('max_daily_trades', 3),
            stop_loss_percentage=user_data.get('stop_loss_percentage', 5.0)
        )

        return final_score, personalized_profile

    def get_risk_questions(self) -> List[Dict]:
        """
        Get the 3 essential risk assessment questions

        Returns:
            List of question dictionaries with question text and scale info
        """
        return [
            {
                'id': 'q1_risk_tolerance',
                'question': 'What is your overall risk tolerance for investments?',
                'description': 'Consider how much portfolio volatility and potential loss you can handle.',
                'scale_low': '1 - Very Conservative (Capital preservation is key)',
                'scale_high': '10 - Very Aggressive (High risk for high returns)'
            },
            {
                'id': 'q2_investment_experience',
                'question': 'What is your investment and trading experience level?',
                'description': 'Your knowledge of markets, financial instruments, and trading strategies.',
                'scale_low': '1 - Beginner (New to investing)',
                'scale_high': '10 - Expert (Extensive trading experience)'
            },
            {
                'id': 'q3_time_horizon',
                'question': 'What is your investment time horizon and liquidity needs?',
                'description': 'How long can you keep money invested before needing access to it.',
                'scale_low': '1 - Short-term (Less than 2 years)',
                'scale_high': '10 - Long-term (10+ years)'
            }
        ]

    def get_trading_strategies(self) -> List[Dict]:
        """
        Get available trading strategies for automated trading

        Returns:
            List of strategy dictionaries
        """
        return [
            {
                'name': 'Conservative',
                'description': 'Low risk, stable returns with dividend focus',
                'risk_level': 1,
                'max_position_size': 5.0,
                'stop_loss': 3.0,
                'sectors': ['Healthcare', 'Utilities', 'Consumer Staples']
            },
            {
                'name': 'Balanced',
                'description': 'Moderate risk with balanced growth and income',
                'risk_level': 5,
                'max_position_size': 10.0,
                'stop_loss': 5.0,
                'sectors': ['Technology', 'Healthcare', 'Financials', 'Industrials']
            },
            {
                'name': 'Growth',
                'description': 'Higher risk focused on capital appreciation',
                'risk_level': 7,
                'max_position_size': 15.0,
                'stop_loss': 8.0,
                'sectors': ['Technology', 'Communication Services', 'Consumer Discretionary']
            },
            {
                'name': 'Aggressive',
                'description': 'High risk, high reward with emerging sectors',
                'risk_level': 9,
                'max_position_size': 20.0,
                'stop_loss': 12.0,
                'sectors': ['Technology', 'Biotechnology', 'Clean Energy', 'Cryptocurrency']
            }
        ]

    def _analyze_trading_behavior(self, trading_history: List[Dict]) -> int:
        """Analyze trading history to adjust risk score"""
        if not trading_history:
            return 0

        # Analyze volatility of trades
        high_risk_symbols = ['TSLA', 'NVDA', 'ARKK', 'COIN', 'PLTR']
        high_risk_trades = sum(1 for trade in trading_history
                              if trade.get('symbol') in high_risk_symbols)

        risk_ratio = high_risk_trades / len(trading_history)

        if risk_ratio > 0.5:
            return 2  # High risk behavior
        elif risk_ratio > 0.3:
            return 1  # Moderate risk behavior
        else:
            return 0  # Conservative behavior

    def get_stock_recommendations(self, risk_profile: RiskProfile,
                                current_portfolio: List[Dict] = None,
                                exclude_owned: bool = True) -> List[StockRecommendation]:
        """
        Get stock recommendations based on risk profile

        Args:
            risk_profile: User's risk profile
            current_portfolio: Current holdings
            exclude_owned: Whether to exclude currently owned stocks

        Returns:
            List of stock recommendations
        """
        recommendations = []
        owned_symbols = set()

        if current_portfolio and exclude_owned:
            owned_symbols = {pos['symbol'] for pos in current_portfolio}

        # Filter stocks by risk compatibility
        compatible_stocks = {}
        for symbol, data in self.stock_universe.items():
            if exclude_owned and symbol in owned_symbols:
                continue

            stock_risk = data['risk']
            sector = data['sector']

            # Check if stock risk is compatible with user profile
            if self._is_risk_compatible(stock_risk, risk_profile.score):
                # Check if sector is recommended
                if not risk_profile.avoid_sectors or sector not in risk_profile.avoid_sectors:
                    compatible_stocks[symbol] = data

        # Get current market data and create recommendations
        for symbol, data in compatible_stocks.items():
            try:
                recommendation = self._create_stock_recommendation(
                    symbol, data, risk_profile
                )
                if recommendation:
                    recommendations.append(recommendation)
            except Exception as e:
                print(f"Error creating recommendation for {symbol}: {e}")
                continue

        # Sort by recommendation strength
        recommendations.sort(key=lambda x: x.recommendation_strength, reverse=True)

        return recommendations[:10]  # Return top 10

    def _is_risk_compatible(self, stock_risk: int, user_risk: int) -> bool:
        """Check if stock risk is compatible with user risk profile"""
        # Allow stocks within ±2 risk levels
        return abs(stock_risk - user_risk) <= 2

    def _create_stock_recommendation(self, symbol: str, stock_data: Dict,
                                   risk_profile: RiskProfile) -> Optional[StockRecommendation]:
        """Create a stock recommendation with analysis"""
        try:
            # Get current market data
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="3mo")

            if hist.empty:
                return None

            current_price = hist['Close'].iloc[-1]

            # Calculate recommendation strength
            strength = self._calculate_recommendation_strength(
                symbol, stock_data, risk_profile, hist, info
            )

            # Calculate target allocation
            target_allocation = min(
                risk_profile.max_position_size,
                0.05 + (strength * 0.15)  # 5-20% based on strength
            )

            # Generate reasoning
            reasoning = self._generate_recommendation_reasoning(
                symbol, stock_data, risk_profile, strength
            )

            # Estimate target price (simple momentum-based)
            target_price = self._estimate_target_price(hist, current_price)

            return StockRecommendation(
                symbol=symbol,
                company_name=stock_data['name'],
                sector=stock_data['sector'],
                risk_rating=stock_data['risk'],
                recommendation_strength=strength,
                target_allocation=target_allocation,
                reasoning=reasoning,
                current_price=current_price,
                target_price=target_price
            )

        except Exception as e:
            print(f"Error analyzing {symbol}: {e}")
            return None

    def _calculate_recommendation_strength(self, symbol: str, stock_data: Dict,
                                         risk_profile: RiskProfile, hist: pd.DataFrame,
                                         info: Dict) -> float:
        """Calculate recommendation strength (0-1)"""
        strength = 0.5  # Base strength

        # Risk compatibility bonus
        risk_diff = abs(stock_data['risk'] - risk_profile.score)
        if risk_diff == 0:
            strength += 0.2
        elif risk_diff == 1:
            strength += 0.1

        # Sector preference bonus
        if stock_data['sector'] in risk_profile.recommended_sectors:
            strength += 0.2

        # Technical analysis
        if len(hist) >= 20:
            # Price momentum
            recent_return = (hist['Close'].iloc[-1] / hist['Close'].iloc[-20] - 1)
            if recent_return > 0.05:  # 5% gain in 20 days
                strength += 0.1
            elif recent_return < -0.05:
                strength -= 0.1

            # Volume trend
            recent_volume = hist['Volume'].iloc[-5:].mean()
            avg_volume = hist['Volume'].mean()
            if recent_volume > avg_volume * 1.2:
                strength += 0.05

        # Fundamental analysis (if available)
        if info:
            pe_ratio = info.get('trailingPE')
            if pe_ratio and 10 <= pe_ratio <= 25:
                strength += 0.1

        return max(0, min(1, strength))

    def _generate_recommendation_reasoning(self, symbol: str, stock_data: Dict,
                                         risk_profile: RiskProfile, strength: float) -> str:
        """Generate human-readable reasoning for recommendation"""
        reasons = []

        # Risk compatibility
        risk_diff = abs(stock_data['risk'] - risk_profile.score)
        if risk_diff <= 1:
            reasons.append(f"Risk level ({stock_data['risk']}/10) aligns well with your profile")

        # Sector alignment
        if stock_data['sector'] in risk_profile.recommended_sectors:
            reasons.append(f"{stock_data['sector'].value.title()} sector matches your preferences")

        # Strength assessment
        if strength > 0.7:
            reasons.append("Strong technical and fundamental indicators")
        elif strength > 0.5:
            reasons.append("Positive momentum and solid fundamentals")
        else:
            reasons.append("Decent fundamentals with growth potential")

        return ". ".join(reasons)

    def _estimate_target_price(self, hist: pd.DataFrame, current_price: float) -> float:
        """Simple target price estimation"""
        if len(hist) < 50:
            return current_price * 1.1  # Default 10% upside

        # Calculate support and resistance levels
        highs = hist['High'].rolling(20).max()
        lows = hist['Low'].rolling(20).min()

        resistance = highs.iloc[-20:].max()
        support = lows.iloc[-20:].min()

        # Target price based on technical levels
        if current_price < (support + resistance) / 2:
            # If below midpoint, target resistance
            return min(resistance, current_price * 1.15)
        else:
            # If above midpoint, conservative target
            return current_price * 1.08

    def calculate_portfolio_risk_score(self, portfolio: List[Dict]) -> Dict:
        """Calculate overall portfolio risk metrics"""
        if not portfolio:
            return {"score": 0, "level": "No Portfolio", "diversification": 0}

        total_value = sum(pos.get('market_value', 0) for pos in portfolio)
        if total_value == 0:
            return {"score": 0, "level": "No Value", "diversification": 0}

        # Calculate weighted risk score
        weighted_risk = 0
        sector_weights = {}

        for position in portfolio:
            symbol = position.get('symbol', '')
            market_value = position.get('market_value', 0)
            weight = market_value / total_value

            # Get stock risk
            stock_info = self.stock_universe.get(symbol, {})
            stock_risk = stock_info.get('risk', 5)
            sector = stock_info.get('sector', Sector.TECHNOLOGY)

            weighted_risk += stock_risk * weight

            # Track sector allocation
            sector_name = sector.value if hasattr(sector, 'value') else str(sector)
            sector_weights[sector_name] = sector_weights.get(sector_name, 0) + weight

        # Calculate diversification score
        diversification_score = self._calculate_diversification_score(sector_weights)

        # Determine risk level
        risk_level = self._get_risk_level_name(int(round(weighted_risk)))

        return {
            "score": round(weighted_risk, 1),
            "level": risk_level,
            "diversification": round(diversification_score, 2),
            "sector_allocation": sector_weights,
            "recommendations": self._get_portfolio_recommendations(
                weighted_risk, diversification_score, sector_weights
            )
        }

    def _calculate_diversification_score(self, sector_weights: Dict[str, float]) -> float:
        """Calculate diversification score using Herfindahl-Hirschman Index"""
        if not sector_weights:
            return 0

        # HHI calculation
        hhi = sum(weight ** 2 for weight in sector_weights.values())

        # Convert to diversification score (1 - normalized HHI)
        # Perfect diversification across 10 sectors would have HHI = 0.1
        max_hhi = 1.0  # Maximum concentration (all in one sector)
        min_hhi = 1 / len(Sector)  # Perfect diversification

        diversification = 1 - (hhi - min_hhi) / (max_hhi - min_hhi)
        return max(0, min(1, diversification))

    def _get_risk_level_name(self, risk_score: int) -> str:
        """Get risk level name from score"""
        risk_names = {
            1: "Very Low Risk",
            2: "Low Risk",
            3: "Low-Moderate Risk",
            4: "Moderate Risk",
            5: "Moderate-High Risk",
            6: "High Risk",
            7: "High-Aggressive Risk",
            8: "Aggressive Risk",
            9: "Very Aggressive Risk",
            10: "Extreme Risk"
        }
        return risk_names.get(risk_score, "Moderate Risk")

    def _get_portfolio_recommendations(self, risk_score: float,
                                     diversification_score: float,
                                     sector_weights: Dict[str, float]) -> List[str]:
        """Generate portfolio improvement recommendations"""
        recommendations = []

        # Diversification recommendations
        if diversification_score < 0.3:
            recommendations.append("Consider diversifying across more sectors")

        # Sector concentration warnings
        for sector, weight in sector_weights.items():
            if weight > 0.4:
                recommendations.append(f"High concentration in {sector} ({weight:.1%}) - consider reducing")

        # Risk level recommendations
        if risk_score > 8:
            recommendations.append("Portfolio risk is very high - consider adding defensive positions")
        elif risk_score < 3:
            recommendations.append("Portfolio is very conservative - consider adding growth positions")

        return recommendations