var WPCommonJS ={
	

	checkBin:function(n){return/^[01]{1,64}$/.test(n)},
	checkDec:function(n){return/^[0-9]{1,64}$/.test(n)},
	checkHex:function(n){return/^[0-9A-Fa-f]{1,64}$/.test(n)},
	pad:function(s,z){s=""+s;return s.length<z?pad("0"+s,z):s},
	unpad:function(s){s=""+s;return s.replace(/^0+/,'')},

//Decimal operations
	Dec2Bin:function(n){if(!this.checkDec(n)||n<0)return 0;return n.toString(2)},
	Dec2Hex:function(n){if(!this.checkDec(n)||n<0)return 0;return n.toString(16)},

//BINARY Operations
	Bin2Dec:function(n){if(!this.checkBin(n))return 0;return parseInt(n,2).toString(10)},
	Bin2Hex:function(n){
		if(!this.checkBin(n))
			return 0;
		//var tmp=parseInt(n,2).toString(16);
		var hex ='';
		for(var i=0; i<n.length/8; i++){
			var otmp = n.substr(8*i,8);
			var tmp = parseInt(otmp,2).toString(16);
			var tmpcount = 2-tmp.length;
			for(var j=0;j<tmpcount;j++){
				tmp='0'+tmp;
			}
			hex=hex.concat(tmp);
		}
		//return parseInt(n,2).toString(16)
		return hex;
	},

//Hexadecimal Operations
	Hex2Bin:function(n){
		if(!this.checkHex(n))
			return 0;
		
		var opty='';
			n=n.toUpperCase();
			for(var i=0; i<n.length/2; i++){
				var tmp = parseInt(n.substr(2*i,2),16).toString(2);
				var padzeroleft =0;
				if(tmp.length!=8){
					padzeroleft=8-tmp.length%8;
					for(var j=0; j<padzeroleft; j++){
						tmp='0'+tmp;
					}
				}
				opty=opty.concat(tmp);
			}
		
		//return parseInt(n,16).toString(2);	 
		return opty;
	},
	HexOdd:function(n){
		
		var nlen =n.length;
		var output = '';
		for(var i=0; i<nlen/2;i++){
			var hex = n.substr(2*i,2);
			var opty =WPCommonJS.Hex2Bin(hex);
			var counthex = 0;
			for (var j=0; j<8; j++){
				var c = opty.substr(j,1);
				if(c==1){
					counthex++;
				}
			}
			if (counthex%2==0){
				var last =opty.substr(7,1);
				if(last=='0'){
					opty =opty.substr(0,7).concat('1');
				}else{
					opty =opty.substr(0,7).concat('0');
				}	
			}
			var b2h = WPCommonJS.Bin2Hex(opty);
			output =output+b2h;
		}
		
		
		return output ;
	},
	Ascii2Hex:function(a){

		var ascii=a.toString();
		var str='';
		for(var i=0;i<ascii.length;i+=1)
			str+=ascii.charCodeAt(i).toString(16);
		return str;

	},
	Hex2Dec:function(n){if(!this.checkHex(n))return 0;return parseInt(n,16).toString(10)},
	WPRSAEncrypt:function(n,e,plaintext){
		
		if(typeof String.prototype.trim !== 'function') {
			String.prototype.trim = function() {
			return this.replace(/^\s+|\s+$/g, ''); 
			}
		}
		
		var rsa = new RSAKey();
		rsa.setPublic(n, e);
		var res ='';
		res=rsa.encrypt(plaintext).toUpperCase().trim();
		
		if(n.length==256){
			var padzero = 256-res.length;
			var zero= '';
			for(var i=0; i<padzero; i++){
				zero=zero+'0';
			}
			res = zero+res;
		}
		else if(n.length==512)
		{
			var padzero = 512-res.length;
			var zero= '';
			for(var i=0; i<padzero; i++){
				zero=zero+'0';
			}
			res = zero+res;
		}
		
		return res;
	},
	WPGenIV:function(){
		sjcl.random.removeEventListener('seeded',this.WPGenIV);
		//
		//return sjcl.codec.hex.fromBits(sjcl.random.randomWords(2));
		return sjcl.random.randomWords(2, 0);
	},
	setCharAt:function(str,index,chr){
		if(index>str.length-1)return str;
		return str.substr(0,index)+chr+str.substr(index+1);
	},
	WPDesEncrypt:function(plaintext,mode,TDesKeyLen,key1Hex,key2Hex,key3Hex,ivhex){
		var encrypted ='';
		var keyHex='';
		if(TDesKeyLen=='2'){
			//Double Length
			keyHex=key1Hex.concat(key2Hex);
			keyHex=keyHex.concat(key1Hex);
		}else if(TDesKeyLen=='3'){
			//Triple Length
			keyHex=key1Hex.concat(key2Hex);
			keyHex=keyHex.concat(key3Hex);
		}
		
		if(mode=='1'){ //ECB
			encrypted =	CryptoJS.DES.encrypt(CryptoJS.enc.Hex.parse(plaintext), CryptoJS.enc.Hex.parse(keyHex), {
				mode: CryptoJS.mode.ECB,
				padding: CryptoJS.pad.ZeroPadding
			});
		}else if(mode=='2'){ //CBC
			if(ivhex==null){
				ivhex=window.WPIVHex;				
			}
			
			encrypted = CryptoJS.DES.encrypt(CryptoJS.enc.Hex.parse(plaintext), CryptoJS.enc.Hex.parse(keyHex), {
				mode: CryptoJS.mode.CBC,
				padding: CryptoJS.pad.ZeroPadding,
				iv:  CryptoJS.enc.Hex.parse(ivhex)
			});
		}
		return encrypted.ciphertext.toString(CryptoJS.enc.Hex);
	},
	WPTriDesEncrypt:function(plaintext,mode,TDesKeyLen,key1Hex,key2Hex,key3Hex,ivhex){
		var encrypted ='';
		var keyHex='';
		if(TDesKeyLen=='2'){
			//Double Length
			keyHex=key1Hex.concat(key2Hex);
			keyHex=keyHex.concat(key1Hex);
		}else if(TDesKeyLen=='3'){
			//Triple Length
			keyHex=key1Hex.concat(key2Hex);
			keyHex=keyHex.concat(key3Hex);
		}
		
		if(mode=='1'){ //ECB
			encrypted =	CryptoJS.TripleDES.encrypt(CryptoJS.enc.Hex.parse(plaintext), CryptoJS.enc.Hex.parse(keyHex), {
				mode: CryptoJS.mode.ECB,
				padding: CryptoJS.pad.NoPadding
			});
		}else if(mode=='2'){ //CBC
			if(ivhex==null){
				ivhex=window.WPIVHex;				
			}
			
			encrypted = CryptoJS.TripleDES.encrypt(CryptoJS.enc.Hex.parse(plaintext), CryptoJS.enc.Hex.parse(keyHex), {
				mode: CryptoJS.mode.CBC,
				padding: CryptoJS.pad.NoPadding,
				iv:  CryptoJS.enc.Hex.parse(ivhex)
			});
		}
		/*
		var hexstr =encrypted.ciphertext.toString(CryptoJS.enc.Hex);
		
		var pad = 16- hexstr.length%16;
		if(pad!=16){
			for(var i=0; i<pad; i++){
				hexstr=hexstr+'0';
			}
		}
		*/
		return encrypted.ciphertext.toString(CryptoJS.enc.Hex);
	},
	WPTriDesDecrypt:function(plaintext,mode,keyHex,ivhex){
		var encrypted ='';
		var key1Hex='';
		if(keyHex.length==32){
			//Double Length
			key1Hex=keyHex.substring(0,16);
			keyHex=keyHex.concat(key1Hex);
		}else if(keyHex==48){
			//do nothing
			
		}
		
		if(mode=='1'){ //ECB
			encrypted =	CryptoJS.TripleDES.decrypt( {
				ciphertext: CryptoJS.enc.Hex.parse(plaintext)
			}, CryptoJS.enc.Hex.parse(keyHex), {
				mode: CryptoJS.mode.ECB, 
				padding: CryptoJS.pad.NoPadding});
		}else if(mode=='2'){ //CBC
			if(ivhex==null){
				ivhex=window.WPIVHex;				
			}
			
			encrypted = CryptoJS.TripleDES.decrypt( {
				ciphertext: CryptoJS.enc.Hex.parse(plaintext)
			}, CryptoJS.enc.Hex.parse(keyHex), {
				mode: CryptoJS.mode.CBC, 
				iv:  CryptoJS.enc.Hex.parse(ivhex),
				padding: CryptoJS.pad.NoPadding});
		}
		/*
		mode: CryptoJS.mode.CBC,
				padding: CryptoJS.pad.ZeroPadding,
				iv:  CryptoJS.enc.Hex.parse(ivhex)
		*/
		/*
		var hexstr ='';
		hexstr = encrypted.toString(CryptoJS.enc.Hex);
		var pad='';
		
		pad = 16- hexstr.length%16;
		if(pad!=16){
			for(var i=0; i<pad; i++){
				hexstr=hexstr+'0';
			}
		}
		*/
		return encrypted.toString(CryptoJS.enc.Hex);
	},
	genkey:function() {
		var Key1 = sjcl.codec.hex.fromBits(sjcl.random.randomWords(2, 0));
		window.WPKey1  = Key1;
		var Key2 = sjcl.codec.hex.fromBits(sjcl.random.randomWords(2, 0));
		window.WPKey2  = Key2;
		var Key3 = sjcl.codec.hex.fromBits(sjcl.random.randomWords(2, 0));
		window.WPKey3  = Key3;
	},
	genIVHex:function () {
		var IVHex = sjcl.codec.hex.fromBits(sjcl.random.randomWords(2, 0));
		window.WPIVHex  = IVHex;
	},
	gen256Hex:function() {
		var Hex256 = sjcl.codec.hex.fromBits(sjcl.random.randomWords(32, 0));
		window.WP256Hex  = Hex256;
	},
	gen512Hex:function() {
		var Hex512 = sjcl.codec.hex.fromBits(sjcl.random.randomWords(64, 0));
		window.WP512Hex  = Hex512;
	},
	gen256PINHex:function() {
		var PINHex256 = sjcl.codec.hex.fromBits(sjcl.random.randomWords(32, 0));
		window.WP256PINHex  = PINHex256;
	},
	gen512PINHex:function() {
		var PINHex512 = sjcl.codec.hex.fromBits(sjcl.random.randomWords(64, 0));
		window.WP512PINHex  = PINHex512;
	},
	gen256MACHex:function() {
		var MACHex256 = sjcl.codec.hex.fromBits(sjcl.random.randomWords(32, 0));
		window.WP256MACHex  = MACHex256;
	},
	gen512MACHex:function() {
		var MACHex512 = sjcl.codec.hex.fromBits(sjcl.random.randomWords(64, 0));
		window.WP512MACHex  = MACHex512;
	},
	genPinkey:function() {
		var Key1 = sjcl.codec.hex.fromBits(sjcl.random.randomWords(2, 0));
		window.WPPINKey1  = Key1;
		var Key2 = sjcl.codec.hex.fromBits(sjcl.random.randomWords(2, 0));
		window.WPPINKey2  = Key2;
		var Key3 = sjcl.codec.hex.fromBits(sjcl.random.randomWords(2, 0));
		window.WPPINKey3  = Key3;
	},
	genMACkey:function() {
		var Key1 = sjcl.codec.hex.fromBits(sjcl.random.randomWords(2, 0));
		window.WPMACKey1  = Key1;
		var Key2 = sjcl.codec.hex.fromBits(sjcl.random.randomWords(2, 0));
		window.WPMACKey2  = Key2;
		var Key3 = sjcl.codec.hex.fromBits(sjcl.random.randomWords(2, 0));
		window.WPMACKey3  = Key3;
	},
	isIE:function() {
		var myNav = navigator.userAgent.toLowerCase();
		return (myNav.indexOf('msie') != -1) ? parseInt(myNav.split('msie')[1]) : false;
	}

}