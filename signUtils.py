# -*- coding: utf-8 -*-
# @Time    : 2026-05-29
# @Author  : xlxlSakura
# @FileName: signUtils.py
# @Software: PyCharm
# @Description: 国密SM2签名算法
# @Version: 0.1

import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

import os
import time
import secrets
import struct

privateKey = "00f661332f70969150a8ea126943958a914cc05abc7e3ad3d96570cc4fd01a9ce4"

def _rotl32(x: int, n: int) -> int:
    """32位循环左移，对应JS中的 o(t, e) 函数"""
    x &= 0xFFFFFFFF
    n &= 31
    if n == 0:
        return x
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF


def _sm3_p0(x: int) -> int:
    """P0置换: x ^ ROTL(x,9) ^ ROTL(x,17)，对应JS中的 s(t) 函数"""
    return (x ^ _rotl32(x, 9) ^ _rotl32(x, 17)) & 0xFFFFFFFF


def _sm3_p1(x: int) -> int:
    """P1置换: x ^ ROTL(x,15) ^ ROTL(x,23)"""
    return (x ^ _rotl32(x, 15) ^ _rotl32(x, 23)) & 0xFFFFFFFF


def sm3_hash(data: bytes) -> bytes:
    """
    SM3密码杂凑算法
    输入: bytes
    输出: 32 字节哈希值
    """
    # SM3初始向量 IV
    IV = [
        0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600,
        0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E,
    ]

    # ---- 消息填充 ----
    msg_len = len(data)
    bit_len = msg_len * 8
    padded = bytearray(data)
    padded.append(0x80)  # 追加'1'位
    while len(padded) % 64 != 56:  # 填充0直到 mod 64 == 56
        padded.append(0x00)
    padded.extend(struct.pack('>Q', bit_len))  # 追加64位长度

    # ---- 分块处理 ----
    V = list(IV)  # 哈希中间值

    for block_start in range(0, len(padded), 64):
        block = padded[block_start: block_start + 64]

        # 消息扩展 W[0..67], W'[0..63]
        W = [0] * 68
        W_prime = [0] * 64

        for i in range(16):
            W[i] = struct.unpack('>I', block[i * 4: i * 4 + 4])[0]

        for i in range(16, 68):
            tmp = W[i - 16] ^ W[i - 9] ^ _rotl32(W[i - 3], 15)
            W[i] = (_sm3_p1(tmp) ^ _rotl32(W[i - 13], 7) ^ W[i - 6]) & 0xFFFFFFFF

        for i in range(64):
            W_prime[i] = (W[i] ^ W[i + 4]) & 0xFFFFFFFF

        # 压缩函数
        A, B, C, D, E, F, G, H = V

        for j in range(64):
            # 常数 T_j
            T = 0x79CC4519 if j <= 15 else 0x7A879D8A

            # SS1 = ROTL(ROTL(A,12) + E + ROTL(T,j), 7)
            SS1 = _rotl32((_rotl32(A, 12) + E + _rotl32(T, j)) & 0xFFFFFFFF, 7)
            # SS2 = SS1 ^ ROTL(A,12)
            SS2 = (SS1 ^ _rotl32(A, 12)) & 0xFFFFFFFF

            # FF_j
            if j <= 15:
                FF = (A ^ B ^ C) & 0xFFFFFFFF
            else:
                FF = ((A & B) | (A & C) | (B & C)) & 0xFFFFFFFF

            # GG_j
            if j <= 15:
                GG = (E ^ F ^ G) & 0xFFFFFFFF
            else:
                GG = ((E & F) | ((~E & 0xFFFFFFFF) & G)) & 0xFFFFFFFF

            # TT1 = FF + D + SS2 + W'[j]
            TT1 = (FF + D + SS2 + W_prime[j]) & 0xFFFFFFFF
            # TT2 = GG + H + SS1 + W[j]
            TT2 = (GG + H + SS1 + W[j]) & 0xFFFFFFFF

            # 状态更新
            D = C
            C = _rotl32(B, 9)
            B = A
            A = TT1
            H = G
            G = _rotl32(F, 19)
            F = E
            E = _sm3_p0(TT2)

        # 更新哈希值
        V[0] ^= A;
        V[1] ^= B;
        V[2] ^= C;
        V[3] ^= D
        V[4] ^= E;
        V[5] ^= F;
        V[6] ^= G;
        V[7] ^= H

    return struct.pack('>8I', *V)

SM2_P = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
SM2_A = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
SM2_B = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
SM2_GX = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
SM2_GY = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
SM2_N = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123

DEFAULT_USER_ID = "1234567812345678"

# 生成元G
_G = (SM2_GX, SM2_GY)


