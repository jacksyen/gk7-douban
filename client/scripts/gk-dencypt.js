var pretty = function (){
    var _hexCHS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz$_~";

    function Hex64(key) {
	this._key = [], 
	this._tbl = {};
	for (var _i = 0; 64 > _i; ++_i){
	    this._key[_i] = _hexCHS.charAt(key[_i]), 
	    this._tbl[this._key[_i]] = _i;
	}
	this._pad = _hexCHS.charAt(64)
    }

    Hex64.prototype.dec = function(s) {
	var _n1, _n2, _n3, _n4, _sa = [],
	_i = 0,
	_c = 0;
        s = s.replace(/[^0-9A-Za-z$_~]/g, "");
	for (s;_i < s.length;){
	    _n1 = this._tbl[s.charAt(_i++)], 
	    _n2 = this._tbl[s.charAt(_i++)], 
	    _n3 = this._tbl[s.charAt(_i++)], 
	    _n4 = this._tbl[s.charAt(_i++)], 
	    _sa[_c++] = _n1 << 2 | _n2 >> 4, 
	    _sa[_c++] = (15 & _n2) << 4 | _n3 >> 2, 
	    _sa[_c++] = (3 & _n3) << 6 | _n4;
	}
	var _e2 = s.slice(-2);
	return _e2.charAt(0) === this._pad ? _sa.length = _sa.length - 2 : _e2.charAt(1) === this._pad && (_sa.length = _sa.length - 1), Hex64._1to2(_sa)
    }, 
    Hex64._1to2 = function(a) {
	for (var  _rs = "", _i = 0; _i < a.length; ++_i) {
            var _c = a[_i];
            _rs += String.fromCharCode(256 * _c + a[++_i]);
	}
	return _rs;
    };

    var _key = [37, 7, 20, 41, 59, 53, 8, 24, 5, 62, 31, 4, 32, 6, 50, 36, 63, 35, 51, 0, 13, 43, 46, 40, 15, 27, 17, 57, 28, 54, 1, 60, 21, 22, 47, 42, 30, 39, 12, 3, 9, 45, 29, 23, 56, 2, 16, 61, 52, 44, 25, 14, 49, 34, 33, 10, 58, 55, 19, 26, 11, 18, 48, 38],
    decrypt = new Hex64(_key);

    return decrypt;
}

/**
   $.parseJSON(
   
**/
