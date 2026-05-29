// sm2_bridge.js
const sm2 = require('miniprogram-sm-crypto').sm2;

/**
 * 封装签名方法
 * @param {string} msgHex - 待签名消息的十六进制字符串
 * @param {string} privKeyHex - 私钥的十六进制字符串
 * @param {object} options - 签名配置（如 hash: true, der: true 等）
 * @returns {string} 签名结果
 */
function sign(msgHex, privKeyHex, options = { hash: true, der: true }) {
    // sm2.doSignature 接收的第一个参数可以是 hex 字符串或 Array
    try {
        let sigValue = sm2.doSignature(msgHex, privKeyHex, options);
        return sigValue;
    } catch (e) {
        return "Error: " + e.message;
    }
}

function decrypt(encryptDataHex, privKeyHex, cipherMode = 1) {
    try {
        // doDecrypt 直接返回解密后的原始字符串
        let decryptData = sm2.doDecrypt(encryptDataHex, privKeyHex, cipherMode);
        return decryptData;
    } catch (e) {
        return "Error: " + e.message;
    }
}

function getPublicKey(privKey) {
    return sm2.getPublicKeyFromPrivateKey(privKey);
}

function verify(msg, sigHex, pubKey) {
    try {
        return sm2.doVerifySignature(msg, sigHex, pubKey, { hash: true });
    } catch (e) {
        return false;
    }
}

// 导出给 execjs 使用（execjs 本质是拼接字符串执行，所以函数需要全局可见）
global.sign = sign;
global.decrypt = decrypt;
global.getPublicKey = getPublicKey;
global.verify = verify;