def _ec_add(P1, P2):
    """椭圆曲线点加法 P1 + P2（仿射坐标）"""
    if P1 is None:
        return P2
    if P2 is None:
        return P1
    x1, y1 = P1
    x2, y2 = P2
    if x1 == x2 and (y1 + y2) % SM2_P == 0:
        return None  # 无穷远点
    if x1 == x2 and y1 == y2:
        # 点加倍: lambda = (3*x1^2 + a) / (2*y1)
        lam = ((3 * x1 * x1 + SM2_A) * pow(2 * y1, -1, SM2_P)) % SM2_P
    else:
        # 点加法: lambda = (y2 - y1) / (x2 - x1)
        lam = ((y2 - y1) * pow(x2 - x1, -1, SM2_P)) % SM2_P
    x3 = (lam * lam - x1 - x2) % SM2_P
    y3 = (lam * (x1 - x3) - y1) % SM2_P
    return (x3, y3)


def _ec_mul(k: int, P):
    """椭圆曲线标量乘法 k * P（二进制展开法）"""
    if k == 0 or P is None:
        return None
    result = None
    addend = P
    while k:
        if k & 1:
            result = _ec_add(result, addend)
        addend = _ec_add(addend, addend)
        k >>= 1
    return result


def _derive_public_key(private_key_hex: str):
    """
    从私钥推导公钥点 PA = d * G
    对应JS中的 p(t) 函数
    """
    d = int(private_key_hex, 16)
    return _ec_mul(d, _G)


def _compute_za(PA, user_id: str = DEFAULT_USER_ID) -> bytes:
    """
    计算ZA值
    ZA = SM3(ENTL || ID || a || b || Gx || Gy || PA.x || PA.y)
    """
    user_id_bytes = user_id.encode('utf-8')
    entl = len(user_id_bytes) * 8  # ID的比特长度

    za_input = bytearray()
    # ENTL: 2字节大端（ID的比特长度）
    za_input.extend(struct.pack('>H', entl))
    # ID
    za_input.extend(user_id_bytes)
    # 曲线参数 a, b, Gx, Gy, PA.x, PA.y（各32字节大端）
    for val in [SM2_A, SM2_B, SM2_GX, SM2_GY, PA[0], PA[1]]:
        za_input.extend(val.to_bytes(32, 'big'))

    return sm3_hash(bytes(za_input))


def sm2_sign(timestamp: int, private_key_hex: str) -> str:
    """
    SM2签名生成
    """
    # 1. 时间戳转字符串
    msg_str = str(timestamp)

    # 2. 取UTF-8字节（ASCII数字的UTF-8编码就是其ASCII码）
    #    等价于 JS 的 utf8ToHex(msg) 后再 hexToArray()
    msg_bytes = msg_str.encode('utf-8')

    # 3. 推导公钥
    PA = _derive_public_key(private_key_hex)

    # 4. 计算 ZA
    ZA = _compute_za(PA)

    # 5. 计算 e = SM3(ZA || msg_bytes)
    e_hash = sm3_hash(ZA + msg_bytes)
    e = int.from_bytes(e_hash, 'big')

    # 6. SM2签名
    d = int(private_key_hex, 16)
    n = SM2_N

    while True:
        # 生成随机 k ∈ [1, n-1]
        k = secrets.randbelow(n - 1) + 1

        # (x1, y1) = k * G
        point = _ec_mul(k, _G)
        x1 = point[0]

        # r = (e + x1) mod n
        r = (e + x1) % n
        if r == 0 or (r + k) == n:
            continue

        # s = ((1 + d)^{-1} * (k - r * d)) mod n
        s = (pow(d + 1, -1, n) * (k - r * d)) % n
        if s == 0:
            continue

        break

    # 返回 r || s（各左填充到64 hex字符）
    return format(r, '064x') + format(s, '064x')


def sm2_verify(timestamp: int, signature_hex: str, private_key_hex: str) -> bool:
    """
    SM2签名验证（用于本地测试签名是否正确）
    """
    msg_str = str(timestamp)
    msg_bytes = msg_str.encode('utf-8')
    PA = _derive_public_key(private_key_hex)
    ZA = _compute_za(PA)
    e_hash = sm3_hash(ZA + msg_bytes)
    e = int.from_bytes(e_hash, 'big')

    r = int(signature_hex[:64], 16)
    s = int(signature_hex[64:], 16)
    n = SM2_N

    # 验证: r != 0 and s != 0 and r < n and s < n
    if r == 0 or s == 0 or r >= n or s >= n:
        return False

    # t = (r + s) mod n
    t = (r + s) % n
    if t == 0:
        return False

    # (x1, y1) = s*G + t*PA
    point = _ec_add(_ec_mul(s, _G), _ec_mul(t, PA))
    if point is None:
        return False
    x1 = point[0]

    # R = (e + x1) mod n
    R = (e + x1) % n

    return R == r

def getSignAndTimestamp():
    timestamp = int(time.time() * 1000)
    sign = sm2_sign(timestamp, privateKey)
    return [sign, str(timestamp)]