import requests
import json
import os
import pandas as pd


URL = "https://api-in21.leadsquared.com/v2/LeadManagement.svc/Leads.RecentlyModified?accessKey=u$rc14713c6132c84aeffb24217ab56efd4&secretKey=021b006097b48fefe3f6815241d178d3de53fece"

params = json.dumps({
    "Parameter": {
        "FromDate": "2024-05-25 10:00:00",
        "ToDate": "2024-05-27 18:30:00"

        
    },
    "Columns": {
        "Include_CSV": "EmailAddress, Phone, CreatedOn"
    },
    "Paging": {
        "PageIndex": 1,
        "PageSize":100
    },
    "Sorting": {
        "ColumnName": "CreatedOn",
        "Direction": "1"
    }
}
)

headers = {"Content-Type":"application/json"}

response = requests.request("POST", URL, headers=headers, data=params)

data = response.json()

class LeadExtractor:
    def __init__(self, data):
        self.data = data
        self.extracted_leads = []

    def extract_leads(self):
        leads = self.data.get("Leads", [])
        for lead in leads:
            lead_info = {}
            for prop in lead.get("LeadPropertyList", []):
                if prop["Attribute"] == "EmailAddress":
                    lead_info["EmailAddress"] = prop["Value"]
                elif prop["Attribute"] == "Phone":
                    lead_info["Phone"] = prop["Value"]
                elif prop["Attribute"] == "CreatedOn":
                    lead_info["CreatedOn"] = prop["Value"]
            if lead_info: 
                self.extracted_leads.append(lead_info)

    def get_json(self):
        return json.dumps(self.extracted_leads, indent=4)
    
lead_data = LeadExtractor(data=data)
lead_data.extract_leads()
lead_result = lead_data.get_json()
lead_dict = json.loads(lead_result)

df = pd.DataFrame(data=lead_dict)

df.to_csv(f"D:/lead/lsq/data/lsq_2527.csv", index=False)

