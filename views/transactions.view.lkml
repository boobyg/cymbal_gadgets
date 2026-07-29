view: transactions {
  sql_table_name: `looker-private-demo.cymbal_gadgets.transactions` ;;

  # --- Hidden IDs ---
  dimension: salesid {
    primary_key: yes
    hidden: yes
    type: number
    sql: ${TABLE}.salesid ;;
  }
  dimension: customerid {
    hidden: yes
    type: number
    sql: ${TABLE}.customerid ;;
  }
  dimension: orderid {
    hidden: yes
    type: string
    sql: ${TABLE}.orderid ;;
  }
  dimension: productid {
    hidden: yes
    type: number
    sql: ${TABLE}.productid ;;
  }
  dimension: storeid {
    hidden: yes
    type: number
    sql: ${TABLE}.storeid ;;
    description:  "in Looker IDE"
  }

  # --- Date & Time ---
  dimension_group: transaction {
    label: "Transaction"
    type: time
    timeframes: [raw, date, week, week_of_year, month, month_name, quarter, year]
    convert_tz: no
    datatype: date
    sql: ${TABLE}.transaction_date ;;
  }
  dimension: isweekend {
    group_label: "Transaction Dates"
    label: "Is Weekend?"
    type: yesno
    sql: ${TABLE}.isweekend ;;
  }

  # --- Customer Info (Grouped) ---
  dimension: firstname {
    hidden: yes
    type: string
    sql: ${TABLE}.firstname ;;
  }
  dimension: lastname {
    hidden: yes
    type: string
    sql: ${TABLE}.lastname ;;
  }

  # Dimension: Full Name
  dimension: customer_name {
    group_label: "Customer Info"
    label: "Customer Name"
    description: "Full name of the customer."
    type: string
    sql: CONCAT(${firstname}, ' ', ${lastname}) ;;
  }
  dimension: customer_city {
    group_label: "Customer Info"
    label: "Customer City"
    type: string
    sql: ${TABLE}.customer_city ;;
  }
  dimension: customer_country {
    group_label: "Customer Info"
    label: "Customer Country"
    type: string
    sql: ${TABLE}.customer_country ;;
    map_layer_name: countries
  }
  dimension: loyaltytier {
    group_label: "Customer Info"
    label: "Loyalty Tier"
    type: string
    sql: ${TABLE}.loyaltytier ;;
  }
  dimension_group: customer_registrationdate {
    group_label: "Customer Info"
    label: "Customer Registration"
    type: time
    timeframes: [date, month, year]
    convert_tz: no
    datatype: date
    sql: ${TABLE}.customer_registrationdate ;;
  }

  # --- Store Info (Grouped) ---
  dimension: storename {
    group_label: "Store Info"
    label: "Store Name"
    type: string
    sql: ${TABLE}.storename ;;
  }
  dimension: store_city {
    group_label: "Store Info"
    label: "Store City"
    type: string
    sql: ${TABLE}.store_city ;;
  }
  dimension: store_country {
    group_label: "Store Info"
    label: "Store Country"
    type: string
    sql: ${TABLE}.store_country ;;
  }
  dimension: store_region {
    group_label: "Store Info"
    label: "Store Region"
    type: string
    sql: ${TABLE}.store_region ;;
  }
  dimension: latitude {
    hidden: yes
    type: number
    sql: ${TABLE}.latitude ;;
  }
  dimension: longitude {
    hidden: yes
    type: number
    sql: ${TABLE}.longitude ;;
  }

  # Dimension: Location Mapping
  dimension: store_location {
    group_label: "Store Info"
    label: "Store Map Location"
    type: location
    sql_latitude: ${latitude} ;;
    sql_longitude: ${longitude} ;;
  }

  # --- Product & Order Info (Grouped) ---
  dimension: brand {
    group_label: "Product Info"
    label: "Brand"
    type: string
    sql: ${TABLE}.brand ;;
  }
  dimension: category {
    group_label: "Product Info"
    label: "Category"
    type: string
    sql: ${TABLE}.category ;;
  }
  dimension: productname {
    group_label: "Product Info"
    label: "Product Name"
    type: string
    sql: ${TABLE}.productname ;;
  }
  dimension: saleschannelname {
    group_label: "Order Info"
    label: "Sales Channel"
    type: string
    sql: ${TABLE}.saleschannelname ;;
  }
  dimension: paymenttypename {
    group_label: "Order Info"
    label: "Payment Type"
    type: string
    sql: ${TABLE}.paymenttypename ;;
  }

  # --- Financial Dimensions (Hidden from UI, used for Measures) ---
  dimension: product_cost {
    hidden: yes
    type: number
    sql: ${TABLE}.product_cost ;;
  }
  dimension: product_master_price {
    hidden: yes
    type: number
    sql: ${TABLE}.product_master_price ;;
  }
  dimension: quantity {
    hidden: yes
    type: number
    sql: ${TABLE}.quantity ;;
  }
  dimension: totalprice {
    hidden: yes
    type: number
    sql: ${TABLE}.totalprice ;;
  }
  dimension: discountamount {
    hidden: yes
    type: number
    sql: ${TABLE}.discountamount ;;
  }
  dimension: shippingcost {
    hidden: yes
    type: number
    sql: ${TABLE}.shippingcost ;;
  }
  dimension: taxamount {
    hidden: yes
    type: number
    sql: ${TABLE}.taxamount ;;
  }

  # Gross Profit
  dimension: gross_profit {
    group_label: "Financials"
    label: "Gross Profit"
    description: "Total Price minus Product Cost"
    type: number
    value_format_name: usd
    sql: ${totalprice} - (${product_cost} * ${quantity}) ;;
  }

  # --- Measures ---
  measure: count {
    label: "Total Transactions"
    type: count
    drill_fields: [transaction_details*]
  }

  measure: total_revenue {
    label: "Total Revenue"
    description: "Sum of total price for all transactions."
    type: sum
    sql: ${totalprice} ;;
    value_format_name: usd_0
    drill_fields: [transaction_details*]
  }

  measure: total_gross_profit {
    label: "Total Gross Profit"
    description: "Sum of gross profit across all transactions."
    type: sum
    sql: ${gross_profit} ;;
    value_format_name: usd_0
    drill_fields: [transaction_details*]
  }

  measure: total_quantity_sold {
    label: "Total Quantity Sold"
    type: sum
    sql: ${quantity} ;;
  }

  measure: average_order_value {
    label: "Average Order Value (AOV)"
    description: "Average revenue generated per transaction."
    type: average
    sql: ${totalprice} ;;
    value_format_name: usd
  }

  measure: gross_margin_percentage {
    label: "Gross Margin %"
    description: "Total Gross Profit divided by Total Revenue."
    type: number
    sql: 1.0 * ${total_gross_profit} / NULLIF(${total_revenue}, 0) ;;
    value_format_name: percent_1
  }

  measure: unique_customers {
    label: "Total Unique Customers"
    type: count_distinct
    sql: ${customerid} ;;
  }

  dimension: shipment_status {
    label: "Shipment status"
    sql: ${TABLE}.shipment_status;;
  }
  dimension: shippingmethod {
    label: "Shipping method"
    sql: ${TABLE}.shipmentmethod;;
  }

  dimension: distribution_center_city {
    label: "Distribution Center"
    sql: ${TABLE}.distribution_center_city ;;
  }

  measure: delayed_order_count {
    label: "Cancelled Order Count"
    type: count
    filters: [shipment_status: "Delayed"]
  }

  # ----- Sets of fields for drilling ------
  set: transaction_details {
    fields: [
      transaction_date,
      customer_name,
      storename,
      productname,
      category,
      saleschannelname,
      quantity,
      total_revenue
    ]
  }
}
