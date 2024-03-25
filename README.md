# Alerts
A Notion API wrapper for storing stock alerts.

Follow the instructions in this post to properly set up the Notion database. You must have the same structure, with the same property assignments. Otherwise, you will need to modify the code:
https://quantasticresearch.com/python/automated-stock-alerts-using-the-notion-api-and-python/

The standard recommendation is to use a virtual environment and set your secret API key and database id as environment variables.

This code works as of March/April 2024.

## Adding Alerts

```py
from alerts import StockAlertDatabase

notion_api_key = "<<< Notion API Key >>>"
notion_database_id = "<<< Notion Database ID >>>"

alerts = StockAlertDatabase(notion_api_key, notion_database_id)

ticker = "XYZ"
alert_date = "2024-03-25"
action = True # True=Buy, False=Sell
reason = "This is a reason."
alerts.add_alert(ticker, alert_date, action, reason)
```

## Get Alerts

```py

from alerts import StockAlertDatabase

notion_api_key = "<<< Notion API Key >>>"
notion_database_id = "<<< Notion Database ID >>>"

alerts_database = StockAlertDatabase(notion_api_key, notion_database_id)

alerts: list = alerts.get_alerts()

for alert in alerts:
    print(alert)

```

## Remove Alerts

To remove an alert you must know the ID of the row in the Notion database. The only way to get this information is to use the get_alerts() function and extract the "id" key's value for the row you want to remove.

```py

from alerts import StockAlertDatabase

notion_api_key = "<<< Notion API Key >>>"
notion_database_id = "<<< Notion Database ID >>>"

alerts_database = StockAlertDatabase(notion_api_key, notion_database_id)

alerts: list = alerts.get_alerts()

# Assume at least 1 row in the Notion database
alert_to_remove = alerts[0]
id_of_alert_to_remove = alert_to_remove["id"]

alerts_database.remove_alert(id_of_alert_to_remove)
```