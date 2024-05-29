async function encode(input, shift) {
    let encoded = '';
    for (let i = 0; i < input.length; i++) {
      let charCode = input.charCodeAt(i);
      let newCharCode = charCode + 3;
      encoded += String.fromCharCode(newCharCode);
    }
    return encoded;
  }
const authKey = "PX-8316A88B-19DC-46D1-A0A9-068E3AA8FB48";
const shift = 3;
const encodedAuthKey = encode(authKey, shift);
console.log(encodedAuthKey)