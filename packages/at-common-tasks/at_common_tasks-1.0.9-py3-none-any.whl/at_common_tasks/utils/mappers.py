from at_common_models.stock.financials.base_models import BaseBalanceSheetStatementModel, BaseCashflowStatementModel, BaseIncomeStatementModel

def map_income_statement(statement: BaseIncomeStatementModel):
    """Maps income statement model to dictionary format.
    
    Args:
        statement: Income statement model instance (Annual or Quarterly)
        
    Returns:
        dict: Mapped income statement data
    """
    return {
        "fiscal_date_ending": statement.fiscal_date_ending,
        "reported_currency": statement.reported_currency,
        # Revenue and direct costs
        "revenue": statement.revenue,
        "cost_of_revenue": statement.cost_of_revenue,
        "gross_profit": statement.gross_profit,
        "gross_profit_ratio": statement.gross_profit_ratio,
        # Operating expenses breakdown
        "research_and_development_expenses": statement.research_and_development_expenses,
        "general_and_administrative_expenses": statement.general_and_administrative_expenses,
        "selling_and_marketing_expenses": statement.selling_and_marketing_expenses,
        "selling_general_and_administrative_expenses": statement.selling_general_and_administrative_expenses,
        "other_expenses": statement.other_expenses,
        "operating_expenses": statement.operating_expenses,
        "cost_and_expenses": statement.cost_and_expenses,
        # Interest and depreciation
        "interest_income": statement.interest_income,
        "interest_expense": statement.interest_expense,
        "depreciation_and_amortization": statement.depreciation_and_amortization,
        # Profitability metrics
        "ebitda": statement.ebitda,
        "operating_income": statement.operating_income,
        "total_other_income_expenses_net": statement.total_other_income_expenses_net,
        "income_before_tax": statement.income_before_tax,
        "income_tax_expense": statement.income_tax_expense,
        "net_income": statement.net_income,
        # Per share metrics
        "eps": statement.eps,
        "eps_diluted": statement.eps_diluted
    }

def map_balance_sheet_statement(statement: BaseBalanceSheetStatementModel):
    """Maps balance sheet model to dictionary format.
    
    Args:
        statement: Balance sheet model instance (Annual or Quarterly)
        
    Returns:
        dict: Mapped balance sheet data
    """
    return {
        "fiscal_date_ending": statement.fiscal_date_ending,
        "reported_currency": statement.reported_currency,
        # Current Assets
        "cash_and_cash_equivalents": statement.cash_and_cash_equivalents,
        "short_term_investments": statement.short_term_investments,
        "cash_and_short_term_investments": statement.cash_and_short_term_investments,
        "net_receivables": statement.net_receivables,
        "inventory": statement.inventory,
        "other_current_assets": statement.other_current_assets,
        "total_current_assets": statement.total_current_assets,
        
        # Non-Current Assets
        "property_plant_equipment_net": statement.property_plant_equipment_net,
        "goodwill": statement.goodwill,
        "intangible_assets": statement.intangible_assets,
        "goodwill_and_intangible_assets": statement.goodwill_and_intangible_assets,
        "long_term_investments": statement.long_term_investments,
        "tax_assets": statement.tax_assets,
        "other_non_current_assets": statement.other_non_current_assets,
        "total_non_current_assets": statement.total_non_current_assets,
        
        # Asset Totals
        "other_assets": statement.other_assets,
        "total_assets": statement.total_assets,
        
        # Current Liabilities
        "account_payables": statement.account_payables,
        "short_term_debt": statement.short_term_debt,
        "tax_payables": statement.tax_payables,
        "deferred_revenue": statement.deferred_revenue,
        "other_current_liabilities": statement.other_current_liabilities,
        "total_current_liabilities": statement.total_current_liabilities,
        
        # Non-Current Liabilities
        "long_term_debt": statement.long_term_debt,
        "deferred_revenue_non_current": statement.deferred_revenue_non_current,
        "deferred_tax_liabilities_non_current": statement.deferred_tax_liabilities_non_current,
        "other_non_current_liabilities": statement.other_non_current_liabilities,
        "total_non_current_liabilities": statement.total_non_current_liabilities,
        
        # Liability Totals
        "other_liabilities": statement.other_liabilities,
        "capital_lease_obligations": statement.capital_lease_obligations,
        "total_liabilities": statement.total_liabilities,
        
        # Stockholders' Equity
        "preferred_stock": statement.preferred_stock,
        "common_stock": statement.common_stock,
        "retained_earnings": statement.retained_earnings,
        "accumulated_other_comprehensive_income_loss": statement.accumulated_other_comprehensive_income_loss,
        "other_total_stockholders_equity": statement.other_total_stockholders_equity,
        "total_stockholders_equity": statement.total_stockholders_equity,
        "total_equity": statement.total_equity,
        
        # Balance Sheet Totals
        "total_liabilities_and_stockholders_equity": statement.total_liabilities_and_stockholders_equity,
        "minority_interest": statement.minority_interest,
        "total_liabilities_and_total_equity": statement.total_liabilities_and_total_equity,
        
        # Additional Financial Metrics
        "total_investments": statement.total_investments,
        "total_debt": statement.total_debt,
        "net_debt": statement.net_debt
    }

