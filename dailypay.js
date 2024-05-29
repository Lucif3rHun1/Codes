const axios = require('axios');
const cheerio = require('cheerio');
const https = require('https');

// Proxy configuration
const proxyConfig = {
    host: 'b825788e670315ba.na.pyproxy.io',  // Replace with your proxy host
    port: 16666,    // Replace with your proxy port
    auth: {
        username: 'salem1-zone-resi-region-us',
        password: 'man120'
    }
};

// Create an axios instance with proxy configuration
const axiosInstance = axios.create({
    proxy: proxyConfig,
    timeout: 10000,
    httpsAgent: new https.Agent({
        rejectUnauthorized: false,
        secureProtocol: 'TLSv1_2_method' // This bypasses SSL certificate validation. Use with caution!
    })
});

async function performRequests() {
    const ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0";
    const headers = {
        'Host': 'app.dailypay.com',
        'User-Agent': ua,  // Assuming ua is a variable containing the user agent string
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://app.dailypay.com/login',
        'Origin': 'https://app.dailypay.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'trailers'
    };
    
    try {
        // First GET request
        const response1 = await axiosInstance.get("http://students-crm.gl.at.ply.gg:35931/castle?ua=" + encodeURIComponent(ua), {
            headers: {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                "Pragma": "no-cache",
                "Accept": "*/*"
            }
        });
        const token = response1.data.token;
        console.log("Token:", token);
    } catch (error) {
        console.error("Error in first request:", error.message);
    }

    let csrf;
    try {
        // Second GET request
        const response2 = await axiosInstance.get("https://app.dailypay.com/forgot_password", {
            headers: headers
        });

        const $ = cheerio.load(response2.data);
        csrf = $('meta[name="csrf-token"]').attr('content');
        console.log("CSRF Token:", csrf);
    } catch (error) {
        console.error("Error in second request:", error.message);
    }

    try {
        // POST request
        const postData = `authenticity_token=${csrf}&forgot_password_email_form%5Bemail%5D=test@gmail.com&commit=Send+Password+Reset&castle_request_token=${token}`;
        const response3 = await axiosInstance.post("https://app.dailypay.com/forgot_password_email", postData, {
            headers: headers
        });

        const instruction = response3.data; // Adjust this based on actual response structure
        console.log("Instruction:", instruction);
    } catch (error) {
        console.error("Error in POST request:", error.message);
    }

    // Continue with other operations or requests
}

performRequests();
