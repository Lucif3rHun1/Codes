const CryptoJS = require('crypto-js');

// Constants
const KEY = "44D4E37C-C22D-455D-90F0-471B9AABC2C8/20231203";
const DATE = "20231203T204215Z";
const REGION = "us-east-1";
const SERVICE = "iam";
const REQ = "aws4_request";

// Step 1: Convert KEY to Base64
const KSECRET_B64 = CryptoJS.enc.Utf8.parse(`AWS4${KEY}`).toString(CryptoJS.enc.Base64);

// Step 2: Convert Base64 to ByteArray
const CON = CryptoJS.enc.Base64.parse(KSECRET_B64);

// Step 3: Convert ByteArray to HexString
const KSECRET_HEX = CON.toString(CryptoJS.enc.Hex);

// Step 4: Calculate Hmac for DATE
const DATEMAC = CryptoJS.HmacSHA256(DATE, CON);

// Step 5: Convert ByteArray to Base64
const KDATE_B64 = DATEMAC.toString(CryptoJS.enc.Base64);

// Step 6: Convert Base64 to ByteArray
const CON1 = CryptoJS.enc.Base64.parse(KDATE_B64);

// Step 7: Convert ByteArray to HexString
const KDATE_HEX = CON1.toString(CryptoJS.enc.Hex);

// Step 8: Calculate Hmac for REGION
const REGIONMAC = CryptoJS.HmacSHA256(REGION, CON1);

// Step 9: Convert ByteArray to Base64
const KREGION_B64 = REGIONMAC.toString(CryptoJS.enc.Base64);

// Step 10: Convert Base64 to ByteArray
const CON2 = CryptoJS.enc.Base64.parse(KREGION_B64);

// Step 11: Convert ByteArray to HexString
const KREGION_HEX = CON2.toString(CryptoJS.enc.Hex);

// Step 12: Calculate Hmac for SERVICE
const SERVICEMAC = CryptoJS.HmacSHA256(SERVICE, CON2);

// Step 13: Convert ByteArray to Base64
const KSERVICE_B64 = SERVICEMAC.toString(CryptoJS.enc.Base64);

// Step 14: Convert Base64 to ByteArray
const CON3 = CryptoJS.enc.Base64.parse(KSERVICE_B64);

// Step 15: Convert ByteArray to HexString
const KSERVICE_HEX = CON3.toString(CryptoJS.enc.Hex);

// Step 16: Calculate Hmac for REQ
const SIGNINGMAC = CryptoJS.HmacSHA256(REQ, CON3);

// Step 17: Convert ByteArray to Base64
const KSIGNING_B64 = SIGNINGMAC.toString(CryptoJS.enc.Base64);

// Step 18: Convert Base64 to ByteArray
const CON4 = CryptoJS.enc.Base64.parse(KSIGNING_B64);

// Step 19: Convert ByteArray to HexString (Signature)
const SIGNATURE = CON4.toString(CryptoJS.enc.Hex);

console.log('Signature:', SIGNATURE);
