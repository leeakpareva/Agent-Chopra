#!/usr/bin/env python3
"""
Enhanced Risk Profiler for Agent Chopra
Simplified 3-question risk assessment system
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple, Optional
import pandas as pd

class RiskLevel(Enum):
    VERY_LOW = 1
    LOW = 2
    LOW_MODERATE = 3
    MODERATE = 4
    MODERATE_HIGH = 5
    HIGH = 6
    HIGH_AGGRESSIVE = 7
    AGGRESSIVE = 8
    VERY_AGGRESSIVE = 9
    EXTREME = 10

class Sector(Enum):
    TECHNOLOGY = "Technology"
    HEALTHCARE = "Healthcare"
    FINANCIALS = "Financials"
    CONSUMER_DISCRETIONARY = "Consumer Discretionary"
    CONSUMER_STAPLES = "Consumer Staples"
    ENERGY = "Energy"
    UTILITIES = "Utilities"
    MATERIALS = "Materials"
    INDUSTRIALS = "Industrials"
    REAL_ESTATE = "Real Estate"
    COMMUNICATION = "Communication Services"

@dataclass
class RiskProfile:
    """Enhanced risk profile with personal information"""
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
    name: str
    sector: Sector
    risk_rating: int
    recommendation_strength: float  # 0-1
    target_allocation: float
    reasoning: str
    current_price: float
    target_price: float

class RiskProfiler:
    """Simplified risk profiling and assessment system"""

    def __init__(self):
        self.risk_profiles = self._initialize_risk_profiles()
        self.sector_risk_ratings = self._initialize_sector_risks()
        self.stock_universe = self._initialize_stock_universe()

    def _initialize_risk_profiles(self) -> Dict[int, RiskProfile]:
        """Initialize risk profile definitions"""
        return {
            1: RiskProfile(
                first_name="", last_name="", score=1, level=RiskLevel.VERY_LOW,
                description="Ultra-conservative investor seeking capital preservation",
                allocation={"bonds": 70, "cash": 20, "stocks": 10},
                max_position_size=0.05,
                recommended_sectors=[Sector.UTILITIES, Sector.CONSUMER_STAPLES],
                avoid_sectors=[Sector.TECHNOLOGY, Sector.ENERGY]
            ),
            2: RiskProfile(
                first_name="", last_name="", score=2, level=RiskLevel.LOW,
                description="Conservative investor with minimal risk tolerance",
                allocation={"bonds": 60, "stocks": 30, "cash": 10},
                max_position_size=0.08,
                recommended_sectors=[Sector.UTILITIES, Sector.CONSUMER_STAPLES, Sector.HEALTHCARE],
                avoid_sectors=[Sector.TECHNOLOGY, Sector.ENERGY]
            ),
            3: RiskProfile(
                first_name="", last_name="", score=3, level=RiskLevel.LOW_MODERATE,
                description="Cautious investor with slight growth orientation",
                allocation={"stocks": 40, "bonds": 50, "cash": 10},
                max_position_size=0.10,
                recommended_sectors=[Sector.HEALTHCARE, Sector.CONSUMER_STAPLES, Sector.UTILITIES],
                avoid_sectors=[Sector.ENERGY, Sector.MATERIALS]
            ),
            4: RiskProfile(
                first_name="", last_name="", score=4, level=RiskLevel.MODERATE,
                description="Balanced investor seeking steady growth",
                allocation={"stocks": 50, "bonds": 40, "cash": 10},
                max_position_size=0.12,
                recommended_sectors=[Sector.HEALTHCARE, Sector.FINANCIALS, Sector.CONSUMER_STAPLES],
                avoid_sectors=[Sector.ENERGY]
            ),
            5: RiskProfile(
                first_name="", last_name="", score=5, level=RiskLevel.MODERATE_HIGH,
                description="Growth-oriented investor with moderate risk tolerance",
                allocation={"stocks": 60, "bonds": 30, "cash": 10},
                max_position_size=0.15,
                recommended_sectors=[Sector.TECHNOLOGY, Sector.HEALTHCARE, Sector.FINANCIALS],
                avoid_sectors=[]
            ),
            6: RiskProfile(
                first_name="", last_name="", score=6, level=RiskLevel.HIGH,
                description="Growth investor comfortable with volatility",
                allocation={"stocks": 70, "bonds": 20, "cash": 10},
                max_position_size=0.18,
                recommended_sectors=[Sector.TECHNOLOGY, Sector.CONSUMER_DISCRETIONARY, Sector.FINANCIALS],
                avoid_sectors=[]
            ),
            7: RiskProfile(
                first_name="", last_name="", score=7, level=RiskLevel.HIGH_AGGRESSIVE,
                description="Aggressive growth investor seeking high returns",
                allocation={"stocks": 80, "bonds": 15, "cash": 5},
                max_position_size=0.20,
                recommended_sectors=[Sector.TECHNOLOGY, Sector.ENERGY, Sector.MATERIALS],
                avoid_sectors=[]
            ),
            8: RiskProfile(
                first_name="", last_name="", score=8, level=RiskLevel.AGGRESSIVE,
                description="High-risk investor focused on capital appreciation",
                allocation={"stocks": 85, "bonds": 10, "cash": 5},
                max_position_size=0.25,
                recommended_sectors=[Sector.TECHNOLOGY, Sector.ENERGY, Sector.MATERIALS, Sector.CONSUMER_DISCRETIONARY],
                avoid_sectors=[]
            ),
            9: RiskProfile(
                first_name="", last_name="", score=9, level=RiskLevel.VERY_AGGRESSIVE,
                description="Very aggressive investor willing to accept high volatility",
                allocation={"stocks": 90, "bonds": 5, "cash": 5},
                max_position_size=0.30,
                recommended_sectors=[Sector.TECHNOLOGY, Sector.ENERGY, Sector.MATERIALS],
                avoid_sectors=[]
            ),
            10: RiskProfile(
                first_name="", last_name="", score=10, level=RiskLevel.EXTREME,
                description="Extreme risk investor seeking maximum returns",
                allocation={"stocks": 95, "bonds": 0, "cash": 5},
                max_position_size=0.35,
                recommended_sectors=[Sector.TECHNOLOGY, Sector.ENERGY, Sector.MATERIALS],
                avoid_sectors=[]
            )
        }

    def _initialize_sector_risks(self) -> Dict[Sector, int]:
        """Initialize sector risk ratings (1-10)"""
        return {
            Sector.UTILITIES: 2,
            Sector.CONSUMER_STAPLES: 3,
            Sector.HEALTHCARE: 4,
            Sector.FINANCIALS: 5,
            Sector.INDUSTRIALS: 5,
            Sector.REAL_ESTATE: 6,
            Sector.COMMUNICATION: 6,
            Sector.CONSUMER_DISCRETIONARY: 7,
            Sector.MATERIALS: 8,
            Sector.TECHNOLOGY: 8,
            Sector.ENERGY: 9
        }

    def _initialize_stock_universe(self) -> Dict[str, Dict]:
        """Initialize stock universe with risk ratings"""
        return {
            # Low Risk (1-3)
            "KO": {"name": "Coca-Cola", "sector": Sector.CONSUMER_STAPLES, "risk": 2},
            "PG": {"name": "Procter & Gamble", "sector": Sector.CONSUMER_STAPLES, "risk": 2},
            "JNJ": {"name": "Johnson & Johnson", "sector": Sector.HEALTHCARE, "risk": 3},

            # Medium Risk (4-6)
            "MSFT": {"name": "Microsoft", "sector": Sector.TECHNOLOGY, "risk": 4},
            "AAPL": {"name": "Apple", "sector": Sector.TECHNOLOGY, "risk": 5},
            "JPM": {"name": "JPMorgan Chase", "sector": Sector.FINANCIALS, "risk": 5},

            # High Risk (7-10)
            "TSLA": {"name": "Tesla", "sector": Sector.CONSUMER_DISCRETIONARY, "risk": 9},
            "NVDA": {"name": "NVIDIA", "sector": Sector.TECHNOLOGY, "risk": 8},
            "AMD": {"name": "Advanced Micro Devices", "sector": Sector.TECHNOLOGY, "risk": 8},
        }

    def assess_risk_profile(self, user_data: Dict) -> Tuple[int, RiskProfile]:
        """
        Assess user's risk profile based on 3-question questionnaire

        Args:
            user_data: Dictionary containing:
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

        # Get base profile template
        base_profile = self.risk_profiles.get(final_score, self.risk_profiles[5])

        # Create personalized profile
        personalized_profile = RiskProfile(
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
            score=final_score,
            level=base_profile.level,
            description=base_profile.description,
            allocation=base_profile.allocation.copy(),
            max_position_size=base_profile.max_position_size,
            recommended_sectors=base_profile.recommended_sectors.copy(),
            avoid_sectors=base_profile.avoid_sectors.copy(),
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
        """Get available trading strategies for automated trading"""
        return [
            {
                'name': 'Conservative',
                'description': 'Focus on dividend stocks and blue-chip companies with low volatility',
                'risk_level': 'Low',
                'expected_return': '5-8%'
            },
            {
                'name': 'Balanced Growth',
                'description': 'Mix of growth and value stocks with moderate risk',
                'risk_level': 'Medium',
                'expected_return': '8-12%'
            },
            {
                'name': 'Aggressive Growth',
                'description': 'High-growth stocks and emerging sectors with higher volatility',
                'risk_level': 'High',
                'expected_return': '12-20%'
            },
            {
                'name': 'Tech Focus',
                'description': 'Technology sector concentration with innovation focus',
                'risk_level': 'High',
                'expected_return': '10-25%'
            },
            {
                'name': 'Momentum Trading',
                'description': 'Follow market trends and momentum indicators',
                'risk_level': 'Very High',
                'expected_return': '15-30%'
            }
        ]

    def calculate_portfolio_risk_score(self, positions: List[Dict]) -> Dict:
        """Calculate portfolio-level risk metrics"""
        if not positions:
            return {'score': 0, 'level': 'No Positions', 'diversification': 0}

        total_value = sum(pos.get('market_value', 0) for pos in positions)
        if total_value == 0:
            return {'score': 0, 'level': 'No Value', 'diversification': 0}

        # Calculate weighted risk score
        weighted_risk = 0
        sector_allocation = {}

        for position in positions:
            symbol = position.get('symbol', '')
            market_value = position.get('market_value', 0)
            weight = market_value / total_value

            # Get stock risk rating
            stock_info = self.stock_universe.get(symbol, {'risk': 5, 'sector': Sector.TECHNOLOGY})
            stock_risk = stock_info['risk']
            sector = stock_info['sector']

            weighted_risk += stock_risk * weight

            # Track sector allocation
            sector_name = sector.value if hasattr(sector, 'value') else str(sector)
            sector_allocation[sector_name] = sector_allocation.get(sector_name, 0) + weight

        # Calculate diversification score (lower concentration = higher diversification)
        diversification = 1 - max(sector_allocation.values()) if sector_allocation else 0

        # Risk level mapping
        risk_levels = {
            (1, 2): 'Very Low',
            (2, 3): 'Low',
            (3, 4): 'Low-Moderate',
            (4, 5): 'Moderate',
            (5, 6): 'Moderate-High',
            (6, 7): 'High',
            (7, 8): 'High-Aggressive',
            (8, 9): 'Aggressive',
            (9, 10): 'Very Aggressive',
            (10, 11): 'Extreme'
        }

        risk_level = 'Moderate'
        for (min_risk, max_risk), level in risk_levels.items():
            if min_risk <= weighted_risk < max_risk:
                risk_level = level
                break

        return {
            'score': round(weighted_risk, 1),
            'level': risk_level,
            'diversification': diversification
        }

    def get_stock_recommendations(self, risk_profile: RiskProfile, current_positions: List[str] = None) -> List[StockRecommendation]:
        """Get personalized stock recommendations based on risk profile"""
        recommendations = []
        current_positions = current_positions or []

        # Filter stocks based on risk profile
        suitable_stocks = {}
        for symbol, info in self.stock_universe.items():
            if symbol in current_positions:
                continue

            stock_risk = info['risk']
            stock_sector = info['sector']

            # Check if stock matches risk tolerance
            if stock_risk <= risk_profile.score + 2:  # Allow slight risk tolerance buffer
                # Check if sector is recommended or not avoided
                if (not risk_profile.avoid_sectors or stock_sector not in risk_profile.avoid_sectors):
                    suitable_stocks[symbol] = info

        # Create recommendations
        for symbol, info in list(suitable_stocks.items())[:5]:  # Top 5 recommendations
            strength = min(1.0, (risk_profile.score - info['risk'] + 5) / 10)  # Recommendation strength

            recommendation = StockRecommendation(
                symbol=symbol,
                name=info['name'],
                sector=info['sector'],
                risk_rating=info['risk'],
                recommendation_strength=max(0.1, strength),
                target_allocation=min(risk_profile.max_position_size, 0.1),
                reasoning=f"Matches your {risk_profile.level.name.replace('_', ' ').lower()} risk profile",
                current_price=100.0,  # Placeholder
                target_price=110.0    # Placeholder
            )
            recommendations.append(recommendation)

        return recommendations