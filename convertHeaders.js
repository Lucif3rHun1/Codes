// Function to convert header string to a JSON object
function headersToJson(headerStr) {
  const headersArray = headerStr.split('\n').filter(line => line.trim() !== '');
  const headersJson = {};

  headersArray.forEach(header => {
    const [key, value] = header.split(/:\s*/);
    headersJson[key] = value;
  });

  return headersJson;
}

// Your headers as a plain string
const headersString = `upgrade-insecure-requests: 1
dnt: 1
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8
sec-gpc: 1
sec-fetch-site: same-site
sec-fetch-mode: navigate
sec-fetch-user: ?1
sec-fetch-dest: document
sec-ch-ua: "Not A(Brand";v="99", "Brave";v="121", "Chromium";v="121"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "macOS"
accept-language: en-GB,en;q=0.7
referer: https://www.ticketmaster.com/
accept-encoding: gzip, deflate, br`.trim();

// Convert to JSON
const headersJson = headersToJson(headersString);

// Use JSON.stringify to convert the JSON object to a string if needed for a payload
const headersJsonString = JSON.stringify(headersJson, null);

console.log(headersJsonString);
