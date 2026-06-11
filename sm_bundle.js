var smAlgorithm = (() => {
  var __getOwnPropNames = Object.getOwnPropertyNames;
  var __commonJS = (cb, mod) => function __require() {
    return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
  };

  // node_modules/@babel/runtime/helpers/typeof.js
  var require_typeof = __commonJS({
    "node_modules/@babel/runtime/helpers/typeof.js"(exports, module) {
      function _typeof(o) {
        return module.exports = _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(o2) {
          return typeof o2;
        } : function(o2) {
          return o2 && "function" == typeof Symbol && o2.constructor === Symbol && o2 !== Symbol.prototype ? "symbol" : typeof o2;
        }, _typeof(o);
      }
      module.exports = _typeof;
    }
  });

  // node_modules/jsbn/index.js
  var require_jsbn = __commonJS({
    "node_modules/jsbn/index.js"(exports, module) {
      (function() {
        var dbits;
        var canary = 244837814094590;
        var j_lm = (canary & 16777215) == 15715070;
        function BigInteger(a, b, c) {
          if (a != null)
            if ("number" == typeof a) this.fromNumber(a, b, c);
            else if (b == null && "string" != typeof a) this.fromString(a, 256);
            else this.fromString(a, b);
        }
        function nbi() {
          return new BigInteger(null);
        }
        function am1(i, x, w, j, c, n) {
          while (--n >= 0) {
            var v = x * this[i++] + w[j] + c;
            c = Math.floor(v / 67108864);
            w[j++] = v & 67108863;
          }
          return c;
        }
        function am2(i, x, w, j, c, n) {
          var xl = x & 32767, xh = x >> 15;
          while (--n >= 0) {
            var l = this[i] & 32767;
            var h = this[i++] >> 15;
            var m = xh * l + h * xl;
            l = xl * l + ((m & 32767) << 15) + w[j] + (c & 1073741823);
            c = (l >>> 30) + (m >>> 15) + xh * h + (c >>> 30);
            w[j++] = l & 1073741823;
          }
          return c;
        }
        function am3(i, x, w, j, c, n) {
          var xl = x & 16383, xh = x >> 14;
          while (--n >= 0) {
            var l = this[i] & 16383;
            var h = this[i++] >> 14;
            var m = xh * l + h * xl;
            l = xl * l + ((m & 16383) << 14) + w[j] + c;
            c = (l >> 28) + (m >> 14) + xh * h;
            w[j++] = l & 268435455;
          }
          return c;
        }
        var inBrowser = typeof navigator !== "undefined";
        if (inBrowser && j_lm && navigator.appName == "Microsoft Internet Explorer") {
          BigInteger.prototype.am = am2;
          dbits = 30;
        } else if (inBrowser && j_lm && navigator.appName != "Netscape") {
          BigInteger.prototype.am = am1;
          dbits = 26;
        } else {
          BigInteger.prototype.am = am3;
          dbits = 28;
        }
        BigInteger.prototype.DB = dbits;
        BigInteger.prototype.DM = (1 << dbits) - 1;
        BigInteger.prototype.DV = 1 << dbits;
        var BI_FP = 52;
        BigInteger.prototype.FV = Math.pow(2, BI_FP);
        BigInteger.prototype.F1 = BI_FP - dbits;
        BigInteger.prototype.F2 = 2 * dbits - BI_FP;
        var BI_RM = "0123456789abcdefghijklmnopqrstuvwxyz";
        var BI_RC = new Array();
        var rr, vv;
        rr = "0".charCodeAt(0);
        for (vv = 0; vv <= 9; ++vv) BI_RC[rr++] = vv;
        rr = "a".charCodeAt(0);
        for (vv = 10; vv < 36; ++vv) BI_RC[rr++] = vv;
        rr = "A".charCodeAt(0);
        for (vv = 10; vv < 36; ++vv) BI_RC[rr++] = vv;
        function int2char(n) {
          return BI_RM.charAt(n);
        }
        function intAt(s, i) {
          var c = BI_RC[s.charCodeAt(i)];
          return c == null ? -1 : c;
        }
        function bnpCopyTo(r) {
          for (var i = this.t - 1; i >= 0; --i) r[i] = this[i];
          r.t = this.t;
          r.s = this.s;
        }
        function bnpFromInt(x) {
          this.t = 1;
          this.s = x < 0 ? -1 : 0;
          if (x > 0) this[0] = x;
          else if (x < -1) this[0] = x + this.DV;
          else this.t = 0;
        }
        function nbv(i) {
          var r = nbi();
          r.fromInt(i);
          return r;
        }
        function bnpFromString(s, b) {
          var k;
          if (b == 16) k = 4;
          else if (b == 8) k = 3;
          else if (b == 256) k = 8;
          else if (b == 2) k = 1;
          else if (b == 32) k = 5;
          else if (b == 4) k = 2;
          else {
            this.fromRadix(s, b);
            return;
          }
          this.t = 0;
          this.s = 0;
          var i = s.length, mi = false, sh = 0;
          while (--i >= 0) {
            var x = k == 8 ? s[i] & 255 : intAt(s, i);
            if (x < 0) {
              if (s.charAt(i) == "-") mi = true;
              continue;
            }
            mi = false;
            if (sh == 0)
              this[this.t++] = x;
            else if (sh + k > this.DB) {
              this[this.t - 1] |= (x & (1 << this.DB - sh) - 1) << sh;
              this[this.t++] = x >> this.DB - sh;
            } else
              this[this.t - 1] |= x << sh;
            sh += k;
            if (sh >= this.DB) sh -= this.DB;
          }
          if (k == 8 && (s[0] & 128) != 0) {
            this.s = -1;
            if (sh > 0) this[this.t - 1] |= (1 << this.DB - sh) - 1 << sh;
          }
          this.clamp();
          if (mi) BigInteger.ZERO.subTo(this, this);
        }
        function bnpClamp() {
          var c = this.s & this.DM;
          while (this.t > 0 && this[this.t - 1] == c) --this.t;
        }
        function bnToString(b) {
          if (this.s < 0) return "-" + this.negate().toString(b);
          var k;
          if (b == 16) k = 4;
          else if (b == 8) k = 3;
          else if (b == 2) k = 1;
          else if (b == 32) k = 5;
          else if (b == 4) k = 2;
          else return this.toRadix(b);
          var km = (1 << k) - 1, d, m = false, r = "", i = this.t;
          var p = this.DB - i * this.DB % k;
          if (i-- > 0) {
            if (p < this.DB && (d = this[i] >> p) > 0) {
              m = true;
              r = int2char(d);
            }
            while (i >= 0) {
              if (p < k) {
                d = (this[i] & (1 << p) - 1) << k - p;
                d |= this[--i] >> (p += this.DB - k);
              } else {
                d = this[i] >> (p -= k) & km;
                if (p <= 0) {
                  p += this.DB;
                  --i;
                }
              }
              if (d > 0) m = true;
              if (m) r += int2char(d);
            }
          }
          return m ? r : "0";
        }
        function bnNegate() {
          var r = nbi();
          BigInteger.ZERO.subTo(this, r);
          return r;
        }
        function bnAbs() {
          return this.s < 0 ? this.negate() : this;
        }
        function bnCompareTo(a) {
          var r = this.s - a.s;
          if (r != 0) return r;
          var i = this.t;
          r = i - a.t;
          if (r != 0) return this.s < 0 ? -r : r;
          while (--i >= 0) if ((r = this[i] - a[i]) != 0) return r;
          return 0;
        }
        function nbits(x) {
          var r = 1, t2;
          if ((t2 = x >>> 16) != 0) {
            x = t2;
            r += 16;
          }
          if ((t2 = x >> 8) != 0) {
            x = t2;
            r += 8;
          }
          if ((t2 = x >> 4) != 0) {
            x = t2;
            r += 4;
          }
          if ((t2 = x >> 2) != 0) {
            x = t2;
            r += 2;
          }
          if ((t2 = x >> 1) != 0) {
            x = t2;
            r += 1;
          }
          return r;
        }
        function bnBitLength() {
          if (this.t <= 0) return 0;
          return this.DB * (this.t - 1) + nbits(this[this.t - 1] ^ this.s & this.DM);
        }
        function bnpDLShiftTo(n, r) {
          var i;
          for (i = this.t - 1; i >= 0; --i) r[i + n] = this[i];
          for (i = n - 1; i >= 0; --i) r[i] = 0;
          r.t = this.t + n;
          r.s = this.s;
        }
        function bnpDRShiftTo(n, r) {
          for (var i = n; i < this.t; ++i) r[i - n] = this[i];
          r.t = Math.max(this.t - n, 0);
          r.s = this.s;
        }
        function bnpLShiftTo(n, r) {
          var bs = n % this.DB;
          var cbs = this.DB - bs;
          var bm = (1 << cbs) - 1;
          var ds = Math.floor(n / this.DB), c = this.s << bs & this.DM, i;
          for (i = this.t - 1; i >= 0; --i) {
            r[i + ds + 1] = this[i] >> cbs | c;
            c = (this[i] & bm) << bs;
          }
          for (i = ds - 1; i >= 0; --i) r[i] = 0;
          r[ds] = c;
          r.t = this.t + ds + 1;
          r.s = this.s;
          r.clamp();
        }
        function bnpRShiftTo(n, r) {
          r.s = this.s;
          var ds = Math.floor(n / this.DB);
          if (ds >= this.t) {
            r.t = 0;
            return;
          }
          var bs = n % this.DB;
          var cbs = this.DB - bs;
          var bm = (1 << bs) - 1;
          r[0] = this[ds] >> bs;
          for (var i = ds + 1; i < this.t; ++i) {
            r[i - ds - 1] |= (this[i] & bm) << cbs;
            r[i - ds] = this[i] >> bs;
          }
          if (bs > 0) r[this.t - ds - 1] |= (this.s & bm) << cbs;
          r.t = this.t - ds;
          r.clamp();
        }
        function bnpSubTo(a, r) {
          var i = 0, c = 0, m = Math.min(a.t, this.t);
          while (i < m) {
            c += this[i] - a[i];
            r[i++] = c & this.DM;
            c >>= this.DB;
          }
          if (a.t < this.t) {
            c -= a.s;
            while (i < this.t) {
              c += this[i];
              r[i++] = c & this.DM;
              c >>= this.DB;
            }
            c += this.s;
          } else {
            c += this.s;
            while (i < a.t) {
              c -= a[i];
              r[i++] = c & this.DM;
              c >>= this.DB;
            }
            c -= a.s;
          }
          r.s = c < 0 ? -1 : 0;
          if (c < -1) r[i++] = this.DV + c;
          else if (c > 0) r[i++] = c;
          r.t = i;
          r.clamp();
        }
        function bnpMultiplyTo(a, r) {
          var x = this.abs(), y = a.abs();
          var i = x.t;
          r.t = i + y.t;
          while (--i >= 0) r[i] = 0;
          for (i = 0; i < y.t; ++i) r[i + x.t] = x.am(0, y[i], r, i, 0, x.t);
          r.s = 0;
          r.clamp();
          if (this.s != a.s) BigInteger.ZERO.subTo(r, r);
        }
        function bnpSquareTo(r) {
          var x = this.abs();
          var i = r.t = 2 * x.t;
          while (--i >= 0) r[i] = 0;
          for (i = 0; i < x.t - 1; ++i) {
            var c = x.am(i, x[i], r, 2 * i, 0, 1);
            if ((r[i + x.t] += x.am(i + 1, 2 * x[i], r, 2 * i + 1, c, x.t - i - 1)) >= x.DV) {
              r[i + x.t] -= x.DV;
              r[i + x.t + 1] = 1;
            }
          }
          if (r.t > 0) r[r.t - 1] += x.am(i, x[i], r, 2 * i, 0, 1);
          r.s = 0;
          r.clamp();
        }
        function bnpDivRemTo(m, q, r) {
          var pm = m.abs();
          if (pm.t <= 0) return;
          var pt = this.abs();
          if (pt.t < pm.t) {
            if (q != null) q.fromInt(0);
            if (r != null) this.copyTo(r);
            return;
          }
          if (r == null) r = nbi();
          var y = nbi(), ts = this.s, ms = m.s;
          var nsh = this.DB - nbits(pm[pm.t - 1]);
          if (nsh > 0) {
            pm.lShiftTo(nsh, y);
            pt.lShiftTo(nsh, r);
          } else {
            pm.copyTo(y);
            pt.copyTo(r);
          }
          var ys = y.t;
          var y0 = y[ys - 1];
          if (y0 == 0) return;
          var yt = y0 * (1 << this.F1) + (ys > 1 ? y[ys - 2] >> this.F2 : 0);
          var d1 = this.FV / yt, d2 = (1 << this.F1) / yt, e = 1 << this.F2;
          var i = r.t, j = i - ys, t2 = q == null ? nbi() : q;
          y.dlShiftTo(j, t2);
          if (r.compareTo(t2) >= 0) {
            r[r.t++] = 1;
            r.subTo(t2, r);
          }
          BigInteger.ONE.dlShiftTo(ys, t2);
          t2.subTo(y, y);
          while (y.t < ys) y[y.t++] = 0;
          while (--j >= 0) {
            var qd = r[--i] == y0 ? this.DM : Math.floor(r[i] * d1 + (r[i - 1] + e) * d2);
            if ((r[i] += y.am(0, qd, r, j, 0, ys)) < qd) {
              y.dlShiftTo(j, t2);
              r.subTo(t2, r);
              while (r[i] < --qd) r.subTo(t2, r);
            }
          }
          if (q != null) {
            r.drShiftTo(ys, q);
            if (ts != ms) BigInteger.ZERO.subTo(q, q);
          }
          r.t = ys;
          r.clamp();
          if (nsh > 0) r.rShiftTo(nsh, r);
          if (ts < 0) BigInteger.ZERO.subTo(r, r);
        }
        function bnMod(a) {
          var r = nbi();
          this.abs().divRemTo(a, null, r);
          if (this.s < 0 && r.compareTo(BigInteger.ZERO) > 0) a.subTo(r, r);
          return r;
        }
        function Classic(m) {
          this.m = m;
        }
        function cConvert(x) {
          if (x.s < 0 || x.compareTo(this.m) >= 0) return x.mod(this.m);
          else return x;
        }
        function cRevert(x) {
          return x;
        }
        function cReduce(x) {
          x.divRemTo(this.m, null, x);
        }
        function cMulTo(x, y, r) {
          x.multiplyTo(y, r);
          this.reduce(r);
        }
        function cSqrTo(x, r) {
          x.squareTo(r);
          this.reduce(r);
        }
        Classic.prototype.convert = cConvert;
        Classic.prototype.revert = cRevert;
        Classic.prototype.reduce = cReduce;
        Classic.prototype.mulTo = cMulTo;
        Classic.prototype.sqrTo = cSqrTo;
        function bnpInvDigit() {
          if (this.t < 1) return 0;
          var x = this[0];
          if ((x & 1) == 0) return 0;
          var y = x & 3;
          y = y * (2 - (x & 15) * y) & 15;
          y = y * (2 - (x & 255) * y) & 255;
          y = y * (2 - ((x & 65535) * y & 65535)) & 65535;
          y = y * (2 - x * y % this.DV) % this.DV;
          return y > 0 ? this.DV - y : -y;
        }
        function Montgomery(m) {
          this.m = m;
          this.mp = m.invDigit();
          this.mpl = this.mp & 32767;
          this.mph = this.mp >> 15;
          this.um = (1 << m.DB - 15) - 1;
          this.mt2 = 2 * m.t;
        }
        function montConvert(x) {
          var r = nbi();
          x.abs().dlShiftTo(this.m.t, r);
          r.divRemTo(this.m, null, r);
          if (x.s < 0 && r.compareTo(BigInteger.ZERO) > 0) this.m.subTo(r, r);
          return r;
        }
        function montRevert(x) {
          var r = nbi();
          x.copyTo(r);
          this.reduce(r);
          return r;
        }
        function montReduce(x) {
          while (x.t <= this.mt2)
            x[x.t++] = 0;
          for (var i = 0; i < this.m.t; ++i) {
            var j = x[i] & 32767;
            var u0 = j * this.mpl + ((j * this.mph + (x[i] >> 15) * this.mpl & this.um) << 15) & x.DM;
            j = i + this.m.t;
            x[j] += this.m.am(0, u0, x, i, 0, this.m.t);
            while (x[j] >= x.DV) {
              x[j] -= x.DV;
              x[++j]++;
            }
          }
          x.clamp();
          x.drShiftTo(this.m.t, x);
          if (x.compareTo(this.m) >= 0) x.subTo(this.m, x);
        }
        function montSqrTo(x, r) {
          x.squareTo(r);
          this.reduce(r);
        }
        function montMulTo(x, y, r) {
          x.multiplyTo(y, r);
          this.reduce(r);
        }
        Montgomery.prototype.convert = montConvert;
        Montgomery.prototype.revert = montRevert;
        Montgomery.prototype.reduce = montReduce;
        Montgomery.prototype.mulTo = montMulTo;
        Montgomery.prototype.sqrTo = montSqrTo;
        function bnpIsEven() {
          return (this.t > 0 ? this[0] & 1 : this.s) == 0;
        }
        function bnpExp(e, z2) {
          if (e > 4294967295 || e < 1) return BigInteger.ONE;
          var r = nbi(), r2 = nbi(), g = z2.convert(this), i = nbits(e) - 1;
          g.copyTo(r);
          while (--i >= 0) {
            z2.sqrTo(r, r2);
            if ((e & 1 << i) > 0) z2.mulTo(r2, g, r);
            else {
              var t2 = r;
              r = r2;
              r2 = t2;
            }
          }
          return z2.revert(r);
        }
        function bnModPowInt(e, m) {
          var z2;
          if (e < 256 || m.isEven()) z2 = new Classic(m);
          else z2 = new Montgomery(m);
          return this.exp(e, z2);
        }
        BigInteger.prototype.copyTo = bnpCopyTo;
        BigInteger.prototype.fromInt = bnpFromInt;
        BigInteger.prototype.fromString = bnpFromString;
        BigInteger.prototype.clamp = bnpClamp;
        BigInteger.prototype.dlShiftTo = bnpDLShiftTo;
        BigInteger.prototype.drShiftTo = bnpDRShiftTo;
        BigInteger.prototype.lShiftTo = bnpLShiftTo;
        BigInteger.prototype.rShiftTo = bnpRShiftTo;
        BigInteger.prototype.subTo = bnpSubTo;
        BigInteger.prototype.multiplyTo = bnpMultiplyTo;
        BigInteger.prototype.squareTo = bnpSquareTo;
        BigInteger.prototype.divRemTo = bnpDivRemTo;
        BigInteger.prototype.invDigit = bnpInvDigit;
        BigInteger.prototype.isEven = bnpIsEven;
        BigInteger.prototype.exp = bnpExp;
        BigInteger.prototype.toString = bnToString;
        BigInteger.prototype.negate = bnNegate;
        BigInteger.prototype.abs = bnAbs;
        BigInteger.prototype.compareTo = bnCompareTo;
        BigInteger.prototype.bitLength = bnBitLength;
        BigInteger.prototype.mod = bnMod;
        BigInteger.prototype.modPowInt = bnModPowInt;
        BigInteger.ZERO = nbv(0);
        BigInteger.ONE = nbv(1);
        function bnClone() {
          var r = nbi();
          this.copyTo(r);
          return r;
        }
        function bnIntValue() {
          if (this.s < 0) {
            if (this.t == 1) return this[0] - this.DV;
            else if (this.t == 0) return -1;
          } else if (this.t == 1) return this[0];
          else if (this.t == 0) return 0;
          return (this[1] & (1 << 32 - this.DB) - 1) << this.DB | this[0];
        }
        function bnByteValue() {
          return this.t == 0 ? this.s : this[0] << 24 >> 24;
        }
        function bnShortValue() {
          return this.t == 0 ? this.s : this[0] << 16 >> 16;
        }
        function bnpChunkSize(r) {
          return Math.floor(Math.LN2 * this.DB / Math.log(r));
        }
        function bnSigNum() {
          if (this.s < 0) return -1;
          else if (this.t <= 0 || this.t == 1 && this[0] <= 0) return 0;
          else return 1;
        }
        function bnpToRadix(b) {
          if (b == null) b = 10;
          if (this.signum() == 0 || b < 2 || b > 36) return "0";
          var cs = this.chunkSize(b);
          var a = Math.pow(b, cs);
          var d = nbv(a), y = nbi(), z2 = nbi(), r = "";
          this.divRemTo(d, y, z2);
          while (y.signum() > 0) {
            r = (a + z2.intValue()).toString(b).substr(1) + r;
            y.divRemTo(d, y, z2);
          }
          return z2.intValue().toString(b) + r;
        }
        function bnpFromRadix(s, b) {
          this.fromInt(0);
          if (b == null) b = 10;
          var cs = this.chunkSize(b);
          var d = Math.pow(b, cs), mi = false, j = 0, w = 0;
          for (var i = 0; i < s.length; ++i) {
            var x = intAt(s, i);
            if (x < 0) {
              if (s.charAt(i) == "-" && this.signum() == 0) mi = true;
              continue;
            }
            w = b * w + x;
            if (++j >= cs) {
              this.dMultiply(d);
              this.dAddOffset(w, 0);
              j = 0;
              w = 0;
            }
          }
          if (j > 0) {
            this.dMultiply(Math.pow(b, j));
            this.dAddOffset(w, 0);
          }
          if (mi) BigInteger.ZERO.subTo(this, this);
        }
        function bnpFromNumber(a, b, c) {
          if ("number" == typeof b) {
            if (a < 2) this.fromInt(1);
            else {
              this.fromNumber(a, c);
              if (!this.testBit(a - 1))
                this.bitwiseTo(BigInteger.ONE.shiftLeft(a - 1), op_or, this);
              if (this.isEven()) this.dAddOffset(1, 0);
              while (!this.isProbablePrime(b)) {
                this.dAddOffset(2, 0);
                if (this.bitLength() > a) this.subTo(BigInteger.ONE.shiftLeft(a - 1), this);
              }
            }
          } else {
            var x = new Array(), t2 = a & 7;
            x.length = (a >> 3) + 1;
            b.nextBytes(x);
            if (t2 > 0) x[0] &= (1 << t2) - 1;
            else x[0] = 0;
            this.fromString(x, 256);
          }
        }
        function bnToByteArray() {
          var i = this.t, r = new Array();
          r[0] = this.s;
          var p = this.DB - i * this.DB % 8, d, k = 0;
          if (i-- > 0) {
            if (p < this.DB && (d = this[i] >> p) != (this.s & this.DM) >> p)
              r[k++] = d | this.s << this.DB - p;
            while (i >= 0) {
              if (p < 8) {
                d = (this[i] & (1 << p) - 1) << 8 - p;
                d |= this[--i] >> (p += this.DB - 8);
              } else {
                d = this[i] >> (p -= 8) & 255;
                if (p <= 0) {
                  p += this.DB;
                  --i;
                }
              }
              if ((d & 128) != 0) d |= -256;
              if (k == 0 && (this.s & 128) != (d & 128)) ++k;
              if (k > 0 || d != this.s) r[k++] = d;
            }
          }
          return r;
        }
        function bnEquals(a) {
          return this.compareTo(a) == 0;
        }
        function bnMin(a) {
          return this.compareTo(a) < 0 ? this : a;
        }
        function bnMax(a) {
          return this.compareTo(a) > 0 ? this : a;
        }
        function bnpBitwiseTo(a, op, r) {
          var i, f, m = Math.min(a.t, this.t);
          for (i = 0; i < m; ++i) r[i] = op(this[i], a[i]);
          if (a.t < this.t) {
            f = a.s & this.DM;
            for (i = m; i < this.t; ++i) r[i] = op(this[i], f);
            r.t = this.t;
          } else {
            f = this.s & this.DM;
            for (i = m; i < a.t; ++i) r[i] = op(f, a[i]);
            r.t = a.t;
          }
          r.s = op(this.s, a.s);
          r.clamp();
        }
        function op_and(x, y) {
          return x & y;
        }
        function bnAnd(a) {
          var r = nbi();
          this.bitwiseTo(a, op_and, r);
          return r;
        }
        function op_or(x, y) {
          return x | y;
        }
        function bnOr(a) {
          var r = nbi();
          this.bitwiseTo(a, op_or, r);
          return r;
        }
        function op_xor(x, y) {
          return x ^ y;
        }
        function bnXor(a) {
          var r = nbi();
          this.bitwiseTo(a, op_xor, r);
          return r;
        }
        function op_andnot(x, y) {
          return x & ~y;
        }
        function bnAndNot(a) {
          var r = nbi();
          this.bitwiseTo(a, op_andnot, r);
          return r;
        }
        function bnNot() {
          var r = nbi();
          for (var i = 0; i < this.t; ++i) r[i] = this.DM & ~this[i];
          r.t = this.t;
          r.s = ~this.s;
          return r;
        }
        function bnShiftLeft(n) {
          var r = nbi();
          if (n < 0) this.rShiftTo(-n, r);
          else this.lShiftTo(n, r);
          return r;
        }
        function bnShiftRight(n) {
          var r = nbi();
          if (n < 0) this.lShiftTo(-n, r);
          else this.rShiftTo(n, r);
          return r;
        }
        function lbit(x) {
          if (x == 0) return -1;
          var r = 0;
          if ((x & 65535) == 0) {
            x >>= 16;
            r += 16;
          }
          if ((x & 255) == 0) {
            x >>= 8;
            r += 8;
          }
          if ((x & 15) == 0) {
            x >>= 4;
            r += 4;
          }
          if ((x & 3) == 0) {
            x >>= 2;
            r += 2;
          }
          if ((x & 1) == 0) ++r;
          return r;
        }
        function bnGetLowestSetBit() {
          for (var i = 0; i < this.t; ++i)
            if (this[i] != 0) return i * this.DB + lbit(this[i]);
          if (this.s < 0) return this.t * this.DB;
          return -1;
        }
        function cbit(x) {
          var r = 0;
          while (x != 0) {
            x &= x - 1;
            ++r;
          }
          return r;
        }
        function bnBitCount() {
          var r = 0, x = this.s & this.DM;
          for (var i = 0; i < this.t; ++i) r += cbit(this[i] ^ x);
          return r;
        }
        function bnTestBit(n) {
          var j = Math.floor(n / this.DB);
          if (j >= this.t) return this.s != 0;
          return (this[j] & 1 << n % this.DB) != 0;
        }
        function bnpChangeBit(n, op) {
          var r = BigInteger.ONE.shiftLeft(n);
          this.bitwiseTo(r, op, r);
          return r;
        }
        function bnSetBit(n) {
          return this.changeBit(n, op_or);
        }
        function bnClearBit(n) {
          return this.changeBit(n, op_andnot);
        }
        function bnFlipBit(n) {
          return this.changeBit(n, op_xor);
        }
        function bnpAddTo(a, r) {
          var i = 0, c = 0, m = Math.min(a.t, this.t);
          while (i < m) {
            c += this[i] + a[i];
            r[i++] = c & this.DM;
            c >>= this.DB;
          }
          if (a.t < this.t) {
            c += a.s;
            while (i < this.t) {
              c += this[i];
              r[i++] = c & this.DM;
              c >>= this.DB;
            }
            c += this.s;
          } else {
            c += this.s;
            while (i < a.t) {
              c += a[i];
              r[i++] = c & this.DM;
              c >>= this.DB;
            }
            c += a.s;
          }
          r.s = c < 0 ? -1 : 0;
          if (c > 0) r[i++] = c;
          else if (c < -1) r[i++] = this.DV + c;
          r.t = i;
          r.clamp();
        }
        function bnAdd(a) {
          var r = nbi();
          this.addTo(a, r);
          return r;
        }
        function bnSubtract(a) {
          var r = nbi();
          this.subTo(a, r);
          return r;
        }
        function bnMultiply(a) {
          var r = nbi();
          this.multiplyTo(a, r);
          return r;
        }
        function bnSquare() {
          var r = nbi();
          this.squareTo(r);
          return r;
        }
        function bnDivide(a) {
          var r = nbi();
          this.divRemTo(a, r, null);
          return r;
        }
        function bnRemainder(a) {
          var r = nbi();
          this.divRemTo(a, null, r);
          return r;
        }
        function bnDivideAndRemainder(a) {
          var q = nbi(), r = nbi();
          this.divRemTo(a, q, r);
          return new Array(q, r);
        }
        function bnpDMultiply(n) {
          this[this.t] = this.am(0, n - 1, this, 0, 0, this.t);
          ++this.t;
          this.clamp();
        }
        function bnpDAddOffset(n, w) {
          if (n == 0) return;
          while (this.t <= w) this[this.t++] = 0;
          this[w] += n;
          while (this[w] >= this.DV) {
            this[w] -= this.DV;
            if (++w >= this.t) this[this.t++] = 0;
            ++this[w];
          }
        }
        function NullExp() {
        }
        function nNop(x) {
          return x;
        }
        function nMulTo(x, y, r) {
          x.multiplyTo(y, r);
        }
        function nSqrTo(x, r) {
          x.squareTo(r);
        }
        NullExp.prototype.convert = nNop;
        NullExp.prototype.revert = nNop;
        NullExp.prototype.mulTo = nMulTo;
        NullExp.prototype.sqrTo = nSqrTo;
        function bnPow(e) {
          return this.exp(e, new NullExp());
        }
        function bnpMultiplyLowerTo(a, n, r) {
          var i = Math.min(this.t + a.t, n);
          r.s = 0;
          r.t = i;
          while (i > 0) r[--i] = 0;
          var j;
          for (j = r.t - this.t; i < j; ++i) r[i + this.t] = this.am(0, a[i], r, i, 0, this.t);
          for (j = Math.min(a.t, n); i < j; ++i) this.am(0, a[i], r, i, 0, n - i);
          r.clamp();
        }
        function bnpMultiplyUpperTo(a, n, r) {
          --n;
          var i = r.t = this.t + a.t - n;
          r.s = 0;
          while (--i >= 0) r[i] = 0;
          for (i = Math.max(n - this.t, 0); i < a.t; ++i)
            r[this.t + i - n] = this.am(n - i, a[i], r, 0, 0, this.t + i - n);
          r.clamp();
          r.drShiftTo(1, r);
        }
        function Barrett(m) {
          this.r2 = nbi();
          this.q3 = nbi();
          BigInteger.ONE.dlShiftTo(2 * m.t, this.r2);
          this.mu = this.r2.divide(m);
          this.m = m;
        }
        function barrettConvert(x) {
          if (x.s < 0 || x.t > 2 * this.m.t) return x.mod(this.m);
          else if (x.compareTo(this.m) < 0) return x;
          else {
            var r = nbi();
            x.copyTo(r);
            this.reduce(r);
            return r;
          }
        }
        function barrettRevert(x) {
          return x;
        }
        function barrettReduce(x) {
          x.drShiftTo(this.m.t - 1, this.r2);
          if (x.t > this.m.t + 1) {
            x.t = this.m.t + 1;
            x.clamp();
          }
          this.mu.multiplyUpperTo(this.r2, this.m.t + 1, this.q3);
          this.m.multiplyLowerTo(this.q3, this.m.t + 1, this.r2);
          while (x.compareTo(this.r2) < 0) x.dAddOffset(1, this.m.t + 1);
          x.subTo(this.r2, x);
          while (x.compareTo(this.m) >= 0) x.subTo(this.m, x);
        }
        function barrettSqrTo(x, r) {
          x.squareTo(r);
          this.reduce(r);
        }
        function barrettMulTo(x, y, r) {
          x.multiplyTo(y, r);
          this.reduce(r);
        }
        Barrett.prototype.convert = barrettConvert;
        Barrett.prototype.revert = barrettRevert;
        Barrett.prototype.reduce = barrettReduce;
        Barrett.prototype.mulTo = barrettMulTo;
        Barrett.prototype.sqrTo = barrettSqrTo;
        function bnModPow(e, m) {
          var i = e.bitLength(), k, r = nbv(1), z2;
          if (i <= 0) return r;
          else if (i < 18) k = 1;
          else if (i < 48) k = 3;
          else if (i < 144) k = 4;
          else if (i < 768) k = 5;
          else k = 6;
          if (i < 8)
            z2 = new Classic(m);
          else if (m.isEven())
            z2 = new Barrett(m);
          else
            z2 = new Montgomery(m);
          var g = new Array(), n = 3, k1 = k - 1, km = (1 << k) - 1;
          g[1] = z2.convert(this);
          if (k > 1) {
            var g2 = nbi();
            z2.sqrTo(g[1], g2);
            while (n <= km) {
              g[n] = nbi();
              z2.mulTo(g2, g[n - 2], g[n]);
              n += 2;
            }
          }
          var j = e.t - 1, w, is1 = true, r2 = nbi(), t2;
          i = nbits(e[j]) - 1;
          while (j >= 0) {
            if (i >= k1) w = e[j] >> i - k1 & km;
            else {
              w = (e[j] & (1 << i + 1) - 1) << k1 - i;
              if (j > 0) w |= e[j - 1] >> this.DB + i - k1;
            }
            n = k;
            while ((w & 1) == 0) {
              w >>= 1;
              --n;
            }
            if ((i -= n) < 0) {
              i += this.DB;
              --j;
            }
            if (is1) {
              g[w].copyTo(r);
              is1 = false;
            } else {
              while (n > 1) {
                z2.sqrTo(r, r2);
                z2.sqrTo(r2, r);
                n -= 2;
              }
              if (n > 0) z2.sqrTo(r, r2);
              else {
                t2 = r;
                r = r2;
                r2 = t2;
              }
              z2.mulTo(r2, g[w], r);
            }
            while (j >= 0 && (e[j] & 1 << i) == 0) {
              z2.sqrTo(r, r2);
              t2 = r;
              r = r2;
              r2 = t2;
              if (--i < 0) {
                i = this.DB - 1;
                --j;
              }
            }
          }
          return z2.revert(r);
        }
        function bnGCD(a) {
          var x = this.s < 0 ? this.negate() : this.clone();
          var y = a.s < 0 ? a.negate() : a.clone();
          if (x.compareTo(y) < 0) {
            var t2 = x;
            x = y;
            y = t2;
          }
          var i = x.getLowestSetBit(), g = y.getLowestSetBit();
          if (g < 0) return x;
          if (i < g) g = i;
          if (g > 0) {
            x.rShiftTo(g, x);
            y.rShiftTo(g, y);
          }
          while (x.signum() > 0) {
            if ((i = x.getLowestSetBit()) > 0) x.rShiftTo(i, x);
            if ((i = y.getLowestSetBit()) > 0) y.rShiftTo(i, y);
            if (x.compareTo(y) >= 0) {
              x.subTo(y, x);
              x.rShiftTo(1, x);
            } else {
              y.subTo(x, y);
              y.rShiftTo(1, y);
            }
          }
          if (g > 0) y.lShiftTo(g, y);
          return y;
        }
        function bnpModInt(n) {
          if (n <= 0) return 0;
          var d = this.DV % n, r = this.s < 0 ? n - 1 : 0;
          if (this.t > 0)
            if (d == 0) r = this[0] % n;
            else for (var i = this.t - 1; i >= 0; --i) r = (d * r + this[i]) % n;
          return r;
        }
        function bnModInverse(m) {
          var ac = m.isEven();
          if (this.isEven() && ac || m.signum() == 0) return BigInteger.ZERO;
          var u = m.clone(), v = this.clone();
          var a = nbv(1), b = nbv(0), c = nbv(0), d = nbv(1);
          while (u.signum() != 0) {
            while (u.isEven()) {
              u.rShiftTo(1, u);
              if (ac) {
                if (!a.isEven() || !b.isEven()) {
                  a.addTo(this, a);
                  b.subTo(m, b);
                }
                a.rShiftTo(1, a);
              } else if (!b.isEven()) b.subTo(m, b);
              b.rShiftTo(1, b);
            }
            while (v.isEven()) {
              v.rShiftTo(1, v);
              if (ac) {
                if (!c.isEven() || !d.isEven()) {
                  c.addTo(this, c);
                  d.subTo(m, d);
                }
                c.rShiftTo(1, c);
              } else if (!d.isEven()) d.subTo(m, d);
              d.rShiftTo(1, d);
            }
            if (u.compareTo(v) >= 0) {
              u.subTo(v, u);
              if (ac) a.subTo(c, a);
              b.subTo(d, b);
            } else {
              v.subTo(u, v);
              if (ac) c.subTo(a, c);
              d.subTo(b, d);
            }
          }
          if (v.compareTo(BigInteger.ONE) != 0) return BigInteger.ZERO;
          if (d.compareTo(m) >= 0) return d.subtract(m);
          if (d.signum() < 0) d.addTo(m, d);
          else return d;
          if (d.signum() < 0) return d.add(m);
          else return d;
        }
        var lowprimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997];
        var lplim = (1 << 26) / lowprimes[lowprimes.length - 1];
        function bnIsProbablePrime(t2) {
          var i, x = this.abs();
          if (x.t == 1 && x[0] <= lowprimes[lowprimes.length - 1]) {
            for (i = 0; i < lowprimes.length; ++i)
              if (x[0] == lowprimes[i]) return true;
            return false;
          }
          if (x.isEven()) return false;
          i = 1;
          while (i < lowprimes.length) {
            var m = lowprimes[i], j = i + 1;
            while (j < lowprimes.length && m < lplim) m *= lowprimes[j++];
            m = x.modInt(m);
            while (i < j) if (m % lowprimes[i++] == 0) return false;
          }
          return x.millerRabin(t2);
        }
        function bnpMillerRabin(t2) {
          var n1 = this.subtract(BigInteger.ONE);
          var k = n1.getLowestSetBit();
          if (k <= 0) return false;
          var r = n1.shiftRight(k);
          t2 = t2 + 1 >> 1;
          if (t2 > lowprimes.length) t2 = lowprimes.length;
          var a = nbi();
          for (var i = 0; i < t2; ++i) {
            a.fromInt(lowprimes[Math.floor(Math.random() * lowprimes.length)]);
            var y = a.modPow(r, this);
            if (y.compareTo(BigInteger.ONE) != 0 && y.compareTo(n1) != 0) {
              var j = 1;
              while (j++ < k && y.compareTo(n1) != 0) {
                y = y.modPowInt(2, this);
                if (y.compareTo(BigInteger.ONE) == 0) return false;
              }
              if (y.compareTo(n1) != 0) return false;
            }
          }
          return true;
        }
        BigInteger.prototype.chunkSize = bnpChunkSize;
        BigInteger.prototype.toRadix = bnpToRadix;
        BigInteger.prototype.fromRadix = bnpFromRadix;
        BigInteger.prototype.fromNumber = bnpFromNumber;
        BigInteger.prototype.bitwiseTo = bnpBitwiseTo;
        BigInteger.prototype.changeBit = bnpChangeBit;
        BigInteger.prototype.addTo = bnpAddTo;
        BigInteger.prototype.dMultiply = bnpDMultiply;
        BigInteger.prototype.dAddOffset = bnpDAddOffset;
        BigInteger.prototype.multiplyLowerTo = bnpMultiplyLowerTo;
        BigInteger.prototype.multiplyUpperTo = bnpMultiplyUpperTo;
        BigInteger.prototype.modInt = bnpModInt;
        BigInteger.prototype.millerRabin = bnpMillerRabin;
        BigInteger.prototype.clone = bnClone;
        BigInteger.prototype.intValue = bnIntValue;
        BigInteger.prototype.byteValue = bnByteValue;
        BigInteger.prototype.shortValue = bnShortValue;
        BigInteger.prototype.signum = bnSigNum;
        BigInteger.prototype.toByteArray = bnToByteArray;
        BigInteger.prototype.equals = bnEquals;
        BigInteger.prototype.min = bnMin;
        BigInteger.prototype.max = bnMax;
        BigInteger.prototype.and = bnAnd;
        BigInteger.prototype.or = bnOr;
        BigInteger.prototype.xor = bnXor;
        BigInteger.prototype.andNot = bnAndNot;
        BigInteger.prototype.not = bnNot;
        BigInteger.prototype.shiftLeft = bnShiftLeft;
        BigInteger.prototype.shiftRight = bnShiftRight;
        BigInteger.prototype.getLowestSetBit = bnGetLowestSetBit;
        BigInteger.prototype.bitCount = bnBitCount;
        BigInteger.prototype.testBit = bnTestBit;
        BigInteger.prototype.setBit = bnSetBit;
        BigInteger.prototype.clearBit = bnClearBit;
        BigInteger.prototype.flipBit = bnFlipBit;
        BigInteger.prototype.add = bnAdd;
        BigInteger.prototype.subtract = bnSubtract;
        BigInteger.prototype.multiply = bnMultiply;
        BigInteger.prototype.divide = bnDivide;
        BigInteger.prototype.remainder = bnRemainder;
        BigInteger.prototype.divideAndRemainder = bnDivideAndRemainder;
        BigInteger.prototype.modPow = bnModPow;
        BigInteger.prototype.modInverse = bnModInverse;
        BigInteger.prototype.pow = bnPow;
        BigInteger.prototype.gcd = bnGCD;
        BigInteger.prototype.isProbablePrime = bnIsProbablePrime;
        BigInteger.prototype.square = bnSquare;
        BigInteger.prototype.Barrett = Barrett;
        var rng_state;
        var rng_pool;
        var rng_pptr;
        function rng_seed_int(x) {
          rng_pool[rng_pptr++] ^= x & 255;
          rng_pool[rng_pptr++] ^= x >> 8 & 255;
          rng_pool[rng_pptr++] ^= x >> 16 & 255;
          rng_pool[rng_pptr++] ^= x >> 24 & 255;
          if (rng_pptr >= rng_psize) rng_pptr -= rng_psize;
        }
        function rng_seed_time() {
          rng_seed_int((/* @__PURE__ */ new Date()).getTime());
        }
        if (rng_pool == null) {
          rng_pool = new Array();
          rng_pptr = 0;
          var t;
          if (typeof window !== "undefined" && window.crypto) {
            if (window.crypto.getRandomValues) {
              var ua = new Uint8Array(32);
              window.crypto.getRandomValues(ua);
              for (t = 0; t < 32; ++t)
                rng_pool[rng_pptr++] = ua[t];
            } else if (navigator.appName == "Netscape" && navigator.appVersion < "5") {
              var z = window.crypto.random(32);
              for (t = 0; t < z.length; ++t)
                rng_pool[rng_pptr++] = z.charCodeAt(t) & 255;
            }
          }
          while (rng_pptr < rng_psize) {
            t = Math.floor(65536 * Math.random());
            rng_pool[rng_pptr++] = t >>> 8;
            rng_pool[rng_pptr++] = t & 255;
          }
          rng_pptr = 0;
          rng_seed_time();
        }
        function rng_get_byte() {
          if (rng_state == null) {
            rng_seed_time();
            rng_state = prng_newstate();
            rng_state.init(rng_pool);
            for (rng_pptr = 0; rng_pptr < rng_pool.length; ++rng_pptr)
              rng_pool[rng_pptr] = 0;
            rng_pptr = 0;
          }
          return rng_state.next();
        }
        function rng_get_bytes(ba) {
          var i;
          for (i = 0; i < ba.length; ++i) ba[i] = rng_get_byte();
        }
        function SecureRandom() {
        }
        SecureRandom.prototype.nextBytes = rng_get_bytes;
        function Arcfour() {
          this.i = 0;
          this.j = 0;
          this.S = new Array();
        }
        function ARC4init(key) {
          var i, j, t2;
          for (i = 0; i < 256; ++i)
            this.S[i] = i;
          j = 0;
          for (i = 0; i < 256; ++i) {
            j = j + this.S[i] + key[i % key.length] & 255;
            t2 = this.S[i];
            this.S[i] = this.S[j];
            this.S[j] = t2;
          }
          this.i = 0;
          this.j = 0;
        }
        function ARC4next() {
          var t2;
          this.i = this.i + 1 & 255;
          this.j = this.j + this.S[this.i] & 255;
          t2 = this.S[this.i];
          this.S[this.i] = this.S[this.j];
          this.S[this.j] = t2;
          return this.S[t2 + this.S[this.i] & 255];
        }
        Arcfour.prototype.init = ARC4init;
        Arcfour.prototype.next = ARC4next;
        function prng_newstate() {
          return new Arcfour();
        }
        var rng_psize = 256;
        if (typeof exports !== "undefined") {
          exports = module.exports = {
            default: BigInteger,
            BigInteger,
            SecureRandom
          };
        } else {
          this.jsbn = {
            BigInteger,
            SecureRandom
          };
        }
      }).call(exports);
    }
  });

  // node_modules/miniprogram-sm-crypto/miniprogram_dist/index.js
  var require_miniprogram_dist = __commonJS({
    "node_modules/miniprogram-sm-crypto/miniprogram_dist/index.js"(exports, module) {
      "use strict";
      var t = require_typeof();
      module.exports = (function(e) {
        var r = {};
        function n(t2) {
          if (r[t2])
            return r[t2].exports;
          var i = r[t2] = {
            i: t2,
            l: false,
            exports: {}
          };
          return e[t2].call(i.exports, i, i.exports, n), i.l = true, i.exports;
        }
        return n.m = e, n.c = r, n.d = function(t2, e2, r2) {
          n.o(t2, e2) || Object.defineProperty(t2, e2, {
            enumerable: true,
            get: r2
          });
        }, n.r = function(t2) {
          "undefined" != typeof Symbol && Symbol.toStringTag && Object.defineProperty(t2, Symbol.toStringTag, {
            value: "Module"
          }), Object.defineProperty(t2, "__esModule", {
            value: true
          });
        }, n.t = function(e2, r2) {
          if (1 & r2 && (e2 = n(e2)), 8 & r2)
            return e2;
          if (4 & r2 && "object" === t(e2) && e2 && e2.__esModule)
            return e2;
          var i = /* @__PURE__ */ Object.create(null);
          if (n.r(i), Object.defineProperty(i, "default", {
            enumerable: true,
            value: e2
          }), 2 & r2 && "string" != typeof e2)
            for (var o in e2)
              n.d(i, o, function(t2) {
                return e2[t2];
              }.bind(null, o));
          return i;
        }, n.n = function(t2) {
          var e2 = t2 && t2.__esModule ? function() {
            return t2.default;
          } : function() {
            return t2;
          };
          return n.d(e2, "a", e2), e2;
        }, n.o = function(t2, e2) {
          return Object.prototype.hasOwnProperty.call(t2, e2);
        }, n.p = "", n(n.s = 2);
      })([
        function(t2, e) {
          t2.exports = require_jsbn();
        },
        function(t2, e, r) {
          var n = new Uint32Array(68), i = new Uint32Array(64);
          function o(t3, e2) {
            var r2 = 31 & e2;
            return t3 << r2 | t3 >>> 32 - r2;
          }
          function u(t3, e2) {
            for (var r2 = [], n2 = t3.length - 1; n2 >= 0; n2--)
              r2[n2] = 255 & (t3[n2] ^ e2[n2]);
            return r2;
          }
          function s(t3) {
            return t3 ^ o(t3, 9) ^ o(t3, 17);
          }
          function a(t3) {
            var e2 = 8 * t3.length, r2 = e2 % 512;
            r2 = r2 >= 448 ? 512 - r2 % 448 - 1 : 448 - r2 - 1;
            for (var u2 = new Array((r2 - 7) / 8), a2 = new Array(8), l2 = 0, c2 = u2.length; l2 < c2; l2++)
              u2[l2] = 0;
            for (var f2 = 0, h = a2.length; f2 < h; f2++)
              a2[f2] = 0;
            e2 = e2.toString(2);
            for (var g = 7; g >= 0; g--)
              if (e2.length > 8) {
                var p = e2.length - 8;
                a2[g] = parseInt(e2.substr(p), 2), e2 = e2.substr(0, p);
              } else
                e2.length > 0 && (a2[g] = parseInt(e2, 2), e2 = "");
            for (var d, v = new Uint8Array([].concat(t3, [128], u2, a2)), y = new DataView(v.buffer, 0), F = v.length / 64, m = new Uint32Array([1937774191, 1226093241, 388252375, 3666478592, 2842636476, 372324522, 3817729613, 2969243214]), w = 0; w < F; w++) {
              n.fill(0), i.fill(0);
              for (var b = 16 * w, x = 0; x < 16; x++)
                n[x] = y.getUint32(4 * (b + x), false);
              for (var I = 16; I < 68; I++)
                n[I] = (d = n[I - 16] ^ n[I - 9] ^ o(n[I - 3], 15)) ^ o(d, 15) ^ o(d, 23) ^ o(n[I - 13], 7) ^ n[I - 6];
              for (var B = 0; B < 64; B++)
                i[B] = n[B] ^ n[B + 4];
              for (var q = m[0], P = m[1], E = m[2], A = m[3], H = m[4], C = m[5], S = m[6], T = m[7], O = void 0, R = void 0, K = void 0, j = void 0, z = 0; z < 64; z++)
                j = z >= 0 && z <= 15 ? 2043430169 : 2055708042, R = (z >= 0 && z <= 15 ? q ^ P ^ E : q & P | q & E | P & E) + A + ((O = o(o(q, 12) + H + o(j, z), 7)) ^ o(q, 12)) + i[z], K = (z >= 0 && z <= 15 ? H ^ C ^ S : H & C | ~H & S) + T + O + n[z], A = E, E = o(P, 9), P = q, q = R, T = S, S = o(C, 19), C = H, H = s(K);
              m[0] ^= q, m[1] ^= P, m[2] ^= E, m[3] ^= A, m[4] ^= H, m[5] ^= C, m[6] ^= S, m[7] ^= T;
            }
            for (var D = [], U = 0, k = m.length; U < k; U++) {
              var X = m[U];
              D.push((4278190080 & X) >>> 24, (16711680 & X) >>> 16, (65280 & X) >>> 8, 255 & X);
            }
            return D;
          }
          for (var l = new Uint8Array(64), c = new Uint8Array(64), f = 0; f < 64; f++)
            l[f] = 54, c[f] = 92;
          t2.exports = {
            sm3: a,
            hmac: function(t3, e2) {
              for (e2.length > 64 && (e2 = a(e2)); e2.length < 64; )
                e2.push(0);
              var r2 = u(e2, l), n2 = u(e2, c), i2 = a([].concat(r2, t3));
              return a([].concat(n2, i2));
            }
          };
        },
        function(t2, e, r) {
          t2.exports = {
            sm2: r(3),
            sm3: r(7),
            sm4: r(8)
          };
        },
        function(t2, e, r) {
          var n = r(0).BigInteger, i = r(4), o = i.encodeDer, u = i.decodeDer, s = r(5), a = r(1).sm3, l = s.generateEcparam(), c = l.G, f = l.curve, h = l.n;
          function g(t3, e2) {
            var r2 = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : "1234567812345678";
            r2 = s.utf8ToHex(r2);
            var n2 = s.leftPad(c.curve.a.toBigInteger().toRadix(16), 64), i2 = s.leftPad(c.curve.b.toBigInteger().toRadix(16), 64), o2 = s.leftPad(c.getX().toBigInteger().toRadix(16), 64), u2 = s.leftPad(c.getY().toBigInteger().toRadix(16), 64), l2 = void 0, f2 = void 0;
            if (128 === e2.length)
              l2 = e2.substr(0, 64), f2 = e2.substr(64, 64);
            else {
              var h2 = c.curve.decodePointHex(e2);
              l2 = s.leftPad(h2.getX().toBigInteger().toRadix(16), 64), f2 = s.leftPad(h2.getY().toBigInteger().toRadix(16), 64);
            }
            var g2 = s.hexToArray(r2 + n2 + i2 + o2 + u2 + l2 + f2), p2 = 4 * r2.length;
            g2.unshift(255 & p2), g2.unshift(p2 >> 8 & 255);
            var d2 = a(g2);
            return s.arrayToHex(a(d2.concat(s.hexToArray(t3))));
          }
          function p(t3) {
            var e2 = c.multiply(new n(t3, 16));
            return "04" + s.leftPad(e2.getX().toBigInteger().toString(16), 64) + s.leftPad(e2.getY().toBigInteger().toString(16), 64);
          }
          function d() {
            var t3 = s.generateKeyPairHex(), e2 = f.decodePointHex(t3.publicKey);
            return t3.k = new n(t3.privateKey, 16), t3.x1 = e2.getX().toBigInteger(), t3;
          }
          t2.exports = {
            generateKeyPairHex: s.generateKeyPairHex,
            compressPublicKeyHex: s.compressPublicKeyHex,
            comparePublicKeyHex: s.comparePublicKeyHex,
            doEncrypt: function(t3, e2) {
              var r2 = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : 1;
              t3 = "string" == typeof t3 ? s.hexToArray(s.utf8ToHex(t3)) : Array.prototype.slice.call(t3), e2 = s.getGlobalCurve().decodePointHex(e2);
              var i2 = s.generateKeyPairHex(), o2 = new n(i2.privateKey, 16), u2 = i2.publicKey;
              u2.length > 128 && (u2 = u2.substr(u2.length - 128));
              var l2 = e2.multiply(o2), c2 = s.hexToArray(s.leftPad(l2.getX().toBigInteger().toRadix(16), 64)), f2 = s.hexToArray(s.leftPad(l2.getY().toBigInteger().toRadix(16), 64)), h2 = s.arrayToHex(a([].concat(c2, t3, f2))), g2 = 1, p2 = 0, d2 = [], v = [].concat(c2, f2), y = function() {
                d2 = a([].concat(v, [g2 >> 24 & 255, g2 >> 16 & 255, g2 >> 8 & 255, 255 & g2])), g2++, p2 = 0;
              };
              y();
              for (var F = 0, m = t3.length; F < m; F++)
                p2 === d2.length && y(), t3[F] ^= 255 & d2[p2++];
              var w = s.arrayToHex(t3);
              return 0 === r2 ? u2 + w + h2 : u2 + h2 + w;
            },
            doDecrypt: function(t3, e2) {
              var r2 = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : 1, i2 = arguments.length > 3 && void 0 !== arguments[3] ? arguments[3] : {}, o2 = i2.output, u2 = void 0 === o2 ? "string" : o2;
              e2 = new n(e2, 16);
              var l2 = t3.substr(128, 64), c2 = t3.substr(192);
              0 === r2 && (l2 = t3.substr(t3.length - 64), c2 = t3.substr(128, t3.length - 128 - 64));
              var f2 = s.hexToArray(c2), h2 = s.getGlobalCurve().decodePointHex("04" + t3.substr(0, 128)), g2 = h2.multiply(e2), p2 = s.hexToArray(s.leftPad(g2.getX().toBigInteger().toRadix(16), 64)), d2 = s.hexToArray(s.leftPad(g2.getY().toBigInteger().toRadix(16), 64)), v = 1, y = 0, F = [], m = [].concat(p2, d2), w = function() {
                F = a([].concat(m, [v >> 24 & 255, v >> 16 & 255, v >> 8 & 255, 255 & v])), v++, y = 0;
              };
              w();
              for (var b = 0, x = f2.length; b < x; b++)
                y === F.length && w(), f2[b] ^= 255 & F[y++];
              var I = s.arrayToHex(a([].concat(p2, f2, d2)));
              return I === l2.toLowerCase() ? "array" === u2 ? f2 : s.arrayToUtf8(f2) : "array" === u2 ? [] : "";
            },
            doSignature: function(t3, e2) {
              var r2 = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : {}, i2 = r2.pointPool, u2 = r2.der, a2 = r2.hash, l2 = r2.publicKey, c2 = r2.userId, f2 = "string" == typeof t3 ? s.utf8ToHex(t3) : s.arrayToHex(t3);
              a2 && (f2 = g(f2, l2 = l2 || p(e2), c2));
              var v = new n(e2, 16), y = new n(f2, 16), F = null, m = null, w = null;
              do {
                do {
                  var b = void 0;
                  F = (b = i2 && i2.length ? i2.pop() : d()).k, m = y.add(b.x1).mod(h);
                } while (m.equals(n.ZERO) || m.add(F).equals(h));
                w = v.add(n.ONE).modInverse(h).multiply(F.subtract(m.multiply(v))).mod(h);
              } while (w.equals(n.ZERO));
              return u2 ? o(m, w) : s.leftPad(m.toString(16), 64) + s.leftPad(w.toString(16), 64);
            },
            doVerifySignature: function(t3, e2, r2) {
              var i2 = arguments.length > 3 && void 0 !== arguments[3] ? arguments[3] : {}, o2 = i2.der, a2 = i2.hash, l2 = i2.userId, p2 = "string" == typeof t3 ? s.utf8ToHex(t3) : s.arrayToHex(t3);
              a2 && (p2 = g(p2, r2, l2));
              var d2 = void 0, v = void 0;
              if (o2) {
                var y = u(e2);
                d2 = y.r, v = y.s;
              } else
                d2 = new n(e2.substring(0, 64), 16), v = new n(e2.substring(64), 16);
              var F = f.decodePointHex(r2), m = new n(p2, 16), w = d2.add(v).mod(h);
              if (w.equals(n.ZERO))
                return false;
              var b = c.multiply(v).add(F.multiply(w)), x = m.add(b.getX().toBigInteger()).mod(h);
              return d2.equals(x);
            },
            getPublicKeyFromPrivateKey: p,
            getPoint: d,
            verifyPublicKey: s.verifyPublicKey
          };
        },
        function(e, r, n) {
          function i(e2, r2) {
            if (!e2)
              throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return !r2 || "object" !== t(r2) && "function" != typeof r2 ? e2 : r2;
          }
          function o(e2, r2) {
            if ("function" != typeof r2 && null !== r2)
              throw new TypeError("Super expression must either be null or a function, not " + t(r2));
            e2.prototype = Object.create(r2 && r2.prototype, {
              constructor: {
                value: e2,
                enumerable: false,
                writable: true,
                configurable: true
              }
            }), r2 && (Object.setPrototypeOf ? Object.setPrototypeOf(e2, r2) : e2.__proto__ = r2);
          }
          function u(t2, e2) {
            if (!(t2 instanceof e2))
              throw new TypeError("Cannot call a class as a function");
          }
          var s = n(0).BigInteger;
          var a = (function() {
            function t2() {
              u(this, t2), this.tlv = null, this.t = "00", this.l = "00", this.v = "";
            }
            return t2.prototype.getEncodedHex = function() {
              return this.tlv || (this.v = this.getValue(), this.l = this.getLength(), this.tlv = this.t + this.l + this.v), this.tlv;
            }, t2.prototype.getLength = function() {
              var t3 = this.v.length / 2, e2 = t3.toString(16);
              return e2.length % 2 == 1 && (e2 = "0" + e2), t3 < 128 ? e2 : (128 + e2.length / 2).toString(16) + e2;
            }, t2.prototype.getValue = function() {
              return "";
            }, t2;
          })(), l = (function(t2) {
            function e2(r2) {
              u(this, e2);
              var n2 = i(this, t2.call(this));
              return n2.t = "02", r2 && (n2.v = (function(t3) {
                var e3 = t3.toString(16);
                if ("-" !== e3[0])
                  e3.length % 2 == 1 ? e3 = "0" + e3 : e3.match(/^[0-7]/) || (e3 = "00" + e3);
                else {
                  var r3 = (e3 = e3.substr(1)).length;
                  r3 % 2 == 1 ? r3 += 1 : e3.match(/^[0-7]/) || (r3 += 2);
                  for (var n3 = "", i2 = 0; i2 < r3; i2++)
                    n3 += "f";
                  e3 = (e3 = (n3 = new s(n3, 16)).xor(t3).add(s.ONE)).toString(16).replace(/^-/, "");
                }
                return e3;
              })(r2)), n2;
            }
            return o(e2, t2), e2.prototype.getValue = function() {
              return this.v;
            }, e2;
          })(a), c = (function(t2) {
            function e2(r2) {
              u(this, e2);
              var n2 = i(this, t2.call(this));
              return n2.t = "30", n2.asn1Array = r2, n2;
            }
            return o(e2, t2), e2.prototype.getValue = function() {
              return this.v = this.asn1Array.map((function(t3) {
                return t3.getEncodedHex();
              })).join(""), this.v;
            }, e2;
          })(a);
          function f(t2, e2) {
            return +t2[e2 + 2] < 8 ? 1 : 128 & +t2.substr(e2 + 2, 2);
          }
          function h(t2, e2) {
            var r2 = f(t2, e2), n2 = t2.substr(e2 + 2, 2 * r2);
            return n2 ? (+n2[0] < 8 ? new s(n2, 16) : new s(n2.substr(2), 16)).intValue() : -1;
          }
          function g(t2, e2) {
            return e2 + 2 * (f(t2, e2) + 1);
          }
          e.exports = {
            encodeDer: function(t2, e2) {
              var r2 = new l(t2), n2 = new l(e2);
              return new c([r2, n2]).getEncodedHex();
            },
            decodeDer: function(t2) {
              var e2 = g(t2, 0), r2 = g(t2, e2), n2 = h(t2, e2), i2 = t2.substr(r2, 2 * n2), o2 = r2 + i2.length, u2 = g(t2, o2), a2 = h(t2, o2), l2 = t2.substr(u2, 2 * a2);
              return {
                r: new s(i2, 16),
                s: new s(l2, 16)
              };
            }
          };
        },
        function(t2, e, r) {
          var n = r(0), i = n.BigInteger, o = n.SecureRandom, u = r(6).ECCurveFp, s = new o(), a = h(), l = a.curve, c = a.G, f = a.n;
          function h() {
            var t3 = new i("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF", 16), e2 = new i("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC", 16), r2 = new i("28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93", 16), n2 = new u(t3, e2, r2), o2 = n2.decodePointHex("0432C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7BC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0");
            return {
              curve: n2,
              G: o2,
              n: new i("FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123", 16)
            };
          }
          function g(t3, e2) {
            return t3.length >= e2 ? t3 : new Array(e2 - t3.length + 1).join("0") + t3;
          }
          t2.exports = {
            getGlobalCurve: function() {
              return l;
            },
            generateEcparam: h,
            generateKeyPairHex: function(t3, e2, r2) {
              var n2 = (t3 ? new i(t3, e2, r2) : new i(f.bitLength(), s)).mod(f.subtract(i.ONE)).add(i.ONE), o2 = g(n2.toString(16), 64), u2 = c.multiply(n2);
              return {
                privateKey: o2,
                publicKey: "04" + g(u2.getX().toBigInteger().toString(16), 64) + g(u2.getY().toBigInteger().toString(16), 64)
              };
            },
            compressPublicKeyHex: function(t3) {
              if (130 !== t3.length)
                throw new Error("Invalid public key to compress");
              var e2 = (t3.length - 2) / 2, r2 = t3.substr(2, e2), n2 = "03";
              return new i(t3.substr(e2 + 2, e2), 16).mod(new i("2")).equals(i.ZERO) && (n2 = "02"), n2 + r2;
            },
            utf8ToHex: function(t3) {
              for (var e2 = (t3 = unescape(encodeURIComponent(t3))).length, r2 = [], n2 = 0; n2 < e2; n2++)
                r2[n2 >>> 2] |= (255 & t3.charCodeAt(n2)) << 24 - n2 % 4 * 8;
              for (var i2 = [], o2 = 0; o2 < e2; o2++) {
                var u2 = r2[o2 >>> 2] >>> 24 - o2 % 4 * 8 & 255;
                i2.push((u2 >>> 4).toString(16)), i2.push((15 & u2).toString(16));
              }
              return i2.join("");
            },
            leftPad: g,
            arrayToHex: function(t3) {
              return t3.map((function(t4) {
                return 1 === (t4 = t4.toString(16)).length ? "0" + t4 : t4;
              })).join("");
            },
            arrayToUtf8: function(t3) {
              for (var e2 = [], r2 = 0, n2 = 0; n2 < 2 * t3.length; n2 += 2)
                e2[n2 >>> 3] |= parseInt(t3[r2], 10) << 24 - n2 % 8 * 4, r2++;
              try {
                for (var i2 = [], o2 = 0; o2 < t3.length; o2++) {
                  var u2 = e2[o2 >>> 2] >>> 24 - o2 % 4 * 8 & 255;
                  i2.push(String.fromCharCode(u2));
                }
                return decodeURIComponent(escape(i2.join("")));
              } catch (t4) {
                throw new Error("Malformed UTF-8 data");
              }
            },
            hexToArray: function(t3) {
              var e2 = [], r2 = t3.length;
              r2 % 2 != 0 && (t3 = g(t3, r2 + 1)), r2 = t3.length;
              for (var n2 = 0; n2 < r2; n2 += 2)
                e2.push(parseInt(t3.substr(n2, 2), 16));
              return e2;
            },
            verifyPublicKey: function(t3) {
              var e2 = l.decodePointHex(t3);
              if (!e2)
                return false;
              var r2 = e2.getX();
              return e2.getY().square().equals(r2.multiply(r2.square()).add(r2.multiply(l.a)).add(l.b));
            },
            comparePublicKeyHex: function(t3, e2) {
              var r2 = l.decodePointHex(t3);
              if (!r2)
                return false;
              var n2 = l.decodePointHex(e2);
              return !!n2 && r2.equals(n2);
            }
          };
        },
        function(t2, e, r) {
          function n(t3, e2) {
            if (!(t3 instanceof e2))
              throw new TypeError("Cannot call a class as a function");
          }
          var i = r(0).BigInteger, o = new i("2"), u = new i("3"), s = (function() {
            function t3(e2, r2) {
              n(this, t3), this.x = r2, this.q = e2;
            }
            return t3.prototype.equals = function(t4) {
              return t4 === this || this.q.equals(t4.q) && this.x.equals(t4.x);
            }, t3.prototype.toBigInteger = function() {
              return this.x;
            }, t3.prototype.negate = function() {
              return new t3(this.q, this.x.negate().mod(this.q));
            }, t3.prototype.add = function(e2) {
              return new t3(this.q, this.x.add(e2.toBigInteger()).mod(this.q));
            }, t3.prototype.subtract = function(e2) {
              return new t3(this.q, this.x.subtract(e2.toBigInteger()).mod(this.q));
            }, t3.prototype.multiply = function(e2) {
              return new t3(this.q, this.x.multiply(e2.toBigInteger()).mod(this.q));
            }, t3.prototype.divide = function(e2) {
              return new t3(this.q, this.x.multiply(e2.toBigInteger().modInverse(this.q)).mod(this.q));
            }, t3.prototype.square = function() {
              return new t3(this.q, this.x.square().mod(this.q));
            }, t3;
          })(), a = (function() {
            function t3(e2, r2, o2, u2) {
              n(this, t3), this.curve = e2, this.x = r2, this.y = o2, this.z = null == u2 ? i.ONE : u2, this.zinv = null;
            }
            return t3.prototype.getX = function() {
              return null === this.zinv && (this.zinv = this.z.modInverse(this.curve.q)), this.curve.fromBigInteger(this.x.toBigInteger().multiply(this.zinv).mod(this.curve.q));
            }, t3.prototype.getY = function() {
              return null === this.zinv && (this.zinv = this.z.modInverse(this.curve.q)), this.curve.fromBigInteger(this.y.toBigInteger().multiply(this.zinv).mod(this.curve.q));
            }, t3.prototype.equals = function(t4) {
              return t4 === this || (this.isInfinity() ? t4.isInfinity() : t4.isInfinity() ? this.isInfinity() : !!t4.y.toBigInteger().multiply(this.z).subtract(this.y.toBigInteger().multiply(t4.z)).mod(this.curve.q).equals(i.ZERO) && t4.x.toBigInteger().multiply(this.z).subtract(this.x.toBigInteger().multiply(t4.z)).mod(this.curve.q).equals(i.ZERO));
            }, t3.prototype.isInfinity = function() {
              return null === this.x && null === this.y || this.z.equals(i.ZERO) && !this.y.toBigInteger().equals(i.ZERO);
            }, t3.prototype.negate = function() {
              return new t3(this.curve, this.x, this.y.negate(), this.z);
            }, t3.prototype.add = function(e2) {
              if (this.isInfinity())
                return e2;
              if (e2.isInfinity())
                return this;
              var r2 = this.x.toBigInteger(), n2 = this.y.toBigInteger(), o2 = this.z, u2 = e2.x.toBigInteger(), s2 = e2.y.toBigInteger(), a2 = e2.z, l2 = this.curve.q, c = r2.multiply(a2).mod(l2), f = u2.multiply(o2).mod(l2), h = c.subtract(f), g = n2.multiply(a2).mod(l2), p = s2.multiply(o2).mod(l2), d = g.subtract(p);
              if (i.ZERO.equals(h))
                return i.ZERO.equals(d) ? this.twice() : this.curve.infinity;
              var v = c.add(f), y = o2.multiply(a2).mod(l2), F = h.square().mod(l2), m = h.multiply(F).mod(l2), w = y.multiply(d.square()).subtract(v.multiply(F)).mod(l2), b = h.multiply(w).mod(l2), x = d.multiply(F.multiply(c).subtract(w)).subtract(g.multiply(m)).mod(l2), I = m.multiply(y).mod(l2);
              return new t3(this.curve, this.curve.fromBigInteger(b), this.curve.fromBigInteger(x), I);
            }, t3.prototype.twice = function() {
              if (this.isInfinity())
                return this;
              if (!this.y.toBigInteger().signum())
                return this.curve.infinity;
              var e2 = this.x.toBigInteger(), r2 = this.y.toBigInteger(), n2 = this.z, i2 = this.curve.q, o2 = this.curve.a.toBigInteger(), s2 = e2.square().multiply(u).add(o2.multiply(n2.square())).mod(i2), a2 = r2.shiftLeft(1).multiply(n2).mod(i2), l2 = r2.square().mod(i2), c = l2.multiply(e2).multiply(n2).mod(i2), f = a2.square().mod(i2), h = s2.square().subtract(c.shiftLeft(3)).mod(i2), g = a2.multiply(h).mod(i2), p = s2.multiply(c.shiftLeft(2).subtract(h)).subtract(f.shiftLeft(1).multiply(l2)).mod(i2), d = a2.multiply(f).mod(i2);
              return new t3(this.curve, this.curve.fromBigInteger(g), this.curve.fromBigInteger(p), d);
            }, t3.prototype.multiply = function(t4) {
              if (this.isInfinity())
                return this;
              if (!t4.signum())
                return this.curve.infinity;
              for (var e2 = t4.multiply(u), r2 = this.negate(), n2 = this, i2 = e2.bitLength() - 2; i2 > 0; i2--) {
                n2 = n2.twice();
                var o2 = e2.testBit(i2);
                o2 !== t4.testBit(i2) && (n2 = n2.add(o2 ? this : r2));
              }
              return n2;
            }, t3;
          })(), l = (function() {
            function t3(e2, r2, i2) {
              n(this, t3), this.q = e2, this.a = this.fromBigInteger(r2), this.b = this.fromBigInteger(i2), this.infinity = new a(this, null, null);
            }
            return t3.prototype.equals = function(t4) {
              return t4 === this || this.q.equals(t4.q) && this.a.equals(t4.a) && this.b.equals(t4.b);
            }, t3.prototype.fromBigInteger = function(t4) {
              return new s(this.q, t4);
            }, t3.prototype.decodePointHex = function(t4) {
              switch (parseInt(t4.substr(0, 2), 16)) {
                case 0:
                  return this.infinity;
                case 2:
                case 3:
                  var e2 = this.fromBigInteger(new i(t4.substr(2), 16)), r2 = this.fromBigInteger(e2.multiply(e2.square()).add(e2.multiply(this.a)).add(this.b).toBigInteger().modPow(this.q.divide(new i("4")).add(i.ONE), this.q));
                  return r2.toBigInteger().mod(o).equals(new i(t4.substr(0, 2), 16).subtract(o)) || (r2 = r2.negate()), new a(this, e2, r2);
                case 4:
                case 6:
                case 7:
                  var n2 = (t4.length - 2) / 2, u2 = t4.substr(2, n2), s2 = t4.substr(n2 + 2, n2);
                  return new a(this, this.fromBigInteger(new i(u2, 16)), this.fromBigInteger(new i(s2, 16)));
                default:
                  return null;
              }
            }, t3;
          })();
          t2.exports = {
            ECPointFp: a,
            ECCurveFp: l
          };
        },
        function(t2, e, r) {
          var n = r(1), i = n.sm3, o = n.hmac;
          function u(t3) {
            return t3.map((function(t4) {
              return 1 === (t4 = t4.toString(16)).length ? "0" + t4 : t4;
            })).join("");
          }
          function s(t3) {
            var e2, r2, n2 = [], i2 = t3.length;
            i2 % 2 != 0 && (r2 = i2 + 1, t3 = (e2 = t3).length >= r2 ? e2 : new Array(r2 - e2.length + 1).join("0") + e2), i2 = t3.length;
            for (var o2 = 0; o2 < i2; o2 += 2)
              n2.push(parseInt(t3.substr(o2, 2), 16));
            return n2;
          }
          t2.exports = function(t3, e2) {
            if (t3 = "string" == typeof t3 ? (function(t4) {
              for (var e3 = [], r3 = 0, n2 = t4.length; r3 < n2; r3++) {
                var i2 = t4.codePointAt(r3);
                if (i2 <= 127)
                  e3.push(i2);
                else if (i2 <= 2047)
                  e3.push(192 | i2 >>> 6), e3.push(128 | 63 & i2);
                else if (i2 <= 55295 || i2 >= 57344 && i2 <= 65535)
                  e3.push(224 | i2 >>> 12), e3.push(128 | i2 >>> 6 & 63), e3.push(128 | 63 & i2);
                else {
                  if (!(i2 >= 65536 && i2 <= 1114111))
                    throw e3.push(i2), new Error("input is not supported");
                  r3++, e3.push(240 | i2 >>> 18 & 28), e3.push(128 | i2 >>> 12 & 63), e3.push(128 | i2 >>> 6 & 63), e3.push(128 | 63 & i2);
                }
              }
              return e3;
            })(t3) : Array.prototype.slice.call(t3), e2) {
              if ("hmac" !== (e2.mode || "hmac"))
                throw new Error("invalid mode");
              var r2 = e2.key;
              if (!r2)
                throw new Error("invalid key");
              return r2 = "string" == typeof r2 ? s(r2) : Array.prototype.slice.call(r2), u(o(t3, r2));
            }
            return u(i(t3));
          };
        },
        function(t2, e, r) {
          var n = [214, 144, 233, 254, 204, 225, 61, 183, 22, 182, 20, 194, 40, 251, 44, 5, 43, 103, 154, 118, 42, 190, 4, 195, 170, 68, 19, 38, 73, 134, 6, 153, 156, 66, 80, 244, 145, 239, 152, 122, 51, 84, 11, 67, 237, 207, 172, 98, 228, 179, 28, 169, 201, 8, 232, 149, 128, 223, 148, 250, 117, 143, 63, 166, 71, 7, 167, 252, 243, 115, 23, 186, 131, 89, 60, 25, 230, 133, 79, 168, 104, 107, 129, 178, 113, 100, 218, 139, 248, 235, 15, 75, 112, 86, 157, 53, 30, 36, 14, 94, 99, 88, 209, 162, 37, 34, 124, 59, 1, 33, 120, 135, 212, 0, 70, 87, 159, 211, 39, 82, 76, 54, 2, 231, 160, 196, 200, 158, 234, 191, 138, 210, 64, 199, 56, 181, 163, 247, 242, 206, 249, 97, 21, 161, 224, 174, 93, 164, 155, 52, 26, 85, 173, 147, 50, 48, 245, 140, 177, 227, 29, 246, 226, 46, 130, 102, 202, 96, 192, 41, 35, 171, 13, 83, 78, 111, 213, 219, 55, 69, 222, 253, 142, 47, 3, 255, 106, 114, 109, 108, 91, 81, 141, 27, 175, 146, 187, 221, 188, 127, 17, 217, 92, 65, 31, 16, 90, 216, 10, 193, 49, 136, 165, 205, 123, 189, 45, 116, 208, 18, 184, 229, 180, 176, 137, 105, 151, 74, 12, 150, 119, 126, 101, 185, 241, 9, 197, 110, 198, 132, 24, 240, 125, 236, 58, 220, 77, 32, 121, 238, 95, 62, 215, 203, 57, 72], i = [462357, 472066609, 943670861, 1415275113, 1886879365, 2358483617, 2830087869, 3301692121, 3773296373, 4228057617, 404694573, 876298825, 1347903077, 1819507329, 2291111581, 2762715833, 3234320085, 3705924337, 4177462797, 337322537, 808926789, 1280531041, 1752135293, 2223739545, 2695343797, 3166948049, 3638552301, 4110090761, 269950501, 741554753, 1213159005, 1684763257];
          function o(t3) {
            for (var e2 = [], r2 = 0, n2 = t3.length; r2 < n2; r2 += 2)
              e2.push(parseInt(t3.substr(r2, 2), 16));
            return e2;
          }
          function u(t3) {
            return t3.map((function(t4) {
              return 1 === (t4 = t4.toString(16)).length ? "0" + t4 : t4;
            })).join("");
          }
          function s(t3) {
            for (var e2 = [], r2 = 0, n2 = t3.length; r2 < n2; r2++) {
              var i2 = t3.codePointAt(r2);
              if (i2 <= 127)
                e2.push(i2);
              else if (i2 <= 2047)
                e2.push(192 | i2 >>> 6), e2.push(128 | 63 & i2);
              else if (i2 <= 55295 || i2 >= 57344 && i2 <= 65535)
                e2.push(224 | i2 >>> 12), e2.push(128 | i2 >>> 6 & 63), e2.push(128 | 63 & i2);
              else {
                if (!(i2 >= 65536 && i2 <= 1114111))
                  throw e2.push(i2), new Error("input is not supported");
                r2++, e2.push(240 | i2 >>> 18 & 28), e2.push(128 | i2 >>> 12 & 63), e2.push(128 | i2 >>> 6 & 63), e2.push(128 | 63 & i2);
              }
            }
            return e2;
          }
          function a(t3) {
            for (var e2 = [], r2 = 0, n2 = t3.length; r2 < n2; r2++)
              t3[r2] >= 240 && t3[r2] <= 247 ? (e2.push(String.fromCodePoint(((7 & t3[r2]) << 18) + ((63 & t3[r2 + 1]) << 12) + ((63 & t3[r2 + 2]) << 6) + (63 & t3[r2 + 3]))), r2 += 3) : t3[r2] >= 224 && t3[r2] <= 239 ? (e2.push(String.fromCodePoint(((15 & t3[r2]) << 12) + ((63 & t3[r2 + 1]) << 6) + (63 & t3[r2 + 2]))), r2 += 2) : t3[r2] >= 192 && t3[r2] <= 223 ? (e2.push(String.fromCodePoint(((31 & t3[r2]) << 6) + (63 & t3[r2 + 1]))), r2++) : e2.push(String.fromCodePoint(t3[r2]));
            return e2.join("");
          }
          function l(t3, e2) {
            var r2 = 31 & e2;
            return t3 << r2 | t3 >>> 32 - r2;
          }
          function c(t3) {
            return (255 & n[t3 >>> 24 & 255]) << 24 | (255 & n[t3 >>> 16 & 255]) << 16 | (255 & n[t3 >>> 8 & 255]) << 8 | 255 & n[255 & t3];
          }
          function f(t3) {
            return t3 ^ l(t3, 2) ^ l(t3, 10) ^ l(t3, 18) ^ l(t3, 24);
          }
          function h(t3) {
            return t3 ^ l(t3, 13) ^ l(t3, 23);
          }
          function g(t3, e2, r2) {
            for (var n2 = new Array(4), i2 = new Array(4), o2 = 0; o2 < 4; o2++)
              i2[0] = 255 & t3[4 * o2], i2[1] = 255 & t3[4 * o2 + 1], i2[2] = 255 & t3[4 * o2 + 2], i2[3] = 255 & t3[4 * o2 + 3], n2[o2] = i2[0] << 24 | i2[1] << 16 | i2[2] << 8 | i2[3];
            for (var u2, s2 = 0; s2 < 32; s2 += 4)
              u2 = n2[1] ^ n2[2] ^ n2[3] ^ r2[s2 + 0], n2[0] ^= f(c(u2)), u2 = n2[2] ^ n2[3] ^ n2[0] ^ r2[s2 + 1], n2[1] ^= f(c(u2)), u2 = n2[3] ^ n2[0] ^ n2[1] ^ r2[s2 + 2], n2[2] ^= f(c(u2)), u2 = n2[0] ^ n2[1] ^ n2[2] ^ r2[s2 + 3], n2[3] ^= f(c(u2));
            for (var a2 = 0; a2 < 16; a2 += 4)
              e2[a2] = n2[3 - a2 / 4] >>> 24 & 255, e2[a2 + 1] = n2[3 - a2 / 4] >>> 16 & 255, e2[a2 + 2] = n2[3 - a2 / 4] >>> 8 & 255, e2[a2 + 3] = 255 & n2[3 - a2 / 4];
          }
          function p(t3, e2, r2) {
            for (var n2 = new Array(4), o2 = new Array(4), u2 = 0; u2 < 4; u2++)
              o2[0] = 255 & t3[0 + 4 * u2], o2[1] = 255 & t3[1 + 4 * u2], o2[2] = 255 & t3[2 + 4 * u2], o2[3] = 255 & t3[3 + 4 * u2], n2[u2] = o2[0] << 24 | o2[1] << 16 | o2[2] << 8 | o2[3];
            n2[0] ^= 2746333894, n2[1] ^= 1453994832, n2[2] ^= 1736282519, n2[3] ^= 2993693404;
            for (var s2, a2 = 0; a2 < 32; a2 += 4)
              s2 = n2[1] ^ n2[2] ^ n2[3] ^ i[a2 + 0], e2[a2 + 0] = n2[0] ^= h(c(s2)), s2 = n2[2] ^ n2[3] ^ n2[0] ^ i[a2 + 1], e2[a2 + 1] = n2[1] ^= h(c(s2)), s2 = n2[3] ^ n2[0] ^ n2[1] ^ i[a2 + 2], e2[a2 + 2] = n2[2] ^= h(c(s2)), s2 = n2[0] ^ n2[1] ^ n2[2] ^ i[a2 + 3], e2[a2 + 3] = n2[3] ^= h(c(s2));
            if (0 === r2)
              for (var l2, f2 = 0; f2 < 16; f2++)
                l2 = e2[f2], e2[f2] = e2[31 - f2], e2[31 - f2] = l2;
          }
          function d(t3, e2, r2) {
            var n2 = arguments.length > 3 && void 0 !== arguments[3] ? arguments[3] : {}, i2 = n2.padding, l2 = void 0 === i2 ? "pkcs#7" : i2, c2 = n2.mode, f2 = n2.iv, h2 = void 0 === f2 ? [] : f2, d2 = n2.output, v = void 0 === d2 ? "string" : d2;
            if ("cbc" === c2 && ("string" == typeof h2 && (h2 = o(h2)), 16 !== h2.length))
              throw new Error("iv is invalid");
            if ("string" == typeof e2 && (e2 = o(e2)), 16 !== e2.length)
              throw new Error("key is invalid");
            if (t3 = "string" == typeof t3 ? 0 !== r2 ? s(t3) : o(t3) : [].concat(t3), ("pkcs#5" === l2 || "pkcs#7" === l2) && 0 !== r2)
              for (var y = 16 - t3.length % 16, F = 0; F < y; F++)
                t3.push(y);
            var m = new Array(32);
            p(e2, m, r2);
            for (var w = [], b = h2, x = t3.length, I = 0; x >= 16; ) {
              var B = t3.slice(I, I + 16), q = new Array(16);
              if ("cbc" === c2)
                for (var P = 0; P < 16; P++)
                  0 !== r2 && (B[P] ^= b[P]);
              g(B, q, m);
              for (var E = 0; E < 16; E++)
                "cbc" === c2 && 0 === r2 && (q[E] ^= b[E]), w[I + E] = q[E];
              "cbc" === c2 && (b = 0 !== r2 ? q : B), x -= 16, I += 16;
            }
            if (("pkcs#5" === l2 || "pkcs#7" === l2) && 0 === r2) {
              for (var A = w.length, H = w[A - 1], C = 1; C <= H; C++)
                if (w[A - C] !== H)
                  throw new Error("padding is invalid");
              w.splice(A - H, H);
            }
            return "array" !== v ? 0 !== r2 ? u(w) : a(w) : w;
          }
          t2.exports = {
            encrypt: function(t3, e2, r2) {
              return d(t3, e2, 1, r2);
            },
            decrypt: function(t3, e2, r2) {
              return d(t3, e2, 0, r2);
            }
          };
        }
      ]);
    }
  });

  // sm2_bridge.js
  var sm2 = require_miniprogram_dist().sm2;
  function sign(msgHex, privKeyHex, options = { hash: true, der: true }) {
    try {
      let sigValue = sm2.doSignature(msgHex, privKeyHex, options);
      return sigValue;
    } catch (e) {
      return "Error: " + e.message;
    }
  }
  function decrypt(encryptDataHex, privKeyHex, cipherMode = 1) {
    try {
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
  globalThis.sign = sign;
  globalThis.decrypt = decrypt;
  globalThis.getPublicKey = getPublicKey;
  globalThis.verify = verify;
})();
