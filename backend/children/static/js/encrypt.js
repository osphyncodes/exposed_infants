// Function to download CSV
const secretKey = 'Osphyncodes_738475-2384853-2832%^#&*@*(#*@'; // Keep this secret!

// Encrypt and store data
function setEncryptedItem(key, value) {
    var ciphertext = CryptoJS.AES.encrypt(JSON.stringify(value), secretKey).toString();
    localStorage.setItem(key, ciphertext);
}

// Retrieve and decrypt data
function getDecryptedItem(key) {
    var ciphertext = localStorage.getItem(key);
    if (!ciphertext) return null;

    try {
        var bytes = CryptoJS.AES.decrypt(ciphertext, secretKey);
        var decryptedData = bytes.toString(CryptoJS.enc.Utf8);
        return JSON.parse(decryptedData);
    } catch (error) {
        console.error('Decryption failed:', error);
        return null;
    }
}
