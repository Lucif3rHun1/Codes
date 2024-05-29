const crypto = require('crypto');

const publicKey = '-----BEGIN PUBLIC KEY-----\n3/kUYfBDZyks/16oZAvBD4lAVboluOiW2HW26n5GDPCaE48ErTyF1DsLx2jm9Y3clApuc0lsUgU96nu1rWdTtvDN6OnNDrJQP20Wd9rG+Z/luurReJT+H+HUD9nwDGKEeiz2EYXNgyylOCH89XNYk6U5V5GsSxXvRkadlnfjj0=\n-----END PUBLIC KEY-----';

const message = 'hello';

function encryptMessage(publicKey, message) {
    const bufferMessage = Buffer.from(message, 'utf-8');
    const encrypted = crypto.publicEncrypt({
        key: publicKey,
        padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
        oaepHash: 'sha256',
    }, bufferMessage);
    return encrypted.toString('base64');
}
const Password = encryptMessage(publicKey, message);
console.log('Encrypted Password:', Password);
