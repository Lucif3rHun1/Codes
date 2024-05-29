function convertMultipartToPattern(multipartData) {
    // Split the multipart data by '--inv-boundery' into individual parts
    const parts = multipartData.split('--inv-boundery');
    
    // Remove the first and last empty parts
    parts.shift();
    parts.pop();

    // Map over each part and format it according to the specified pattern
    const convertedData = parts.map(part => {
        // Extract the fieldname and fieldvalue from each part
        const match = part.match(/name="([^"]+)"\s*\r?\n\r?\n([^]*)/);
        if (match && match.length === 3) {
            const fieldname = match[1];
            const fieldvalue = match[2].trim();
            // Format the part according to the specified pattern
            return `STRING: ${fieldname}: ${fieldvalue}`;
        }
        return '';
    });

    // Join the converted parts with newline characters
    return convertedData.join('\n');
}

// Example usage
const multipartData = `--inv-boundery
Content-Disposition: form-data; name="reg_source"

ios
--inv-boundery
Content-Disposition: form-data; name="smssupport"

true
--inv-boundery
Content-Disposition: form-data; name="reg_initiator"

Side Menu Sign In
--inv-boundery
Content-Disposition: form-data; name="email"

mail@hmsil.com
--inv-boundery
Content-Disposition: form-data; name="smd"

57D50BEE-A345-49FE-A0F0-060BDF58EF6A-1714757863166
--inv-boundery
Content-Disposition: form-data; name="internal_version"

230
--inv-boundery
Content-Disposition: form-data; name="password"

e10adc3949ba59abbe56e057f20f883e
--inv-boundery
Content-Disposition: form-data; name="ga_cid"

0424bdb8-c5d3-4008-a39f-b437e402e280
--inv-boundery
Content-Disposition: form-data; name="unique_device_id"

57D50BEE-A345-49FE-A0F0-060BDF58EF6A
--inv-boundery`;

const convertedData = convertMultipartToPattern(multipartData);
console.log(convertedData);
