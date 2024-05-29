const axios = require("axios");
const HttpProxyAgent = require("http-proxy-agent");
const HttpsProxyAgent = require("https-proxy-agent");
const axiosRetry = require('axios-retry');

// Configure Axios to retry failed requests
axiosRetry(axios, {
  retries: 3, // Retry up to 3 times
  retryDelay: axiosRetry.exponentialDelay, // Use exponential back off for retry delay
});

async function fetchDataWithProxy({ ua, proxy, url }) {
  try {
    // Setup proxy agents
    const httpAgent = new HttpProxyAgent(proxy);
    const httpsAgent = new HttpsProxyAgent(proxy);

    // Make GET request with proxy and custom headers
    const response = await axios.get(url, {
      httpAgent,
      httpsAgent,
      headers: {
        "sec-ch-ua":
          '"Not A(Brand";v="99", "Brave";v="121", "Chromium";v="121"',
        accept: "application/json; charset=utf-8",
        dnt: "1",
        "sec-ch-ua-mobile": "?0",
        "user-agent": ua,
        "sec-ch-ua-platform": '"macOS"',
        "sec-gpc": "1",
        "accept-language": "en-GB,en;q=0.7",
        origin: "https://www.ticketmaster.com",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        referer: "https://www.ticketmaster.com/",
        "accept-encoding": "gzip, deflate, br",
      },
    });

    // Make a request to the processing URL
    const processingResponse = await axios.post(
      "https://incapsula.justhyped.dev/reese84",
      {
        userAgent: ua,
        script: response.data,
      }
    );

    if (!processingResponse.data.payload) {
      throw new Error("No payload received");
    }

    // Make a POST request with the URL and payload obtained
    const finalResponse = await axios.post(
      url,
      processingResponse.data.payload,
      {
        headers: { "Content-Type": "application/json" },
      }
    );

    return finalResponse.data;
  } catch (error) {
    console.error(error.message);
    throw error; // Or handle more gracefully depending on your needs
  }
}

// Example usage
const jsonPayload = {
  ua: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
  proxy: "http://yahunc1-zone-resi-region-us:yahunc323@4195513672a34b1c.na.pyproxy.io:16666",
  url: "https://epsf.ticketmaster.com/eps-d?d=www.ticketmaster.com",
};

fetchDataWithProxy(jsonPayload)
  .then((response) => {
    console.log(response);
  })
  .catch((error) => {
    console.log(error);
  });
