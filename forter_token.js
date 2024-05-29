function i() {
        return {
            d0: (4294967296 * Math.random()) >>> 0,
            d1: (4294967296 * Math.random()) >>> 0,
            d2: (4294967296 * Math.random()) >>> 0,
            d3: (4294967296 * Math.random()) >>> 0,
        };
    }
    for (var t = {}, n = 'fgu', e = [], r = 0; r < 256; r++)
        e[r] = (r < 16 ? '0' : '') + r.toString(16);
    function o(t, n, r, o, i) {
    
        var c = i ? '-' : '';
        return (
            e[255 & t] +
            e[(t >> 8) & 255] +
            e[(t >> 16) & 255] +
            e[(t >> 24) & 255] +
            c +
            e[255 & n] +
            e[(n >> 8) & 255] +
            c +
            e[((n >> 16) & 15) | 64] +
            e[(n >> 24) & 255] +
            c +
            e[(63 & r) | 128] +
            e[(r >> 8) & 255] +
            c +
            e[(r >> 16) & 255] +
            e[(r >> 24) & 255] +
            e[255 & o] +
            e[(o >> 8) & 255] +
            e[(o >> 16) & 255] +
            e[(o >> 24) & 255]);
    }
    
    var t = i();
    console.log(o(t.d0, t.d1, t.d2, t.d3, !1));