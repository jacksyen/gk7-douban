M(i, {
  purchaseTime: this.purchaseTime,
  isSample: this.isSample,
  isGift: this.isGift
}).done(n.proxy((function(n) {
  n.r && function(n) {
    var o, r = n.data;
    try {
      // !!!!!!!!!!!!!!!!
      o = JSON.parse(k(r, O(i)))
    } catch (t) {
      return !1
    }
    return !(!n.purchaseTime && n.limitedVip && n.limitedVip.canRead && new Date(n.limitedVip.endTime) < new Date) && (e.dataFromLocal = !0,
    o.gift && (o.gift.opened = !0),
      e.adaptDecryptedData(o),
      t.resolve(o),
      !0)
  }(o) || this.fetchArticle().done(r)
}

/**
 *
 * @param t  9555823
 * @returns {string}
 */
t.exports = function(t) {
  // i: 58724495
  return parseInt((i + t).slice(0, 10), 36).toString().slice(0, 5)
}

/**
 *
 * @param t r.data
 * @param e 53092
 * @returns {*}
 */
var r = i(46)
// r = ["A", "b", "H", "P", "Q", "X", "V", "p", "r", "I", "$", "7", "F", "z", "o", "K", "_", "S", "6", "a", "T", "C", "t", "j", "5", "n", "D", "e", "x", "U", "R", "y", "4", "N", "Y", "9", "v", "0", "3", "W", "l", "u", "1", "i", "q", "s", "O", "J", "G", "E", "w", "f", "B", "m", "L", "2", "d", "h", "k", "8", "c", "g", "Z", "M"]
t.exports = function(t, e) {
  return function(t, e, i) {
    var r = {}
      , s = String.fromCharCode("}".charCodeAt(0) + 1)
      , o = e.length;
    e = function(t, e, i) {
      return e ? (t = t.slice(),
        e.split("").forEach((function(e) {
            var r = e.charCodeAt(0) % i;
            t = [].concat(n(t.slice(r)), n(t.slice(0, r)))
          }
        )),
        t) : t
    }(e, i, o);
    for (var a = 0; a < o; ++a)
      r[e[a]] = a;
    for (var h, l, c, u, d = [], f = 0, p = 0; f < t.length; )
      h = r[t[f++]],
        l = r[t[f++]],
        c = r[t[f++]],
        u = r[t[f++]],
        d[p++] = h << 2 | l >> 4,
        d[p++] = (15 & l) << 4 | c >> 2,
        d[p++] = (3 & c) << 6 | u;
    var g = t.slice(-2);
    return g[0] === s ? d.length = d.length - 2 : g[1] === s && (d.length = d.length - 1),
      function(t) {
        for (var e = "", i = 0; i < t.length; ++i) {
          var n = t[i];
          e += String.fromCharCode(256 * n + t[++i])
        }
        return e
      }(d)
  }(t, r, e)
}
