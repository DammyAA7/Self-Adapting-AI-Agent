"""
Order Optimizer Module
Optimizes order quantities using EOQ and cost minimization
"""

from typing import Dict, Optional, Tuple
import math


class OrderOptimizer:
    """Optimize order quantities to minimize total inventory costs"""

    def __init__(self):
        """Initialize order optimizer with default cost parameters"""
        self.default_holding_cost_rate = 0.25  # 25% of unit cost per year
        self.default_ordering_cost = 50.0  # Cost per order

    def calculate_eoq(self, annual_demand: float, ordering_cost: float,
                     holding_cost: float) -> Dict[str, float]:
        """
        Calculate Economic Order Quantity (EOQ)

        Args:
            annual_demand: Annual demand for the product
            ordering_cost: Cost to place one order
            holding_cost: Annual cost to hold one unit

        Returns:
            Dict with EOQ and related metrics
        """
        if holding_cost <= 0 or annual_demand <= 0:
            return {'eoq': 0, 'error': 'Invalid parameters'}

        # EOQ formula: sqrt((2 * D * S) / H)
        eoq = math.sqrt((2 * annual_demand * ordering_cost) / holding_cost)

        # Calculate related metrics
        number_of_orders = annual_demand / eoq if eoq > 0 else 0
        total_ordering_cost = number_of_orders * ordering_cost
        total_holding_cost = (eoq / 2) * holding_cost
        total_cost = total_ordering_cost + total_holding_cost

        return {
            'eoq': round(eoq, 2),
            'number_of_orders': round(number_of_orders, 2),
            'total_ordering_cost': round(total_ordering_cost, 2),
            'total_holding_cost': round(total_holding_cost, 2),
            'total_annual_cost': round(total_cost, 2),
            'time_between_orders_days': round(365 / number_of_orders, 1) if number_of_orders > 0 else 0
        }

    def optimize_order_quantity(self, product_data: Dict,
                               constraints: Optional[Dict] = None) -> Dict[str, any]:
        """
        Optimize order quantity considering various constraints

        Args:
            product_data: Dict with demand, unit_cost, current_stock, etc.
            constraints: Dict with min_order, max_order, budget, etc.

        Returns:
            Dict with optimized order quantity and justification
        """
        annual_demand = product_data.get('annual_demand', 0)
        unit_cost = product_data.get('unit_cost', 0)
        ordering_cost = product_data.get('ordering_cost', self.default_ordering_cost)

        # Calculate holding cost
        holding_cost = unit_cost * self.default_holding_cost_rate

        # Calculate EOQ
        eoq_result = self.calculate_eoq(annual_demand, ordering_cost, holding_cost)
        optimal_qty = eoq_result['eoq']

        # Apply constraints
        if constraints:
            min_order = constraints.get('min_order_quantity', 0)
            max_order = constraints.get('max_order_quantity', float('inf'))
            budget = constraints.get('budget', float('inf'))

            if optimal_qty < min_order:
                optimal_qty = min_order
                justification = f'Increased to minimum order quantity: {min_order}'
            elif optimal_qty > max_order:
                optimal_qty = max_order
                justification = f'Reduced to maximum order quantity: {max_order}'
            elif optimal_qty * unit_cost > budget:
                optimal_qty = budget / unit_cost
                justification = f'Reduced to fit budget constraint'
            else:
                justification = 'EOQ calculation optimal'
        else:
            justification = 'EOQ calculation without constraints'

        return {
            'optimal_quantity': round(optimal_qty, 0),
            'eoq': eoq_result['eoq'],
            'justification': justification,
            'estimated_annual_cost': eoq_result['total_annual_cost'],
            'order_frequency_days': eoq_result['time_between_orders_days']
        }

    def minimize_costs(self, demand: float, order_quantity: float,
                      unit_cost: float, ordering_cost: float = None) -> Dict[str, float]:
        """
        Calculate total costs for a given order quantity

        Args:
            demand: Annual demand
            order_quantity: Proposed order quantity
            unit_cost: Cost per unit
            ordering_cost: Cost per order

        Returns:
            Dict with cost breakdown
        """
        if ordering_cost is None:
            ordering_cost = self.default_ordering_cost

        holding_cost_per_unit = unit_cost * self.default_holding_cost_rate

        # Calculate costs
        number_of_orders = demand / order_quantity if order_quantity > 0 else 0
        annual_ordering_cost = number_of_orders * ordering_cost
        average_inventory = order_quantity / 2
        annual_holding_cost = average_inventory * holding_cost_per_unit
        annual_purchase_cost = demand * unit_cost
        total_cost = annual_ordering_cost + annual_holding_cost + annual_purchase_cost

        return {
            'ordering_cost': round(annual_ordering_cost, 2),
            'holding_cost': round(annual_holding_cost, 2),
            'purchase_cost': round(annual_purchase_cost, 2),
            'total_cost': round(total_cost, 2),
            'cost_per_unit': round(total_cost / demand, 2) if demand > 0 else 0
        }

    def calculate_reorder_point(self, daily_demand: float, lead_time_days: int,
                               safety_stock: float = 0) -> Dict[str, float]:
        """
        Calculate reorder point for inventory

        Args:
            daily_demand: Average daily demand
            lead_time_days: Supplier lead time in days
            safety_stock: Additional safety stock quantity

        Returns:
            Dict with reorder point and safety information
        """
        reorder_point = (daily_demand * lead_time_days) + safety_stock

        return {
            'reorder_point': round(reorder_point, 2),
            'lead_time_demand': round(daily_demand * lead_time_days, 2),
            'safety_stock': safety_stock,
            'lead_time_days': lead_time_days
        }

    def suggest_safety_stock(self, daily_demand: float, demand_variability: float,
                            lead_time_days: int, service_level: float = 0.95) -> float:
        """
        Suggest safety stock level based on demand variability

        Args:
            daily_demand: Average daily demand
            demand_variability: Standard deviation of demand
            lead_time_days: Lead time in days
            service_level: Target service level (0-1)

        Returns:
            Suggested safety stock quantity
        """
        # Simplified safety stock calculation
        # Z-score for 95% service level is approximately 1.65
        z_scores = {0.90: 1.28, 0.95: 1.65, 0.99: 2.33}
        z = z_scores.get(service_level, 1.65)

        safety_stock = z * demand_variability * math.sqrt(lead_time_days)
        return round(safety_stock, 2)
