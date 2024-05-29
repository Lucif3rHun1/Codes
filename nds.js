const { createCanvas } = require('canvas');
const express = require('express');
const cluster = require('cluster');
const os = require('os');
const axios = require('axios');

const app = express();
const numCPUs = os.cpus().length;

let G = null
, ka = 1
, A = ""
, ya = null
, Na = 2
, ja = null
, za = "fb"
, Aa = "mc"
, Oa = "fs"
, ha = "mms"
, la = "so"
, va = null
, M = ""
, N = ""
, ea = !0
, wa = "tr"
, W = 0

const hash = function(a) {
    var b = 0, c = 0, d;
    if (0 === a.length)
        return "00000000";
    var e = 0;
    for (d = a.length; e < d; e++) {
        var f = a.charCodeAt(e);
        0 === e % 2 ? (b = (b << 5) - b + f,
        b |= 0) : (c = (c << 5) - c + f,
        c |= 0)
    }
    0 > b && (b = 4294967295 + b + 1);
    0 > c && (c = 4294967295 + c + 1);
    return b.toString(16) + c.toString(16)
}

function ROT13(a) {
    return a.replace(/[A-Za-z]/g, function(a) {
        return String.fromCharCode(a.charCodeAt(0) + ("M" >= a.toUpperCase() ? 13 : -13))
    })
}



function k(a, b, c) {
    b -= G;
    1 < ka && (b = Math.round(b / ka));
    a = a + "," + b.toString(16);
    if (null != c && 0 < c.length) {
        a += ",";
        b = [];
        for (var d = 0; d < c.length; d++)
            "number" === typeof c[d] ? b.push(Math.round(c[d]).toString(16)) : null != c[d] && b.push(c[d].toString());
        c = b.join(",");
        a += c
    }
    return a
}

function ra(a) {
    var b = Math.floor(Date.now() / 1000)
      , d = k(wa, b, [M.length]);
    if (0 === W || a.length + d.length <= W)
        return "";
    a = a.substring(0, W - d.length);
    var e = a.lastIndexOf(";");
    if (0 > e)
        return "";
    G = b;
    return a.substring(0, e + 1) + d + ";"
}

function b(a) {
    va = a;
    M += A,
    N = ra(M)
    // !0 === ea && x(!1)
}

function l(a, d) {
    var e = Math.floor(Date.now() / 1000);
    if (null == G) {
        ja = G = ya = e;
        var t = [Math.floor(Date.now() / 1000), Na, ka];
        A = A + k("ncip", e, t) + ";";
        G = e
    }
    A = A + k(a, e, d) + ";";
    G = e;
    15E3 <= e - ja && (A = A + k("ts", e, [e - ya]) + ";",
    ja = G = e);
    switch (a) {
    case za:
    case Aa:
    case Oa:
    case la:
    case ha:
        b(e);
        break;
    default:
        2E3 < e - va && b(e)
    }
}


async function getHTML5CanvasSignature() {
    var a = "NA";
    try {
        const canvas = createCanvas(200, 40);
        const ctx = canvas.getContext('2d');

        // Fill text on canvas
        ctx.fillText("aBc#$efG~ \ude73\ud63d", 4, 10);
        ctx.fillStyle = "rgba(67, 92, 0, 0.5)";
        ctx.font = "18pt Arial";
        ctx.fillText("aBc#$~efG \ude73\ud63d", 8, 12);

        // Convert canvas to data URL
        a = canvas.toDataURL();
    } catch (d) {console.log(d)}
    return a;
}

async function getwt() {
    try {
      const response = await axios.get('https://api-ticketmaster.nd.nudatasecurity.com/2.2/w/w-481390/sync/js/', {
        headers: {
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36.0 (KHTML, like Gecko) Chrome/112.0.5615.165 Safari/537.36.0',
        },
      });
  
      const body = response.data;
      return body.split('"wt":"')[1].split('"')[0];
    } catch (error) {
      console.error('Error in getwt():', error.message);
      throw error;
    }
  }

async function gen() {
    G = null
    , ka = 1
    , A = ""
    , ya = null
    , Na = 2
    , ja = null
    , za = "fb"
    , Aa = "mc"
    , Oa = "fs"
    , ha = "mms"
    , la = "so"
    , va = null
    , M = ""
    , N = ""
    , ea = !0
    , wa = "tr"
    , W = 0
    l("st", ["input-panel1010,0"])
    return ROT13(JSON.stringify({
        "widgetData": {
          "bd": "851:714:1536:816:1536:816",
          "jsv": "sync-1",
          "bp": "2501cc0f72219bbc",
          "sr": "1536x864 24",
          "didtz": "-60",
          "wkr": 503168,
          "flv": "false",
          "fv": "fv,ogg,mp4,webm",
          "fa": "fa,mpeg,ogg,wav",
          "hf": "5ea8658a4e70c0a2",
          "pl": "Win32",
          "ft": {
            "mtp": 0,
            "ts": false,
            "te": false
          },
          "fc": {
            "tc": true,
            "nc": true
          },
          "fs": "true",
          "wg": "f2aab0055c58b750",
          "fm": "dd24746a55316ea4",
          "ipr": A,
          "af": ""
        },
        "wt": await getwt()
    }))
}


async function main() {
    try {
      if (cluster.isMaster) {
        // Fork workers for each CPU core
        for (let i = 0; i < numCPUs; i++) {
          cluster.fork();
        }
  
        cluster.on('exit', (worker, code, signal) => {
          console.log(`Worker ${worker.process.pid} died`);
        });
      } else {
        // Worker process handles the Express server and API endpoint
        // Call the gen function to get the result
        const result = await gen();
  
        // Set up an API endpoint to return the result
        app.get('/', async (req, res) => {
          try {
            // Directly use the pre-calculated result to respond to the request
            res.json({ result });
          } catch (error) {
            res.status(500).json({ error: 'An error occurred while processing the result.' });
          }
        });
  
        // Start the Express server for the worker process
        const port = 3000; // You can change this to any desired port number
        app.listen(port, () => {
          console.log(`Worker ${process.pid} is running on http://localhost:${port}`);
        });
      }
    } catch (error) {
      console.error('Error:', error.message);
    }
  }
  
  // Call the main function to start the Express server with multithreading
  main();
  
  
  
  
  
  
  
  