const express = require("express");
const cluster = require("cluster");
const totalCPUs = require("os").cpus().length;

if (cluster.isMaster) {
  console.log(`Number of CPUs is ${totalCPUs}`);
  console.log(`Master ${process.pid} is running`);

  for (let i = 0; i < totalCPUs; i++) {
    cluster.fork();
  }

  cluster.on("exit", (worker, code, signal) => {
    console.log(`worker ${worker.process.pid} died, restarting...`);
    cluster.fork();
  });
} else {
  const app = express();
  app.use(express.json());

  app.post("/generateHeaders", (req, res) => {
    try {
      const ua = req.body.ua;
      const proxy = formatIpAddress(req.body.proxy);
      if (!ua || !proxy) {
        return res
          .status(400)
          .json({ error: "Missing required fields 'ua' and/or 'proxy'" });
      }

      const headers = JSON.stringify(generateHeaders(ua));
      res.json({ headers, proxy });
    } catch (error) {
      console.error(`Error in /generateHeaders: ${error.message}`);
      res.status(500).json({ error: "Internal Server Error" });
    }
  });
  function formatIpAddress(input) {
    // Split the input by ":"
    const components = input.split(":");

    // Check if there are four components (ip, port, user, pass)
    if (components.length === 4) {
      const [ip, port, user, pass] = components;
      return `${user}:${pass}@${ip}:${port}`;
    }

    // If not, return the input as it is
    return input;
  }
  function generateRandomToken() {
    return Math.random().toString(36).substring(2, 15);
  }

  function generateRandomDate() {
    const date = new Date();
    date.setDate(date.getDate() - Math.floor(Math.random() * 100));
    return date.toUTCString();
  }

  function randomChoice(array) {
    return array[Math.floor(Math.random() * array.length)];
  }

  function generateRandomHttpMethods(count) {
    const methods = [
      "get",
      "post",
      "put",
      "delete",
      "patch",
      "options",
      "head",
    ];
    let chosenMethods = [];
    for (let i = 0; i < count; i++) {
      chosenMethods.push(randomChoice(methods));
    }
    return chosenMethods.join(", ");
  }

  function generateHeaders(ua) {
    return {
      "tm-integrator-id": "prd1741.iccp",
      "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
      "tm-placement-id": "mytmlogin",
      "accept-language": "en-us",
      "sec-ch-ua-mobile": "?0",
      "user-agent": ua,
      "content-type": "application/json",
      "tm-site-token": "tm-us",
      "tm-client-id": "8bf7204a7e97.web.ticketmaster.us",
      "nds-pmd":
        '{"jvqtrgQngn":{"oq":"1290:816:1295:820:1295:820","wfi":"flap-1","ji":"2.3.1","oc":"rpqq954q95809o60","fe":"1295k820 30","qvqgm":"-330","jxe":245904,"syi":"snyfr","si":"si,btt,zc4,jroz","sn":"sn,zcrt,btt,jni","us":"23qrs43no00806s3","cy":"ZnpVagry","sg":"{"zgc":0,"gf":snyfr,"gr":snyfr}","sp":"{"gp":gehr,"ap":gehr}","sf":"gehr","jt":"31q446612o858870","sz":"12r0213093p022r6","vce":"apvc,0,6579p0r5,2,1;fg,0,rznvy[bowrpgbowrpg]__vachg,0,cnffjbeq[bowrpgbowrpg]__vachg,0;zz,5976,225,18r,;gf,0,5976;xx,202,0,rznvy[bowrpgbowrpg]__vachg;ss,0,rznvy[bowrpgbowrpg]__vachg;zp,5q,284,qr,rznvy[bowrpgbowrpg]__vachg;zzf,189,0,n,43 q4,n41 2159,91s,93q,-sn99,191q,-2624;xq,67,0;xh,33,0;xq,4n,0;xq,73,1;xh,p,0;xh,21,1;xq,7q,0;xh,4n,0;xq,7,0,5;xq,3r,1;xh,68,1;xh,o,0;xq,29,0;xh,28,0;xq,7r,0;zzf,18,3rn,n,ABC;xh,2q,0;xq,27,0;xq,6q,1;xh,11,0;xh,22,1;xq,82,0;xh,31,0;xq,69,0;xh,41,0;xq,22,0;xh,65,0;xq,12,0;xh,2n,0;xq,79,0;xh,38,0;zzf,23,3r8,n,ABC;xq,20,0,8;so,2,rznvy[bowrpgbowrpg]__vachg;xx,1,0,cnffjbeq[bowrpgbowrpg]__vachg;ss,0,cnffjbeq[bowrpgbowrpg]__vachg;xh,51,0;xq,o9,0;xq,9,1;xq,s,2;xh,1q,2;xq,0,2;xq,1n,3;xh,2,0;xh,7,2;xq,p,2;xh,8,1;xq,0,2;xq,1q,3;xh,2,2;xh,0,3;xq,4,2;xq,11,3;xh,7,2;xh,4,3;xq,9,2;xh,24,2;xq,0,2;xh,7,3;xq,0,2;xh,15,2;xh,o,2;xh,8,2;zzf,1o1,3r5,n,2184 qs4,37p2 39or,on8,o8n,-1op17,32npr,24np;so,24s,cnffjbeq[bowrpgbowrpg]__vachg;zp,4s,3s1,1p3,;","vp":"0,qr;","ns":"","qvg":""},"jg":"1.j-481390.1.2.zPvMQpXL-M_yDtl0RKUDSj,,.e1xqLQfZRm47f_FqmjRoWp9VwQO7sxBrnfLIVxhclFy5xDz8NpPWol1Iua5DY7-3Aowfxz_LRkyqze9JRnZO5JqI3eZv-OyhEQiWl5T2q3B3DJUxbB9RRLdRN7bOS3SD3RK1Xdwv4kYOPDPGrmFSUMwyKFp-wt6tUSQ-mmmm8aD-tec0ohj39BAuWam8iUGH4iVx09LU7mDhimOvhuSTj1UYTx792bGEuZYX2vHUQwJOQ-aJyMUPg-hplGYNIZmT"}',
      "sec-ch-ua-platform": '"macOS"',
      accept: "*/*",
      "sec-gpc": "1",
      origin: "https://auth.ticketmaster.com",
      "sec-fetch-site": "same-origin",
      "sec-fetch-mode": "cors",
      "sec-fetch-dest": "empty",
      referer:
        "https://auth.ticketmaster.com/as/authorization.oauth2?client_id=8bf7204a7e97.web.ticketmaster.us&response_type=code&scope=openid%20profile%20phone%20email%20tm&redirect_uri=https://identity.ticketmaster.com/exchange&visualPresets=tm&lang=en-us&placementId=mytmlogin&hideLeftPanel=false&integratorId=prd1741.iccp&intSiteToken=tm-us&deviceId=pQ8Xcz3Tq7W3trS6t762ur64tbqATjCp1VpOhQ",
      "accept-encoding": "gzip, deflate, br",
      "front-end-https": "On",
      "x-att-deviceid": generateRandomToken(),
      "x-request-id": generateRandomToken(),
      "x-correlation-id": generateRandomToken(),
      "save-data": "Yes",
      "upgrade-insecure-requests": "1",
      "content-security-policy": "default-src 'self'",
      te: "Trailers",
      trailer: "Expires",
      prefer: "return=representation",
      pragma: "no-cache",
      "if-unmodified-since": generateRandomDate(),
      "if-range": generateRandomDate(),
      "if-none-match": generateRandomToken(),
      "if-match": generateRandomToken(),
      expect: "100-continue",
      "access-control-request-method": randomChoice([
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS",
        "PATCH",
        "HEAD",
      ]),
      "x-uidh": generateRandomToken(),
      "last-modified": generateRandomDate(),
      vary: "Accept-Encoding",
      "x-powered-by": randomChoice([
        "PHP/7.4.3",
        "Apache/2.4.41",
        "Nginx/1.18.0",
        "Express/4.17.1",
      ]),
      "x-redirect-by": randomChoice([
        "WordPress",
        "Nginx",
        "Apache",
        "URL redirection",
      ]),
      expires: generateRandomDate(),
      "x-csrf-token": generateRandomToken(),
      "x-xsrf-token": generateRandomToken(),
      "sec-gpc": "1",
      allow: generateRandomHttpMethods(Math.floor(Math.random() * 3) + 1),
      dnt: "1",
      via: "1.1 varnish",
      warning: '110 - "Response is Stale"',
    };
  }
  app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send("Something broke!");
  });

  app.listen(8050, () => {
    console.log(`Worker ${process.pid} started`);
  });
}
