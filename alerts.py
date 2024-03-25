import requests
from datetime import date
import json

class StockAlertDatabase:
    def __init__(self, api_key: str, database_id: str):
        """
        Parameters:
        -----------
        api_key: Notion API Key
        database_id: ID of Notion database
        """
        self._api_key: str = api_key
        self._database_id: str = database_id

        self._headers = {
            "Authorization": "Bearer " + self._api_key,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def add_alert(self, ticker: str, alert_date: str = str(date.today()), action: bool = True, reason="New stock alert!"):
        # Set action string
        action_string = "Sell"
        if action:
            action_string = "Buy"
        
        # Setup payload
        payload = {
            "parent": {"database_id": self._database_id},
            "properties": {
                "Ticker": {"title": [{"text": {"content": ticker}}]},
                "Action": {"select":{"name": action_string}},
                "Date": {"date": {"start": alert_date}},
                "Reason": {"rich_text": [{"text":{"content": reason}}]}
            }
        }
        try:
            data = json.dumps(payload)
            url = "https://api.notion.com/v1/pages"
            requests.post(url, headers=self._headers, data=data)
        except Exception as e:
            return False
        return True
    
    def get_alerts(self) -> list:
        """
        Retrieves the rows in the database.
        """
        readUrl: str = f"https://api.notion.com/v1/databases/{self._database_id}/query"
        res: requests.Response = requests.post(readUrl, headers=self._headers)
        json_res: dict = res.json()
        results = json_res['results']

        if len(results) != 0:
            alert_list = []
            for result in results:
                alert = {
                    "id":f"{result["id"]}",
                    "ticker":f"{result['properties']['Ticker']['title'][0]['text']['content']}",
                    "action":f"{result['properties']['Action']['select']['name']}",
                    "date":f"{result['properties']['Date']['date']['start']}",
                    "reason":f"{result['properties']['Reason']['rich_text'][0]['text']['content']}"
                }
                alert_list.append(alert)

            return alert_list
        
        return []
    
    def remove_alert(self, alert_id: str):
        """
        Deletes the row associated with alarm_id.

        The alert_id is equal to the row id in the database table.
        """
        url: str = f"https://api.notion.com/v1/blocks/{alert_id}"
        try:
            res: requests.Response = requests.delete(url, headers=self._headers)
            json_res: dict = res.json()
        except Exception as e:
            print(e)
            return False
        
        if len(json_res) != 0:
            return True
        
        return False
