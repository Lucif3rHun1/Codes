const bcrypt = require('bcryptjs');

// Password to hash
const password = 'your_password_here';

// Generate a salt (typically done once and stored securely)
const salt = "e0b8acf87396a3677f3e0735a8ee034b";

// Hash the password
const hashedPassword = bcrypt.hashSync(password, salt);

console.log('Hashed Password:', hashedPassword);
