# pip install --upgrade capsolver
# export CAPSOLVER_API_KEY='...'

import capsolver

# capsolver.api_key = "..."
solution = capsolver.solve({
    "type": "ReCaptchaV3M1TaskProxyLess",
    "websiteURL": "https://www.google.com",
    "websiteKey": "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_kl-",
})
print(solution)