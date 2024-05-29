const express = require('express');
const app = express();
app.use(express.json());

function parseAddress(json) {
    let addressParts = [];
    const addressFields = ['ligne2Adresse', 'ligne3Adresse', 'ligne4Adresse', 'ligne5Adresse', 'ligne6Adresse', 'ligne7Adresse'];

    for (let field of addressFields) {
        if (json[field] && json[field].trim() !== '') {
            addressParts.push(json[field].trim());
        }
    }

    return addressParts.join(', ');
}

app.post('/parse-address', (req, res) => {
    const address = parseAddress(req.body);
    res.json({ address: address });
});

const PORT = process.env.PORT || 3003;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