def map_cashflow_statement(statement: BaseCashflowStatementModel):
    """Maps cash flow statement model to dictionary format.
    
    Args:
        statement: Cash flow statement model instance (Annual or Quarterly)
        
    Returns:
        dict: Mapped cash flow statement data
    """
    return {
        "fiscal_date_ending": statement.fiscal_date_ending,
        "reported_currency": statement.reported_currency,
        
        # Operating Activities - Core Operations
        "net_income": statement.net_income,
        "depreciation_and_amortization": statement.depreciation_and_amortization,
        "deferred_income_tax": statement.deferred_income_tax,
        "stock_based_compensation": statement.stock_based_compensation,
        
        # Operating Activities - Working Capital Changes
        "change_in_working_capital": statement.change_in_working_capital,
        "accounts_receivables": statement.accounts_receivables,
        "inventory": statement.inventory,
        "accounts_payables": statement.accounts_payables,
        "other_working_capital": statement.other_working_capital,
        "other_non_cash_items": statement.other_non_cash_items,
        "net_cash_provided_by_operating_activities": statement.net_cash_provided_by_operating_activities,
        
        # Investing Activities
        "investments_in_property_plant_and_equipment": statement.investments_in_property_plant_and_equipment,
        "acquisitions_net": statement.acquisitions_net,
        "purchases_of_investments": statement.purchases_of_investments,
        "sales_maturities_of_investments": statement.sales_maturities_of_investments,
        "other_investing_activities": statement.other_investing_activities,
        "net_cash_used_for_investing_activities": statement.net_cash_used_for_investing_activities,
        
        # Financing Activities
        "debt_repayment": statement.debt_repayment,
        "common_stock_issued": statement.common_stock_issued,
        "common_stock_repurchased": statement.common_stock_repurchased,
        "dividends_paid": statement.dividends_paid,
        "other_financing_activities": statement.other_financing_activities,
        "net_cash_used_provided_by_financing_activities": statement.net_cash_used_provided_by_financing_activities,
        
        # Cash Position and Summary Metrics
        "effect_of_forex_changes_on_cash": statement.effect_of_forex_changes_on_cash,
        "net_change_in_cash": statement.net_change_in_cash,
        "cash_at_end_of_period": statement.cash_at_end_of_period,
        "cash_at_beginning_of_period": statement.cash_at_beginning_of_period,
        "operating_cash_flow": statement.operating_cash_flow,
        "capital_expenditure": statement.capital_expenditure,
        "free_cash_flow": statement.free_cash_flow
    }

