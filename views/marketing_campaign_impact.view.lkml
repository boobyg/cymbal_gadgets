view: marketing_campaign_impact {
  sql_table_name: `looker-private-demo.cymbal_gadgets.marketing_campaign_impact` ;;

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
  dimension: productid {
    hidden: yes
    type: number
    sql: ${TABLE}.productid ;;
  }

  # --- Dimensions ---
  dimension: campaignname {
    group_label: "Campaign Details"
    label: "Campaign Name"
    description: "The name of the marketing campaign."
    type: string
    sql: ${TABLE}.campaignname ;;
  }
  dimension: eventname {
    group_label: "Campaign Details"
    label: "Event Name"
    description: "The specific event within the campaign (e.g., 'Email Open', 'Ad Click')."
    type: string
    sql: ${TABLE}.eventname ;;
  }
  dimension: durationdays {
    group_label: "Campaign Details"
    label: "Duration (Days)"
    type: number
    sql: ${TABLE}.durationdays ;;
  }
  dimension_group: transaction {
    label: "Campaign Transaction"
    type: time
    timeframes: [raw, date, week, month, quarter, year]
    convert_tz: no
    datatype: date
    sql: ${TABLE}.transaction_date ;;
  }

  # --- Metrics (Base) ---
  dimension: campaign_impact {
    hidden: yes
    type: number
    sql: ${TABLE}.campaign_impact ;;
  }
  dimension: event_impact {
    hidden: yes
    type: number
    sql: ${TABLE}.event_impact ;;
  }
  dimension: totalprice {
    description: "in VSCode The total price of the transaction associated with the campaign event."
    hidden: no
    type: number
    sql: ${TABLE}.totalprice ;;
  }

  # --- Measures ---
  measure: count {
    label: "Total Campaign Events"
    type: count
    drill_fields: [campaign_details*]
  }

  measure: total_campaign_impact {
    label: "Total Campaign Impact"
    description: "The sum of the campaign impact metric across all campaigns."
    type: sum
    sql: ${campaign_impact} ;;
    value_format_name: decimal_2
  }

  measure: total_event_impact {
    label: "Total Event Impact"
    description: "The sum of the event impact metric across all campaigns."
    type: sum
    sql: ${event_impact} ;;
    value_format_name: decimal_2
  }

  measure: total_sales {
    label: "Total Sales"
    description: "The sum of all sales."
    type: sum
    sql: ${totalprice} ;;
    value_format_name: usd
  }

  measure: average_duration_days {
    label: "Average Campaign Duration"
    type: average
    sql: ${durationdays} ;;
    value_format_name: decimal_1
  }

  set: campaign_details {
    fields: [campaignname, eventname, durationdays, total_campaign_impact]
  }
}
