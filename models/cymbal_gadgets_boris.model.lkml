connection: "cymbal_gadgets"

include: "/views/*"
include: "/dashboards/*"

datagroup: cymbal_gadgets_default_datagroup {
  max_cache_age: "1 hour"
}

persist_with: cymbal_gadgets_default_datagroup

explore: transactions {
  label: "🛍️ Cymbal Gadgets: Transactions & Sales"
  description: "Core explore for analyzing transactions, marketing impact, and product reviews."

  join: product_reviews {
    sql_on: ${transactions.productid} = ${product_reviews.productid} ;;
    relationship: many_to_many
  }
  join: marketing_campaign_impact {
    sql_on: ${transactions.salesid} = ${marketing_campaign_impact.salesid} ;;
    relationship: one_to_many
  }
}
