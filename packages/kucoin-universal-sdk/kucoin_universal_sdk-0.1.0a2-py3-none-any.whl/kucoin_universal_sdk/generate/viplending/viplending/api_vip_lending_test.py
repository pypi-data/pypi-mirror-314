import unittest
from .model_get_account_detail_resp import GetAccountDetailResp
from .model_get_accounts_resp import GetAccountsResp
from kucoin_universal_sdk.model.common import RestResponse


class VIPLendingAPITest(unittest.TestCase):

    def test_get_accounts_req_model(self):
        """
       get_accounts
       Get Accounts
       /api/v1/otc-loan/accounts
       """

    def test_get_accounts_resp_model(self):
        """
        get_accounts
        Get Accounts
        /api/v1/otc-loan/accounts
        """
        data = "\n{\n    \"code\": \"200000\",\n    \"data\": [{\n        \"uid\": \"1260004199\",\n        \"marginCcy\": \"USDT\",\n        \"marginQty\": \"900\",\n        \"marginFactor\": \"0.9000000000\",\n        \"accountType\": \"TRADE\",\n        \"isParent\": true\n    }]\n}"
        common_response = RestResponse.from_json(data)
        resp = GetAccountsResp.from_dict(common_response.data)

    def test_get_account_detail_req_model(self):
        """
       get_account_detail
       Get Account Detail
       /api/v1/otc-loan/loan
       """

    def test_get_account_detail_resp_model(self):
        """
        get_account_detail
        Get Account Detail
        /api/v1/otc-loan/loan
        """
        data = "{\n    \"code\": \"200000\",\n    \"data\": {\n        \"parentUid\": \"1260004199\",\n        \"orders\": [{\n            \"orderId\": \"671a2be815f4140007a588e1\",\n            \"principal\": \"100\",\n            \"interest\": \"0\",\n            \"currency\": \"USDT\"\n        }],\n        \"ltv\": {\n            \"transferLtv\": \"0.6000\",\n            \"onlyClosePosLtv\": \"0.7500\",\n            \"delayedLiquidationLtv\": \"0.7500\",\n            \"instantLiquidationLtv\": \"0.8000\",\n            \"currentLtv\": \"0.1111\"\n        },\n        \"totalMarginAmount\": \"900.00000000\",\n        \"transferMarginAmount\": \"166.66666666\",\n        \"margins\": [{\n            \"marginCcy\": \"USDT\",\n            \"marginQty\": \"1000.00000000\",\n            \"marginFactor\": \"0.9000000000\"\n        }]\n    }\n}"
        common_response = RestResponse.from_json(data)
        resp = GetAccountDetailResp.from_dict(common_response.data)
