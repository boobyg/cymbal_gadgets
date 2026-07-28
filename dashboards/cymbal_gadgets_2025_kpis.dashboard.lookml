- dashboard: cymbal_gadgets_2025_kpis
  title: Cymbal Gadgets 2025 KPIs
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
  - title: Average Order Value
    name: Average Order Value
    model: cymbal_gadgets_boris
    explore: transactions
    type: single_value
    fields: [transactions.average_order_value]
    listen:
      transaction_date_range: transactions.transaction_date
    row: 0
    col: 0
    width: 8
    height: 4

  - title: Gross Margin %
    name: Gross Margin %
    model: cymbal_gadgets_boris
    explore: transactions
    type: single_value
    fields: [transactions.gross_margin_percentage]
    listen:
      transaction_date_range: transactions.transaction_date
    row: 0
    col: 8
    width: 8
    height: 4

  - title: Total Gross Profit
    name: Total Gross Profit
    model: cymbal_gadgets_boris
    explore: transactions
    type: single_value
    fields: [transactions.total_gross_profit]
    listen:
      transaction_date_range: transactions.transaction_date
    row: 0
    col: 16
    width: 8
    height: 4

  - title: Total Revenue by Category
    name: Total Revenue by Category
    model: cymbal_gadgets_boris
    explore: transactions
    type: looker_bar
    fields: [transactions.category, transactions.total_revenue]
    listen:
      transaction_date_range: transactions.transaction_date
    sorts: [transactions.total_revenue desc]
    row: 4
    col: 0
    width: 12
    height: 8

  - title: Transactions by Sales Channel
    name: Transactions by Sales Channel
    model: cymbal_gadgets_boris
    explore: transactions
    type: looker_pie
    fields: [transactions.saleschannelname, transactions.count]
    listen:
      transaction_date_range: transactions.transaction_date
    row: 4
    col: 12
    width: 12
    height: 8

  - title: Average Order Value by Month
    name: Average Order Value by Month
    model: cymbal_gadgets_boris
    explore: transactions
    type: looker_column
    fields: [transactions.transaction_month, transactions.average_order_value]
    listen:
      transaction_date_range: transactions.transaction_date
    sorts: [transactions.transaction_month asc]
    row: 12
    col: 0
    width: 12
    height: 8

  - title: Gross Margin % by Month
    name: Gross Margin % by Month
    model: cymbal_gadgets_boris
    explore: transactions
    type: looker_column
    fields: [transactions.transaction_month, transactions.gross_margin_percentage]
    listen:
      transaction_date_range: transactions.transaction_date
    sorts: [transactions.transaction_month asc]
    row: 12
    col: 12
    width: 12
    height: 8

  - title: Total Gross Profit by Month
    name: Total Gross Profit by Month
    model: cymbal_gadgets_boris
    explore: transactions
    type: looker_column
    fields: [transactions.transaction_month, transactions.total_gross_profit]
    listen:
      transaction_date_range: transactions.transaction_date
    sorts: [transactions.transaction_month asc]
    row: 20
    col: 0
    width: 12
    height: 8

  - title: Total Revenue by Month
    name: Total Revenue by Month
    model: cymbal_gadgets_boris
    explore: transactions
    type: looker_column
    fields: [transactions.transaction_month, transactions.total_revenue]
    listen:
      transaction_date_range: transactions.transaction_date
    sorts: [transactions.transaction_month asc]
    row: 20
    col: 12
    width: 12
    height: 8

  - title: Transactions by Month
    name: Transactions by Month
    model: cymbal_gadgets_boris
    explore: transactions
    type: looker_column
    fields: [transactions.transaction_month, transactions.count]
    listen:
      transaction_date_range: transactions.transaction_date
    sorts: [transactions.transaction_month asc]
    row: 28
    col: 0
    width: 24
    height: 8
