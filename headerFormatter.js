const headersString = `cache-control: max-age=0
sec-ch-ua: "Chromium";v="124", "Brave";v="124", "Not-A.Brand";v="99"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "macOS"
origin: https://ankama.zendesk.com
dnt: 1
upgrade-insecure-requests: 1
content-type: application/x-www-form-urlencoded
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8
sec-gpc: 1
accept-language: en-GB,en;q=0.7
sec-fetch-site: same-origin
sec-fetch-mode: navigate
sec-fetch-user: ?1
sec-fetch-dest: document
referer: https://ankama.zendesk.com/auth/v2/login/signin
accept-encoding: gzip, deflate, br, zstd`;
function headersToJson(rawHeaders) {
  // Split the input into lines based on the newline character
  const lines = rawHeaders.trim().split('\n');
  const headerObject = {};

  // Iterate over each line, splitting into key-value pairs and trimming whitespace
  lines.forEach(line => {
      const [key, value] = line.split(':').map(part => part.trim());
      headerObject[key] = value;
  });

  // Convert the header object into a JSON string
  const jsonString = JSON.stringify(headerObject);

  // Escape the JSON string to make it suitable for embedding in a single line

  return jsonString;
}
const headerNames = headersString.split('\n')
  .map(line => line.split(': ')[0])
  .filter((value, index, self) => self.indexOf(value) === index) // Remove duplicates
  .join(', ');
const singleLineJson = headersToJson(headersString);
console.log(singleLineJson);
console.log(headerNames);
