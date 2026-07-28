- dashboard: powerbi_replication
  title: Power BI Dashboard Replication
  layout: newspaper
  preferred_viewer: dashboards
  filters:
  - name: transaction_date_range
    title: Transaction Date Range
    type: date_filter
    default_value: '2025'
    allow_multiple_values: true
    required: false
    ui_config:
      type: advanced
      display: popover

  elements:
  - title: Transactions by Country
    name: Transactions by Country
    model: cymbal_gadgets_boris
    explore: transactions
    type: looker_pie
    fields: [transactions.store_country, transactions.count]
    listen:
      transaction_date_range: transactions.transaction_date
    row: 0
    col: 0
    width: 12
    height: 8

  - title: Gross Profit by Brand and Category
    name: Gross Profit by Brand and Category
    model: cymbal_gadgets_boris
    explore: transactions
    type: looker_bar
    fields: [transactions.brand, transactions.category, transactions.total_gross_profit]
    listen:
      transaction_date_range: transactions.transaction_date
    sorts: [transactions.category asc, transactions.brand asc]
    row: 0
    col: 12
    width: 12
    height: 8
