- dashboard: cymbal_gadgets_2025_kpis
  title: Cymbal Gadgets 2025 KPIs
  layout: newspaper
  preferred_viewer: dashboards
  elements:
  - title: Average Order Value (2025)
    name: Average Order Value (2025)
    model: cymbal_gadgets_boris
    explore: transactions
    type: single_value
    fields: [transactions.average_order_value]
    filters:
      transactions.transaction_year: '2025'
  - title: Gross Margin % (2025)
    name: Gross Margin % (2025)
    model: cymbal_gadgets_boris
    explore: transactions
    type: single_value
    fields: [transactions.gross_margin_percentage]
    filters:
      transactions.transaction_year: '2025'
  - title: Total Gross Profit (2025)
    name: Total Gross Profit (2025)
    model: cymbal_gadgets_boris
    explore: transactions
    type: single_value
    fields: [transactions.total_gross_profit]
    filters:
      transactions.transaction_year: '2025'
