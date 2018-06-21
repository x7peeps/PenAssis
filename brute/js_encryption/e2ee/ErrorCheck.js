var ErrorCheck ={
	E0002:function(modulus) {
		/*Invalid RSA Public Key modulus length or char*/
		if((modulus.length==256) ||(modulus.length==512)){
			return '';
		}else{
			return 'E0002';
		}
	},
	E0003:function(e) {
		/*Invalid RSA Public Key exponent length or char*/
		if(e.length==6) {
			return '';
		}else{
			return 'E0003';
		}
	},
	E0004:function(l) {
		/*Invalid 3DES Key length*/
		if((l==2) ||(l==3)){
			return '';
		}else{
			return 'E0004';
		}			
	},
	E0005:function(iv) {
		if(iv==null){
			return '';
		}else{
			iv=iv.toUpperCase();
			/*Invalid IV length or charater*/
			if(iv.length==16) {
				for(var i=0; i<16;i++){
					var hex = WPCommonJS.Ascii2Hex(iv.substr(i,1));
					if((hex>=30) &&(hex<=46)){
						//ok
					}else
					{
						return 'E0005';
					}					
				}
				return '';
			}else{
				return 'E0005';
			}
		}
	},
	E0006:function() {
		/*Data length exceed the limit*/
	},
	E0007:function(ap) {
		/*Invalid AnPin length (6-16)*/
		if((ap.length>=6)&&(ap.length<=16)) {
			return '';
		}else{
			return 'E0007';
		}
	},
	E0008:function(newap) {
		/*Invalid New AnPin length (6-16)*/
		if((newap.length>=6)&&(newap.length<=16)) {
			return '';
		}else{
			return 'E0008';
		}
	},
	E0009:function(mode) {
		/*Invalid Mode*/
		if((mode=='1')||(mode=='2')){
			return '';
		}else
		{
			return 'E0009';
		}
	},
	E0010:function() {
		/*Invalid character in data*/
	},
	E0011:function(input) {
		/*Invalid Version in data*/
		if(input=='2'){
			return '';
		}else{
			return 'E0011';
		}
	},
	E0012:function() {
		/*Invalid Type in message*/
	},
	E0013:function() {
		/*Invalid Data Encryption Key length*/
		
	},
	E0014:function() {
		/*Invalid Data length (data is not multiple of 16 hex characters*/
		
	},
	E0015:function() {
		/*Exceed max cata length (i.e. data length larger than 61440 hex characters)*/
		
	}
}