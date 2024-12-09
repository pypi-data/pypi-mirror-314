## PYTHON - NICEPAY

NICEPAY ❤️ Python!

This is the Official Python API client / library for NICEPAY Payment API. Visit [Python Library](https://github.com/nicepay-dev/python-nicepay).
More information about the product and see documentation at [NICEPAY Docs](https://docs.nicepay.co.id/) for more technical details.

This library provides access to Nicepay BI SNAP and V2 APIs.
- `SNAP`
- `v2 Enterprise`
- `v2 professional`

## 1. Installation
You can clone or [download](https://github.com/nicepay-dev/python-nicepay) our source code, then import the folder manually into your project.
#####
Clone Repository :
```bash
git clone https://github.com/nicepay-dev/python-nicepay.git
```

#### 1.1 Requirement 
**Language :** 
Python `v.3.11.9`

**Library :**

- `pycryptodome`
- `requests`


## 2. Usage
Get your credentials from [Nicepay Dashboard](http://103.20.51.40:8012/logIn.do)
initialize Nicepay config

#### 2.1 Client Initialization and Configuration

Credentials used here are for testing purposes only [snap]
```bash
_CLIENT_KEY = "IONPAYTEST"
_PRIVATE_KEY = "MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAInJe1G22R2fMchIE6BjtYRqyMj6lurP/zq6vy79WaiGKt0Fxs4q3Ab4ifmOXd97ynS5f0JRfIqakXDcV/e2rx9bFdsS2HORY7o5At7D5E3tkyNM9smI/7dk8d3O0fyeZyrmPMySghzgkR3oMEDW1TCD5q63Hh/oq0LKZ/4Jjcb9AgMBAAECgYA4Boz2NPsjaE+9uFECrohoR2NNFVe4Msr8/mIuoSWLuMJFDMxBmHvO+dBggNr6vEMeIy7zsF6LnT32PiImv0mFRY5fRD5iLAAlIdh8ux9NXDIHgyera/PW4nyMaz2uC67MRm7uhCTKfDAJK7LXqrNVDlIBFdweH5uzmrPBn77foQJBAMPCnCzR9vIfqbk7gQaA0hVnXL3qBQPMmHaeIk0BMAfXTVq37PUfryo+80XXgEP1mN/e7f10GDUPFiVw6Wfwz38CQQC0L+xoxraftGnwFcVN1cK/MwqGS+DYNXnddo7Hu3+RShUjCz5E5NzVWH5yHu0E0Zt3sdYD2t7u7HSr9wn96OeDAkEApzB6eb0JD1kDd3PeilNTGXyhtIE9rzT5sbT0zpeJEelL44LaGa/pxkblNm0K2v/ShMC8uY6Bbi9oVqnMbj04uQJAJDIgTmfkla5bPZRR/zG6nkf1jEa/0w7i/R7szaiXlqsIFfMTPimvRtgxBmG6ASbOETxTHpEgCWTMhyLoCe54WwJATmPDSXk4APUQNvX5rr5OSfGWEOo67cKBvp5Wst+tpvc6AbIJeiRFlKF4fXYTb6HtiuulgwQNePuvlzlt2Q8hqQ=="
_CLIENT_SECRET = "33F49GnCMS1mFYlGXisbUDzVf2ATWCl9k3R++d5hDd3Frmuos/XLx8XhXpe+LDYAbpGKZYSwtlyyLOtS/8aD7A=="
```

#### 2.2 Request for Access-Token
```bash
from data.builder.snap import builderAccessToken
from service.snapService import SnapService

class testAccessToken:
    bodyCreateToken = (
        builderAccessToken.BuildAccessToken()
        .setGrantType("client_credentials")
        .setAdditionalInfo("")
        .build()
    )

Result = SnapService.serviceOAUTH(bodyCreateToken.jsonAccessToken())
```
Here's the result 
```bash
AccessToken : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJJT05QQVlURVNUIiwiaXNzIjoiTklDRVBBWSIsIm5hbWUiOiJCRElOIiwiZXhwIjoiMjAyNC0xMS0xMlQyMDowNTo1NFoifQ==.RfeDzCn7sk5VT54f8NTPnbbeQvaPmQg6wtLWXIbmBCI=
```

#### 2.3 Request for Generate VA (i.e. Virtual Account)
```bash
from data.builder.snap import builderVirtualAccount
from data.builder.snap import builderAccessToken
from constants.constantsEndpoint import ConstantsEndpoints
from service.snapService import SnapService
from util.utilLogging import Log

log = Log()

class testVirtualAccount:
    bodyCreateToken = (
        builderAccessToken.BuildAccessToken()
        .setGrantType("client_credentials")
        .setAdditionalInfo("")
        .build()
    )

    totalAmount = {"value": "10000.00",
                   "currency": "IDR"
                   }

    additionalInfo = {"bankCd": "BRIN",
                      "goodsNm": "Merchant Goods 1",
                      "dbProcessUrl": "https://webhook.site/e15ef201-98a9-428c-85d4-a0c6458939c3",
                      "vacctValidDt": "",
                      "vacctValidTm": "",
                      "msId": "",
                      "msFee": "",
                      "msFeeType": "",
                      "mbFee": "",
                      "mbFeeType": ""
                      }

    bodyCreateVA = (
        builderVirtualAccount.BuildCreateVA()
        .setPartnerServiceId("")
        .setCustomerNo("")
        .setVirtualAccountNo("")
        .setVirtualAccountName("John Doe")
        .setTrxId("123")
        .setTotalAmount(totalAmount)
        .setAdditionalInfo(additionalInfo)
        .build()
    )

    result = SnapService.serviceTransaction(bodyCreateToken.jsonAccessToken(),
                                            bodyCreateVA.jsonVACreate(),
                                            ConstantsEndpoints.createVA())
```
Here's the result 
```bash
body request :
{"partnerServiceId": "", "customerNo": "", "virtualAccountNo": "", "virtualAccountName": "John Doe", "trxId": "123", "totalAmount": {"value": "10000.00", "currency": "IDR"}, "additionalInfo": {"bankCd": "BRIN", "goodsNm": "Merchant Goods 1", "dbProcessUrl": "https://webhook.site/e15ef201-98a9-428c-85d4-a0c6458939c3", "vacctValidDt": "", "vacctValidTm": "", "msId": "", "msFee": "", "msFeeType": "", "mbFee": "", "mbFeeType": ""}}

body response :
{"responseCode": "2002700", "responseMessage": "Successful", "virtualAccountData": {"partnerServiceId": "", "customerNo": "", "virtualAccountNo": "884800040254370152", "virtualAccountName": "John Doe", "trxId": "123", "totalAmount": {"value": "10000.00", "currency": "IDR"}, "additionalInfo": {"msId": "", "msFee": "", "msFeeType": "", "mbFee": "", "mbFeeType": "", "bankCd": "BRIN", "tXidVA": "IONPAYTEST02202411130254370152", "goodsNm": "Merchant Goods 1", "vacctValidDt": "20241115", "vacctValidTm": "025437"}}}
```
#### 2.4 Verify Signature 
- Import
```bash
import hashlib
import hmac
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from util.utilLogging import Log
```

- for Access Token
```bash
class Signature:
    log = Log()

    @staticmethod
    def signSHA256RSA(stringToSign, privateKey):
        try:
            b1 = base64.b64decode(privateKey)
            key = RSA.importKey(b1)
            signer = PKCS1_v1_5.new(key)
            digest = SHA256.new()
            digest.update(stringToSign.encode('utf-8'))
            signature = signer.sign(digest)
            hexSignature = base64.b64encode(signature).decode('utf-8')
            return hexSignature
        except Exception as e:
            Signature.log.error("Error Generate Signature:" + e)
            return ''


@staticmethod
    def sha256EncodeHex(data):
        sha256Hash = hashlib.sha256(data.encode('utf-8')).digest()
        hexEncoded = sha256Hash.hex()
        return hexEncoded
```
- for Signature Service
```bash
@staticmethod
    def getSignature(accessToken, requestBody, endpoint, timestamp, staticKey, httpMethod):
        Signature.log.info("util - Request Endpoint : " + endpoint)
        data = f"{httpMethod}:{endpoint}:{accessToken}:{requestBody}:{timestamp}"
        Signature.log.info("util - StringDataToSign: " + data)
        try:
            sign = Signature.hmacSHA512EncodeBase64(staticKey, data)
            Signature.log.info("util - Signature: " + sign)
            return sign
        except:
            Signature.log.error("Error Generate Signature - getSignature")

 @staticmethod
    def hmacSHA512EncodeBase64(key, data):
        hmacObj = hmac.new(key.encode('utf-8'), data.encode('utf-8'), hashlib.sha512)
        hmacBytes = hmacObj.digest()
        base64Encoded = base64.b64encode(hmacBytes).decode('utf-8')
        return base64Encoded
```
Here's the result
```bash
StringDataToSign: POST:/api/v1.0/transfer-va/create-va:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJJT05QQVlURVNUIiwiaXNzIjoiTklDRVBBWSIsIm5hbWUiOiJCRElOIiwiZXhwIjoiMjAyNC0xMS0xMlQyMDowOTozN1oifQ==.4djzd9Z1jZE8AXkFRmCrxm8IMfdhuk2RjFz0LSzRXIY=:d04af00b1f17c7045dde178f377b77e385a3d6cecd22fe6822de1ee053489078:2024-11-13T02:54:37+07:00

Signature: w7BpJ392jzRkAgvWC79Zawvztm/l1D+bxIJWgGq59xih0SuAi4PoTtUAUIXcOLuvZ3pYaSs8Mc1QZxhbVMMBqQ==
```

You can view a code example in the following **[UtilSignature.py](https://github.com/nicepay-dev/python-nicepay/blob/main/util/utilSignature.py)** class.
## 3. Other Sample

Integration test are available for SNAP :
- [Virtual Account Regist Unit Test](https://github.com/nicepay-dev/python-nicepay/blob/main/test/snap/testVirtualAccount.py)
- [Virtual Account Inquiry Unit Test](https://github.com/nicepay-dev/python-nicepay/blob/main/test/snap/testVirtualAccountInquiry.py)
- [Virtual Account Cancel Unit Test](https://github.com/nicepay-dev/python-nicepay/blob/main/test/snap/testVirtualAccountCancel.py)
- [E-Wallet Regist Unit Test](https://github.com/nicepay-dev/python-nicepay/blob/main/test/snap/testDirectDebit.py)
- [E-Wallet Inquiry Unit Test](https://github.com/nicepay-dev/python-nicepay/blob/main/test/snap/testDirectDebitInquiry.py)
- [E-Wallet Refund Unit Test](https://github.com/nicepay-dev/python-nicepay/blob/main/test/snap/testDirectDebitRefund.py)
- [Qris Regist Unit Test](https://github.com/nicepay-dev/python-nicepay/blob/main/test/snap/testQris.py)
- [Qris Inquiry Unit Test](https://github.com/nicepay-dev/python-nicepay/blob/main/test/snap/testQrisInquiry.py)
- [Qris Refund Unit Test](https://github.com/nicepay-dev/python-nicepay/blob/main/test/snap/testQrisRefund.py)
- [Payout Regist Unit Test](https://github.com/nicepay-dev/python-nicepay/blob/main/test/snap/testPayout.py)
- [Payout Inquiry Unit Test](https://github.com/nicepay-dev/python-nicepay/blob/main/test/snap/testPayoutInquiry.py)
- [Payout Approve Unit Test](https://github.com/nicepay-dev/python-nicepay/blob/main/test/snap/testPayoutApprove.py)
- [Payout Reject Unit Test](https://github.com/nicepay-dev/python-nicepay/blob/main/test/snap/testPayoutReject.py)
- [Payout Cancel Unit Test](https://github.com/nicepay-dev/python-nicepay/blob/main/test/snap/testPayoutReject.py)
- [Payout Balance Inquiry Unit Test](https://github.com/nicepay-dev/python-nicepay/blob/main/test/snap/testPayoutBalanceInquiry.py)

##### Integration test are available for V2 APIs :
- [Virtual Account V2 Unit Test](https://github.com/nicepay-dev/python-nicepay/blob/main/test/v2/enterprise/testVirtualAccount.py)
- [Inquiry V2 Unit Test](https://github.com/nicepay-dev/python-nicepay/blob/main/test/v2/enterprise/testInquiry.py)
- [Payment V2 Unit Test](https://github.com/nicepay-dev/python-nicepay/blob/main/test/v2/enterprise/testPayment.py)
- [Cancel V2 Unit Test](https://github.com/nicepay-dev/python-nicepay/blob/main/test/v2/enterprise/testCancel.py)

or you can view a example in the following [V2 APIs](https://github.com/nicepay-dev/python-nicepay/tree/main/test/v2)

## 4. Get Help
- [Nicepay Docs](https://docs.nicepay.co.id/)
- [Nicepay Dashboard](http://103.20.51.40:8012/logIn.do)
- [SNAP documentation](https://docs.nicepay.co.id/nicepay-api-snap)
- [V2 Enterprise documentation](https://docs.nicepay.co.id/nicepay-api-v2-payment-api)
- [V2 Professional documentation](https://docs.nicepay.co.id/nicepay-api-v2-checkout-api)


Can't find answer you looking for? email to `cs@nicepay.co.id`

**Thank you and Have a NICEPAY!** 

![Logo](https://nicepay.co.id/wp-content/uploads/2019/09/logo-150.svg )

