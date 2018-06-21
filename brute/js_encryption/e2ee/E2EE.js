var E2EE ={
	EncryptMsg:function(modulus, exponent, triDesKeyLen,iv, mode, data){
		debug=0;
		WPCommonJS.genkey();
		WPCommonJS.genIVHex();
		WPCommonJS.gen256Hex();
		WPCommonJS.gen512Hex();
		var output='222';
		if(iv==''){
			iv=null;
		}
		//error checking
		var E0002 = ErrorCheck.E0002(modulus);
		var E0003 = ErrorCheck.E0003(exponent);
		var E0004 = ErrorCheck.E0004(triDesKeyLen);
		var E0005 = ErrorCheck.E0005(iv);
		var E0009 = ErrorCheck.E0009(mode);
		if(E0002 !=''){
			return E0002;
		}
		if(E0003 !=''){
			return E0003;
		}
		if(E0004 !=''){
			return E0004;
		}
		if(E0005 !=''){
			return E0005;
		}
		if(E0009 !=''){
			return E0009;
		}
		//error checking
		var modlen = modulus.length;
		var rsaKeyLen= '1';
		if(modlen==256){
			rsaKeyLen='1';
		}else if(modlen==512){
			rsaKeyLen ='2';
		}

		output=output.concat(rsaKeyLen);
		output=output.concat(triDesKeyLen);

		var modlen = modulus.length;
		var rsaKeyLen= '1';
		if(modlen==256){
			rsaKeyLen='1';
		}else if(modlen==512){
			rsaKeyLen ='2';
		}

		if(iv==null){
			iv=window.WPIVHex;
		}



		k1=WPCommonJS.HexOdd(window.WPKey1);
		k2=WPCommonJS.HexOdd(window.WPKey2);
		k3=WPCommonJS.HexOdd(window.WPKey3);

		if(debug=='1'){
			console.log('k1:'+k1);
			console.log('k2:'+k2);
			console.log('k3:'+k3);
		}
	//console.log('k1:'+k1);
	//console.log('k2:'+k2);
	if(triDesKeyLen=='3')
	//console.log('k3:'+k3);

		var temp ='';
		//var	ivhex=window.WPIVHex;

		if(rsaKeyLen=='1'){

			temp=window.WP256Hex;
			temp = temp.replace(/0/g,'F');
			temp=WPCommonJS.setCharAt(temp,0,'0');
			temp=WPCommonJS.setCharAt(temp,1,'0');
			temp=WPCommonJS.setCharAt(temp,2,'0');
			temp=WPCommonJS.setCharAt(temp,3,'2');



			if(triDesKeyLen=='2'){
				temp=WPCommonJS.setCharAt(temp,194,'0');
				temp=WPCommonJS.setCharAt(temp,195,'0');

				temp=WPCommonJS.setCharAt(temp,196,'3');
				temp=WPCommonJS.setCharAt(temp,197,'0');
				temp=WPCommonJS.setCharAt(temp,198,'1');
				temp=WPCommonJS.setCharAt(temp,199,'C');

				temp=WPCommonJS.setCharAt(temp,200,'0');
				temp=WPCommonJS.setCharAt(temp,201,'4');
				temp=WPCommonJS.setCharAt(temp,202,'1');
				temp=WPCommonJS.setCharAt(temp,203,'0');

				temp=WPCommonJS.setCharAt(temp,236,'0');
				temp=WPCommonJS.setCharAt(temp,237,'4');
				temp=WPCommonJS.setCharAt(temp,238,'0');
				temp=WPCommonJS.setCharAt(temp,239,'8');



				for(var i=204; i<220; i++){
					temp=WPCommonJS.setCharAt(temp,i,k1.charAt(i-204));
				}
				for(var i=220; i<236; i++){
					temp=WPCommonJS.setCharAt(temp,i,k2.charAt(i-220));
				}

			}else if(triDesKeyLen =='3'){
				temp=WPCommonJS.setCharAt(temp,178,'0');
				temp=WPCommonJS.setCharAt(temp,179,'0');

				temp=WPCommonJS.setCharAt(temp,180,'3');
				temp=WPCommonJS.setCharAt(temp,181,'0');
				temp=WPCommonJS.setCharAt(temp,182,'2');
				temp=WPCommonJS.setCharAt(temp,183,'4');

				temp=WPCommonJS.setCharAt(temp,184,'0');
				temp=WPCommonJS.setCharAt(temp,185,'4');
				temp=WPCommonJS.setCharAt(temp,186,'1');
				temp=WPCommonJS.setCharAt(temp,187,'8');

				temp=WPCommonJS.setCharAt(temp,236,'0');
				temp=WPCommonJS.setCharAt(temp,237,'4');
				temp=WPCommonJS.setCharAt(temp,238,'0');
				temp=WPCommonJS.setCharAt(temp,239,'8');

				for(var i=188; i<204; i++){
					temp=WPCommonJS.setCharAt(temp,i,k1.charAt(i-188));
				}
				for(var i=204; i<220; i++){
					temp=WPCommonJS.setCharAt(temp,i,k2.charAt(i-204));
				}
				for(var i=220; i<236; i++){
					temp=WPCommonJS.setCharAt(temp,i,k3.charAt(i-220));
				}
			}


			for(var i=240; i<256; i++){
				temp=WPCommonJS.setCharAt(temp,i,iv.charAt(i-240));
			}

		}else if(rsaKeyLen=='2'){

			temp=window.WP512Hex;
			temp = temp.replace(/0/g,'F');
			temp=WPCommonJS.setCharAt(temp,0,'0');
			temp=WPCommonJS.setCharAt(temp,1,'0');
			temp=WPCommonJS.setCharAt(temp,2,'0');
			temp=WPCommonJS.setCharAt(temp,3,'2');


			if(triDesKeyLen=='2'){
				temp=WPCommonJS.setCharAt(temp,450,'0');
				temp=WPCommonJS.setCharAt(temp,451,'0');

				temp=WPCommonJS.setCharAt(temp,452,'3');
				temp=WPCommonJS.setCharAt(temp,453,'0');
				temp=WPCommonJS.setCharAt(temp,454,'1');
				temp=WPCommonJS.setCharAt(temp,455,'C');

				temp=WPCommonJS.setCharAt(temp,456,'0');
				temp=WPCommonJS.setCharAt(temp,457,'4');
				temp=WPCommonJS.setCharAt(temp,458,'1');
				temp=WPCommonJS.setCharAt(temp,459,'0');

				temp=WPCommonJS.setCharAt(temp,492,'0');
				temp=WPCommonJS.setCharAt(temp,493,'4');
				temp=WPCommonJS.setCharAt(temp,494,'0');
				temp=WPCommonJS.setCharAt(temp,495,'8');



				for(var i=460; i<476; i++){
					temp=WPCommonJS.setCharAt(temp,i,k1.charAt(i-460));
				}
				for(var i=476; i<492; i++){
					temp=WPCommonJS.setCharAt(temp,i,k2.charAt(i-476));
				}

			}else if(triDesKeyLen =='3'){
				temp=WPCommonJS.setCharAt(temp,434,'0');
				temp=WPCommonJS.setCharAt(temp,435,'0');

				temp=WPCommonJS.setCharAt(temp,436,'3');
				temp=WPCommonJS.setCharAt(temp,437,'0');
				temp=WPCommonJS.setCharAt(temp,438,'2');
				temp=WPCommonJS.setCharAt(temp,439,'4');

				temp=WPCommonJS.setCharAt(temp,440,'0');
				temp=WPCommonJS.setCharAt(temp,441,'4');
				temp=WPCommonJS.setCharAt(temp,442,'1');
				temp=WPCommonJS.setCharAt(temp,443,'8');

				temp=WPCommonJS.setCharAt(temp,492,'0');
				temp=WPCommonJS.setCharAt(temp,493,'4');
				temp=WPCommonJS.setCharAt(temp,494,'0');
				temp=WPCommonJS.setCharAt(temp,495,'8');

				for(var i=444; i<460; i++){
					temp=WPCommonJS.setCharAt(temp,i,k1.charAt(i-444));
				}
				for(var i=460; i<476; i++){
					temp=WPCommonJS.setCharAt(temp,i,k2.charAt(i-460));
				}
				for(var i=476; i<492; i++){
					temp=WPCommonJS.setCharAt(temp,i,k3.charAt(i-476));
				}
			}


			for(var i=496; i<512; i++){
				temp=WPCommonJS.setCharAt(temp,i,iv.charAt(i-496));
			}

		}
	//console.log('Data Encrypt Key Before RSA:'+temp);
		//console.log(modulus);
		//modulus = 'BA4318B1C46025FFA97142AE3D10A6E9030D0462D95002B7692DF37785728D6EA3B06B848839B207536C86450531FF198AF8DA93862B92599ACCF741EBA8B9EA706C01D5100B03E7DAAB3BC03451174BD679478276C807E54E509880245421ADB8E865B4B5EC363F394BC13187647AAB15FE75DE99AEAAAA463F7A4DA5BBC56284E0C38AB2B26639E4D0DE494878BBB85E63EC5DB6F517F3C1CC474959354647376A5DC17BCEE66FF0C14499C0964A4EC6565E61CB3FE6B3DCB9405F41DE3495A35AC6D03219EB4A12BA35026011BC0B233352D4506374246884EB49ECEFA3367ED9A0A6C9EAA444BB3DF25C36E66331D848FA38E32BA94ACD67E1E88976B3A9';
		//temp = '0002038D310EC2F50D37562A32312EC773223B4833C454EFB59AAA93B60A6BEDA904C68D71F5E30FDA9A4D4E5021976904F34079B78596A19A1BE1C209EE0D6AE56ED386339134E7856FCA1BDC2F4DD21C2207C3575F9CA94F94816CD132EF2E29515CC22561394483F0B4A57702538749A4867682A80217BEC9FA616997C1015CA2D9E8925840CAF3C122D76A8AC4BAE5C6D8AC4BDF56D5851FE487B113770AF7CB7AA13BFA7EDCD2B1A4FC42BF886CD67E6FA962CC1B812C1D66F356511B30854D587B3F5536289F716302EA8C6EC9E2A7C3F7BBFB51C92A003024041832E52075E33DFE193ECB57E6E9E5F80185D90B4AB33125B304084A4C97BA981E209D';
		var outputrsa = WPCommonJS.WPRSAEncrypt(modulus,exponent,temp);



	//console.log('Data Encrypt Key After RSA:'+outputrsa);
		var encryptedIV='';
			//(plaintext,mode,TDesKeyLen,key1Hex,key2Hex,ivhex)


		encryptedIV = WPCommonJS.WPTriDesEncrypt(iv,'1',triDesKeyLen,k1,k2,k3,null);//triDesKeyLen,iv, mode,


	//console.log('Encrypted TDES(ECB) IV:'+encryptedIV);
		var encryptedData = '';

	//console.log('Data Before TDES:'+data);
		encryptedData = WPCommonJS.WPTriDesEncrypt(data,mode,triDesKeyLen,k1,k2,k3,iv);
	//console.log('Data After TDES:'+encryptedData);

		output = output.concat(outputrsa.toUpperCase());
		output = output.concat(encryptedIV.toUpperCase());

		if(triDesKeyLen=='2'){
			output = output.concat(k1.toUpperCase());
			output = output.concat(k2.toUpperCase());
			//output = output.concat(k1);
		}else if(triDesKeyLen=='3'){
			output = output.concat(k1.toUpperCase());
			output = output.concat(k2.toUpperCase());
			output = output.concat(k3.toUpperCase());
		}

		output = output.concat(encryptedData.toUpperCase());

		if(debug=='1'){
			console.log('encryptedkey:'+outputrsa);
			console.log('encryptedIV:'+encryptedIV);
			console.log('encryptedData:'+encryptedData);
		}

		return output;
	},
	DecryptMsg:function(key, iv, mode,plaintext){
		var output='';
		if(iv==''){
			iv=null;
		}

		//error checking

		var E0005 = ErrorCheck.E0005(iv);
		var E0009 = ErrorCheck.E0009(mode);

		if(E0005 !=''){
			return E0005;
		}
		if(E0009 !=''){
			return E0009;
		}
		//error checking

		output = WPCommonJS.WPTriDesDecrypt(plaintext,mode,key,iv);
		return output.toUpperCase();
	},
	encryptAlphaPINAndGenerateMAC:function(modulus, exponent, triDesKeyLen, iv, anpin, data){
		WPCommonJS.gen256PINHex();
		WPCommonJS.gen512PINHex();
		WPCommonJS.gen256MACHex();
		WPCommonJS.gen512MACHex();
		WPCommonJS.genIVHex();
		WPCommonJS.genPinkey();
		WPCommonJS.genMACkey();
		WPCommonJS.gen512Hex();

		var debug=0;
		if(iv==''){
			iv=null;
		}

		//error checking
		var E0002 = ErrorCheck.E0002(modulus);
		var E0003 = ErrorCheck.E0003(exponent);
		var E0004 = ErrorCheck.E0004(triDesKeyLen);
		var E0005 = ErrorCheck.E0005(iv);
		var E0007 = ErrorCheck.E0007(anpin);
		if(E0002 !=''){
			return E0002;
		}
		if(E0003 !=''){
			return E0003;
		}
		if(E0004 !=''){
			return E0004;
		}
		if(E0005 !=''){
			return E0005;
		}
		if(E0007 !=''){
			return E0007;
		}
		//error checking

		var output = '220';
		var modlen = modulus.length;
		var rsaKeyLen= '1';
		if(modlen==256){
			rsaKeyLen='1';
		}else if(modlen==512){
			rsaKeyLen ='2';
		}

		if(iv==null){
			iv=window.WPIVHex;
		}


		//output = output+rsaKeyLen+triDesKeyLen;


		k1=WPCommonJS.HexOdd(window.WPPINKey1);
		k2=WPCommonJS.HexOdd(window.WPPINKey2);
		k3=WPCommonJS.HexOdd(window.WPPINKey3);

		if(debug==1){
			console.log('Modulus:'+modulus);
			console.log('Exponent:'+exponent);
			console.log('TriDes Key Length:'+triDesKeyLen);
			console.log('iv:'+iv);
			console.log('k1:'+k1);
			console.log('k2:'+k2);
			if(triDesKeyLen=='3'){
				console.log('k3:'+k3);
			}
			console.log('Anpin:'+anpin);
			console.log('Plaintext:'+data);
		}

		//------------------------------------
		//RSA PIN Key Encrypt
		//------------------------------------
		if(rsaKeyLen=='1'){

			temp=window.WP256PINHex;
			//temp = temp.replace(/0/g,'F');
			temp = temp.replace(/0/g,'F');
			temp=WPCommonJS.setCharAt(temp,0,'0');
			temp=WPCommonJS.setCharAt(temp,1,'0');
			temp=WPCommonJS.setCharAt(temp,2,'0');
			temp=WPCommonJS.setCharAt(temp,3,'2');



			if(triDesKeyLen=='2'){
				temp=WPCommonJS.setCharAt(temp,194,'0');
				temp=WPCommonJS.setCharAt(temp,195,'0');

				temp=WPCommonJS.setCharAt(temp,196,'3');
				temp=WPCommonJS.setCharAt(temp,197,'0');
				temp=WPCommonJS.setCharAt(temp,198,'1');
				temp=WPCommonJS.setCharAt(temp,199,'C');

				temp=WPCommonJS.setCharAt(temp,200,'0');
				temp=WPCommonJS.setCharAt(temp,201,'4');
				temp=WPCommonJS.setCharAt(temp,202,'1');
				temp=WPCommonJS.setCharAt(temp,203,'0');

				temp=WPCommonJS.setCharAt(temp,236,'0');
				temp=WPCommonJS.setCharAt(temp,237,'4');
				temp=WPCommonJS.setCharAt(temp,238,'0');
				temp=WPCommonJS.setCharAt(temp,239,'8');



				for(var i=204; i<220; i++){
					temp=WPCommonJS.setCharAt(temp,i,k1.charAt(i-204));
				}
				for(var i=220; i<236; i++){
					temp=WPCommonJS.setCharAt(temp,i,k2.charAt(i-220));
				}

			}else if(triDesKeyLen =='3'){
				temp=WPCommonJS.setCharAt(temp,178,'0');
				temp=WPCommonJS.setCharAt(temp,179,'0');

				temp=WPCommonJS.setCharAt(temp,180,'3');
				temp=WPCommonJS.setCharAt(temp,181,'0');
				temp=WPCommonJS.setCharAt(temp,182,'2');
				temp=WPCommonJS.setCharAt(temp,183,'4');

				temp=WPCommonJS.setCharAt(temp,184,'0');
				temp=WPCommonJS.setCharAt(temp,185,'4');
				temp=WPCommonJS.setCharAt(temp,186,'1');
				temp=WPCommonJS.setCharAt(temp,187,'8');

				temp=WPCommonJS.setCharAt(temp,236,'0');
				temp=WPCommonJS.setCharAt(temp,237,'4');
				temp=WPCommonJS.setCharAt(temp,238,'0');
				temp=WPCommonJS.setCharAt(temp,239,'8');

				for(var i=188; i<204; i++){
					temp=WPCommonJS.setCharAt(temp,i,k1.charAt(i-188));
				}
				for(var i=204; i<220; i++){
					temp=WPCommonJS.setCharAt(temp,i,k2.charAt(i-204));
				}
				for(var i=220; i<236; i++){
					temp=WPCommonJS.setCharAt(temp,i,k3.charAt(i-220));
				}
			}


			for(var i=240; i<256; i++){
				temp=WPCommonJS.setCharAt(temp,i,iv.charAt(i-240));
			}

		}else if(rsaKeyLen=='2'){
			temp=window.WP512PINHex;
			temp = temp.replace(/0/g,'F');
			temp=WPCommonJS.setCharAt(temp,0,'0');
			temp=WPCommonJS.setCharAt(temp,1,'0');
			temp=WPCommonJS.setCharAt(temp,2,'0');
			temp=WPCommonJS.setCharAt(temp,3,'2');


			if(triDesKeyLen=='2'){
				temp=WPCommonJS.setCharAt(temp,450,'0');
				temp=WPCommonJS.setCharAt(temp,451,'0');

				temp=WPCommonJS.setCharAt(temp,452,'3');
				temp=WPCommonJS.setCharAt(temp,453,'0');
				temp=WPCommonJS.setCharAt(temp,454,'1');
				temp=WPCommonJS.setCharAt(temp,455,'C');

				temp=WPCommonJS.setCharAt(temp,456,'0');
				temp=WPCommonJS.setCharAt(temp,457,'4');
				temp=WPCommonJS.setCharAt(temp,458,'1');
				temp=WPCommonJS.setCharAt(temp,459,'0');

				temp=WPCommonJS.setCharAt(temp,492,'0');
				temp=WPCommonJS.setCharAt(temp,493,'4');
				temp=WPCommonJS.setCharAt(temp,494,'0');
				temp=WPCommonJS.setCharAt(temp,495,'8');



				for(var i=460; i<476; i++){
					temp=WPCommonJS.setCharAt(temp,i,k1.charAt(i-460));
				}
				for(var i=476; i<492; i++){
					temp=WPCommonJS.setCharAt(temp,i,k2.charAt(i-476));
				}

			}else if(triDesKeyLen =='3'){
				temp=WPCommonJS.setCharAt(temp,434,'0');
				temp=WPCommonJS.setCharAt(temp,435,'0');

				temp=WPCommonJS.setCharAt(temp,436,'3');
				temp=WPCommonJS.setCharAt(temp,437,'0');
				temp=WPCommonJS.setCharAt(temp,438,'2');
				temp=WPCommonJS.setCharAt(temp,439,'4');

				temp=WPCommonJS.setCharAt(temp,440,'0');
				temp=WPCommonJS.setCharAt(temp,441,'4');
				temp=WPCommonJS.setCharAt(temp,442,'1');
				temp=WPCommonJS.setCharAt(temp,443,'8');

				temp=WPCommonJS.setCharAt(temp,492,'0');
				temp=WPCommonJS.setCharAt(temp,493,'4');
				temp=WPCommonJS.setCharAt(temp,494,'0');
				temp=WPCommonJS.setCharAt(temp,495,'8');

				for(var i=444; i<460; i++){
					temp=WPCommonJS.setCharAt(temp,i,k1.charAt(i-444));
				}
				for(var i=460; i<476; i++){
					temp=WPCommonJS.setCharAt(temp,i,k2.charAt(i-460));
				}
				for(var i=476; i<492; i++){
					temp=WPCommonJS.setCharAt(temp,i,k3.charAt(i-476));
				}
			}


			for(var i=496; i<512; i++){
				temp=WPCommonJS.setCharAt(temp,i,iv.charAt(i-496));
			}

		}
		//console.log('Data Encrypt Key Before RSA:'+temp);
		//console.log(modulus);
		//modulus = 'BA4318B1C46025FFA97142AE3D10A6E9030D0462D95002B7692DF37785728D6EA3B06B848839B207536C86450531FF198AF8DA93862B92599ACCF741EBA8B9EA706C01D5100B03E7DAAB3BC03451174BD679478276C807E54E509880245421ADB8E865B4B5EC363F394BC13187647AAB15FE75DE99AEAAAA463F7A4DA5BBC56284E0C38AB2B26639E4D0DE494878BBB85E63EC5DB6F517F3C1CC474959354647376A5DC17BCEE66FF0C14499C0964A4EC6565E61CB3FE6B3DCB9405F41DE3495A35AC6D03219EB4A12BA35026011BC0B233352D4506374246884EB49ECEFA3367ED9A0A6C9EAA444BB3DF25C36E66331D848FA38E32BA94ACD67E1E88976B3A9';
		//temp = '0002038D310EC2F50D37562A32312EC773223B4833C454EFB59AAA93B60A6BEDA904C68D71F5E30FDA9A4D4E5021976904F34079B78596A19A1BE1C209EE0D6AE56ED386339134E7856FCA1BDC2F4DD21C2207C3575F9CA94F94816CD132EF2E29515CC22561394483F0B4A57702538749A4867682A80217BEC9FA616997C1015CA2D9E8925840CAF3C122D76A8AC4BAE5C6D8AC4BDF56D5851FE487B113770AF7CB7AA13BFA7EDCD2B1A4FC42BF886CD67E6FA962CC1B812C1D66F356511B30854D587B3F5536289F716302EA8C6EC9E2A7C3F7BBFB51C92A003024041832E52075E33DFE193ECB57E6E9E5F80185D90B4AB33125B304084A4C97BA981E209D';
		var outputrsapin = WPCommonJS.WPRSAEncrypt(modulus,exponent,temp);



		if(debug==1){
			console.log('pin key1:'+k1);
			console.log('pin key2:'+k2);

			if(triDesKeyLen=='3'){
				console.log('pin key3:'+k3);
			}
			console.log('pin input:'+temp);
			console.log('Encrypt Pin RSA:'+outputrsapin);
		}

		//------------------------------------
		//RSA MAC Key Encrypt
		//------------------------------------
		k1=WPCommonJS.HexOdd(window.WPMACKey1);
		k2=WPCommonJS.HexOdd(window.WPMACKey2);
		k3=WPCommonJS.HexOdd(window.WPMACKey3);


		temp='';
		if(rsaKeyLen=='1'){

			temp=window.WP256MACHex;
			temp = temp.replace(/0/g,'F');
			temp=WPCommonJS.setCharAt(temp,0,'0');
			temp=WPCommonJS.setCharAt(temp,1,'0');
			temp=WPCommonJS.setCharAt(temp,2,'0');
			temp=WPCommonJS.setCharAt(temp,3,'2');



			if(triDesKeyLen=='2'){
				temp=WPCommonJS.setCharAt(temp,194,'0');
				temp=WPCommonJS.setCharAt(temp,195,'0');

				temp=WPCommonJS.setCharAt(temp,196,'3');
				temp=WPCommonJS.setCharAt(temp,197,'0');
				temp=WPCommonJS.setCharAt(temp,198,'1');
				temp=WPCommonJS.setCharAt(temp,199,'C');

				temp=WPCommonJS.setCharAt(temp,200,'0');
				temp=WPCommonJS.setCharAt(temp,201,'4');
				temp=WPCommonJS.setCharAt(temp,202,'1');
				temp=WPCommonJS.setCharAt(temp,203,'0');

				temp=WPCommonJS.setCharAt(temp,236,'0');
				temp=WPCommonJS.setCharAt(temp,237,'4');
				temp=WPCommonJS.setCharAt(temp,238,'0');
				temp=WPCommonJS.setCharAt(temp,239,'8');



				for(var i=204; i<220; i++){
					temp=WPCommonJS.setCharAt(temp,i,k1.charAt(i-204));
				}
				for(var i=220; i<236; i++){
					temp=WPCommonJS.setCharAt(temp,i,k2.charAt(i-220));
				}

			}else if(triDesKeyLen =='3'){
				temp=WPCommonJS.setCharAt(temp,178,'0');
				temp=WPCommonJS.setCharAt(temp,179,'0');

				temp=WPCommonJS.setCharAt(temp,180,'3');
				temp=WPCommonJS.setCharAt(temp,181,'0');
				temp=WPCommonJS.setCharAt(temp,182,'2');
				temp=WPCommonJS.setCharAt(temp,183,'4');

				temp=WPCommonJS.setCharAt(temp,184,'0');
				temp=WPCommonJS.setCharAt(temp,185,'4');
				temp=WPCommonJS.setCharAt(temp,186,'1');
				temp=WPCommonJS.setCharAt(temp,187,'8');

				temp=WPCommonJS.setCharAt(temp,236,'0');
				temp=WPCommonJS.setCharAt(temp,237,'4');
				temp=WPCommonJS.setCharAt(temp,238,'0');
				temp=WPCommonJS.setCharAt(temp,239,'8');

				for(var i=188; i<204; i++){
					temp=WPCommonJS.setCharAt(temp,i,k1.charAt(i-188));
				}
				for(var i=204; i<220; i++){
					temp=WPCommonJS.setCharAt(temp,i,k2.charAt(i-204));
				}
				for(var i=220; i<236; i++){
					temp=WPCommonJS.setCharAt(temp,i,k3.charAt(i-220));
				}
			}


			for(var i=240; i<256; i++){
				temp=WPCommonJS.setCharAt(temp,i,iv.charAt(i-240));
			}

		}else if(rsaKeyLen=='2'){
			temp=window.WP512MACHex;
			temp = temp.replace(/0/g,'F');
			temp=WPCommonJS.setCharAt(temp,0,'0');
			temp=WPCommonJS.setCharAt(temp,1,'0');
			temp=WPCommonJS.setCharAt(temp,2,'0');
			temp=WPCommonJS.setCharAt(temp,3,'2');


			if(triDesKeyLen=='2'){
				temp=WPCommonJS.setCharAt(temp,450,'0');
				temp=WPCommonJS.setCharAt(temp,451,'0');

				temp=WPCommonJS.setCharAt(temp,452,'3');
				temp=WPCommonJS.setCharAt(temp,453,'0');
				temp=WPCommonJS.setCharAt(temp,454,'1');
				temp=WPCommonJS.setCharAt(temp,455,'C');

				temp=WPCommonJS.setCharAt(temp,456,'0');
				temp=WPCommonJS.setCharAt(temp,457,'4');
				temp=WPCommonJS.setCharAt(temp,458,'1');
				temp=WPCommonJS.setCharAt(temp,459,'0');

				temp=WPCommonJS.setCharAt(temp,492,'0');
				temp=WPCommonJS.setCharAt(temp,493,'4');
				temp=WPCommonJS.setCharAt(temp,494,'0');
				temp=WPCommonJS.setCharAt(temp,495,'8');



				for(var i=460; i<476; i++){
					temp=WPCommonJS.setCharAt(temp,i,k1.charAt(i-460));
				}
				for(var i=476; i<492; i++){
					temp=WPCommonJS.setCharAt(temp,i,k2.charAt(i-476));
				}

			}else if(triDesKeyLen =='3'){
				temp=WPCommonJS.setCharAt(temp,434,'0');
				temp=WPCommonJS.setCharAt(temp,435,'0');

				temp=WPCommonJS.setCharAt(temp,436,'3');
				temp=WPCommonJS.setCharAt(temp,437,'0');
				temp=WPCommonJS.setCharAt(temp,438,'2');
				temp=WPCommonJS.setCharAt(temp,439,'4');

				temp=WPCommonJS.setCharAt(temp,440,'0');
				temp=WPCommonJS.setCharAt(temp,441,'4');
				temp=WPCommonJS.setCharAt(temp,442,'1');
				temp=WPCommonJS.setCharAt(temp,443,'8');

				temp=WPCommonJS.setCharAt(temp,492,'0');
				temp=WPCommonJS.setCharAt(temp,493,'4');
				temp=WPCommonJS.setCharAt(temp,494,'0');
				temp=WPCommonJS.setCharAt(temp,495,'8');

				for(var i=444; i<460; i++){
					temp=WPCommonJS.setCharAt(temp,i,k1.charAt(i-444));
				}
				for(var i=460; i<476; i++){
					temp=WPCommonJS.setCharAt(temp,i,k2.charAt(i-460));
				}
				for(var i=476; i<492; i++){
					temp=WPCommonJS.setCharAt(temp,i,k3.charAt(i-476));
				}
			}


			for(var i=496; i<512; i++){
				temp=WPCommonJS.setCharAt(temp,i,iv.charAt(i-496));
			}

		}

		var outputrsamac = WPCommonJS.WPRSAEncrypt(modulus,exponent,temp);


		if(debug==1){
			console.log('mac key1:'+k1);
			console.log('mac key2:'+k2);
			if(triDesKeyLen=='3'){
				console.log('mac key3:'+k3);
			}
			console.log('Mac Input:'+temp);
			console.log('Encrypted RSA MAC:'+outputrsamac);
		}

		var anpinlen = 16 - anpin.length ;
		for(var i=0; i<anpinlen; i++){
			anpin = anpin+' ';
		}

		var anpinHex = WPCommonJS.Ascii2Hex(anpin);
		var PINKey1 = WPCommonJS.HexOdd(window.WPPINKey1);
		var PINKey2 = WPCommonJS.HexOdd(window.WPPINKey2);
		var PINKey3 = WPCommonJS.HexOdd(window.WPPINKey3);

		encryptedAnpin = WPCommonJS.WPTriDesEncrypt(anpinHex,'2',triDesKeyLen,PINKey1,PINKey2,PINKey3,iv);

		//var asciidata = WPCommonJS.Ascii2Hex(data);
		output=output +rsaKeyLen+triDesKeyLen+outputrsapin.toUpperCase()+outputrsamac.toUpperCase()+encryptedAnpin.toUpperCase()+data;
		var main = output;
		output = WPCommonJS.Ascii2Hex(output);
		if(debug==1){
			console.log('Anpin Hex:'+anpinHex);
			console.log('Encrypt Anpin Hex:'+encryptedAnpin);


			//console.log('Ascii Data to Hex:'+asciidata);
			console.log('output before mac:'+output);
		}

		var outputlen = output.length;
		var pad = 16- outputlen%16;
		if(pad!=16){
			for(var i=0; i<pad; i++){
				output=output+'0';
			}
		}
		if(debug==1){
			console.log('output before mac(padded zero):'+output);
		}
		zeroiv = '0000000000000000';

		var macout1 = WPCommonJS.WPTriDesEncrypt(output,'2','3',k1,k1, k1, zeroiv );
		if(debug==1){
			console.log('Mac First TDES Encrypt Plaintext:'+output);
			console.log('k1:'+k1);
			console.log('iv:'+zeroiv);
			console.log('TDES Encrypt Result:'+macout1);
		}
		outputlen = output.length;
		var plain2 = macout1.substr(outputlen-16,16);
		var key2 = k2+k2+k2;
		//WPTriDesDecrypt:function(plaintext,mode,keyHex,ivhex){
		var macout2 = WPCommonJS.WPTriDesDecrypt(plain2,'2',key2, zeroiv );
		if(debug==1){
			console.log('Mac Second TDES Decrypt Plaintext:'+plain2);
			console.log('k2:'+k2);
			console.log('iv:'+zeroiv);
			console.log('TDES Decrypt Result:'+macout2);
		}
		var mac ='';
		if(triDesKeyLen=='2'){
			mac = WPCommonJS.WPTriDesEncrypt(macout2,'2','3',k1,k1, k1, zeroiv );
			if(debug==1){
				console.log('Mac Third TDES Encrypt Plaintext:'+macout2);
				console.log('k1:'+k1);
				console.log('iv:'+zeroiv);
				console.log('TDES Encrypt Result:'+mac);
			}
		}else if(triDesKeyLen=='3'){
			mac = WPCommonJS.WPTriDesEncrypt(macout2,'2','3',k3,k3, k3, zeroiv );
			if(debug==1){
				console.log('Mac Third TDES Encrypt Plaintext:'+macout2);
				console.log('k3:'+k3);
				console.log('iv:'+zeroiv);
				console.log('TDES Encrypt Result:'+mac);
			}
		}
		mac = mac.substr(0,8);

		output=main+mac.toUpperCase();

		if(debug==1){
			console.log('MAC:'+mac);
			console.log('OUTPUT:\n'+output);
		}
		return output;
	},
	encryptChangeAlphaPINAndGenerateMAC:function(modulus, exponent, triDesKeyLen, iv, anpin,newanpin, data){
		WPCommonJS.gen256PINHex();
		WPCommonJS.gen512PINHex();
		WPCommonJS.gen256MACHex();
		WPCommonJS.gen512MACHex();
		WPCommonJS.genIVHex();
		WPCommonJS.genPinkey();
		WPCommonJS.genMACkey();

		if(iv==''){
			iv=null;
		}

		//error checking
		var E0002 = ErrorCheck.E0002(modulus);
		var E0003 = ErrorCheck.E0003(exponent);
		var E0004 = ErrorCheck.E0004(triDesKeyLen);
		var E0005 = ErrorCheck.E0005(iv);
		var E0007 = ErrorCheck.E0007(anpin);
		var E0008 = ErrorCheck.E0007(newanpin);
		if(E0002 !=''){
			return E0002;
		}
		if(E0003 !=''){
			return E0003;
		}
		if(E0004 !=''){
			return E0004;
		}
		if(E0005 !=''){
			return E0005;
		}
		if(E0007 !=''){
			return E0007;
		}
		if(E0008 !=''){
			return E0008;
		}
		//error checking

		var debug=0;


		var output = '221';
		var modlen = modulus.length;
		var rsaKeyLen= '1';
		if(modlen==256){
			rsaKeyLen='1';
		}else if(modlen==512){
			rsaKeyLen ='2';
		}

		if(iv==null){
			iv=window.WPIVHex;
		}


		//output = output+rsaKeyLen+triDesKeyLen;


		k1=WPCommonJS.HexOdd(window.WPPINKey1);
		k2=WPCommonJS.HexOdd(window.WPPINKey2);
		k3=WPCommonJS.HexOdd(window.WPPINKey3);

		if(debug==1){
			console.log('Modulus:'+modulus);
			console.log('Exponent:'+exponent);
			console.log('TriDes Key Length:'+triDesKeyLen);
			console.log('iv:'+iv);
			console.log('k1:'+k1);
			console.log('k2:'+k2);
			if(triDesKeyLen=='3'){
				console.log('k3:'+k3);
			}
			console.log('Old Anpin:'+anpin);
			console.log('New Anpin:'+newanpin);
			console.log('Plaintext:'+data);
		}

		//------------------------------------
		//RSA PIN Key Encrypt
		//------------------------------------
		if(rsaKeyLen=='1'){

			temp=window.WP256PINHex;
			temp = temp.replace(/0/g,'F');
			temp=WPCommonJS.setCharAt(temp,0,'0');
			temp=WPCommonJS.setCharAt(temp,1,'0');
			temp=WPCommonJS.setCharAt(temp,2,'0');
			temp=WPCommonJS.setCharAt(temp,3,'2');



			if(triDesKeyLen=='2'){
				temp=WPCommonJS.setCharAt(temp,194,'0');
				temp=WPCommonJS.setCharAt(temp,195,'0');

				temp=WPCommonJS.setCharAt(temp,196,'3');
				temp=WPCommonJS.setCharAt(temp,197,'0');
				temp=WPCommonJS.setCharAt(temp,198,'1');
				temp=WPCommonJS.setCharAt(temp,199,'C');

				temp=WPCommonJS.setCharAt(temp,200,'0');
				temp=WPCommonJS.setCharAt(temp,201,'4');
				temp=WPCommonJS.setCharAt(temp,202,'1');
				temp=WPCommonJS.setCharAt(temp,203,'0');

				temp=WPCommonJS.setCharAt(temp,236,'0');
				temp=WPCommonJS.setCharAt(temp,237,'4');
				temp=WPCommonJS.setCharAt(temp,238,'0');
				temp=WPCommonJS.setCharAt(temp,239,'8');



				for(var i=204; i<220; i++){
					temp=WPCommonJS.setCharAt(temp,i,k1.charAt(i-204));
				}
				for(var i=220; i<236; i++){
					temp=WPCommonJS.setCharAt(temp,i,k2.charAt(i-220));
				}

			}else if(triDesKeyLen =='3'){
				temp=WPCommonJS.setCharAt(temp,178,'0');
				temp=WPCommonJS.setCharAt(temp,179,'0');

				temp=WPCommonJS.setCharAt(temp,180,'3');
				temp=WPCommonJS.setCharAt(temp,181,'0');
				temp=WPCommonJS.setCharAt(temp,182,'2');
				temp=WPCommonJS.setCharAt(temp,183,'4');

				temp=WPCommonJS.setCharAt(temp,184,'0');
				temp=WPCommonJS.setCharAt(temp,185,'4');
				temp=WPCommonJS.setCharAt(temp,186,'1');
				temp=WPCommonJS.setCharAt(temp,187,'8');

				temp=WPCommonJS.setCharAt(temp,236,'0');
				temp=WPCommonJS.setCharAt(temp,237,'4');
				temp=WPCommonJS.setCharAt(temp,238,'0');
				temp=WPCommonJS.setCharAt(temp,239,'8');

				for(var i=188; i<204; i++){
					temp=WPCommonJS.setCharAt(temp,i,k1.charAt(i-188));
				}
				for(var i=204; i<220; i++){
					temp=WPCommonJS.setCharAt(temp,i,k2.charAt(i-204));
				}
				for(var i=220; i<236; i++){
					temp=WPCommonJS.setCharAt(temp,i,k3.charAt(i-220));
				}
			}


			for(var i=240; i<256; i++){
				temp=WPCommonJS.setCharAt(temp,i,iv.charAt(i-240));
			}

		}else if(rsaKeyLen=='2'){
			temp=window.WP512PINHex;
			temp = temp.replace(/0/g,'F');
			temp=WPCommonJS.setCharAt(temp,0,'0');
			temp=WPCommonJS.setCharAt(temp,1,'0');
			temp=WPCommonJS.setCharAt(temp,2,'0');
			temp=WPCommonJS.setCharAt(temp,3,'2');


			if(triDesKeyLen=='2'){
				temp=WPCommonJS.setCharAt(temp,450,'0');
				temp=WPCommonJS.setCharAt(temp,451,'0');

				temp=WPCommonJS.setCharAt(temp,452,'3');
				temp=WPCommonJS.setCharAt(temp,453,'0');
				temp=WPCommonJS.setCharAt(temp,454,'1');
				temp=WPCommonJS.setCharAt(temp,455,'C');

				temp=WPCommonJS.setCharAt(temp,456,'0');
				temp=WPCommonJS.setCharAt(temp,457,'4');
				temp=WPCommonJS.setCharAt(temp,458,'1');
				temp=WPCommonJS.setCharAt(temp,459,'0');

				temp=WPCommonJS.setCharAt(temp,492,'0');
				temp=WPCommonJS.setCharAt(temp,493,'4');
				temp=WPCommonJS.setCharAt(temp,494,'0');
				temp=WPCommonJS.setCharAt(temp,495,'8');



				for(var i=460; i<476; i++){
					temp=WPCommonJS.setCharAt(temp,i,k1.charAt(i-460));
				}
				for(var i=476; i<492; i++){
					temp=WPCommonJS.setCharAt(temp,i,k2.charAt(i-476));
				}

			}else if(triDesKeyLen =='3'){
				temp=WPCommonJS.setCharAt(temp,434,'0');
				temp=WPCommonJS.setCharAt(temp,435,'0');

				temp=WPCommonJS.setCharAt(temp,436,'3');
				temp=WPCommonJS.setCharAt(temp,437,'0');
				temp=WPCommonJS.setCharAt(temp,438,'2');
				temp=WPCommonJS.setCharAt(temp,439,'4');

				temp=WPCommonJS.setCharAt(temp,440,'0');
				temp=WPCommonJS.setCharAt(temp,441,'4');
				temp=WPCommonJS.setCharAt(temp,442,'1');
				temp=WPCommonJS.setCharAt(temp,443,'8');

				temp=WPCommonJS.setCharAt(temp,492,'0');
				temp=WPCommonJS.setCharAt(temp,493,'4');
				temp=WPCommonJS.setCharAt(temp,494,'0');
				temp=WPCommonJS.setCharAt(temp,495,'8');

				for(var i=444; i<460; i++){
					temp=WPCommonJS.setCharAt(temp,i,k1.charAt(i-444));
				}
				for(var i=460; i<476; i++){
					temp=WPCommonJS.setCharAt(temp,i,k2.charAt(i-460));
				}
				for(var i=476; i<492; i++){
					temp=WPCommonJS.setCharAt(temp,i,k3.charAt(i-476));
				}
			}


			for(var i=496; i<512; i++){
				temp=WPCommonJS.setCharAt(temp,i,iv.charAt(i-496));
			}

		}
		//console.log('Data Encrypt Key Before RSA:'+temp);
		//console.log(modulus);
		//modulus = 'BA4318B1C46025FFA97142AE3D10A6E9030D0462D95002B7692DF37785728D6EA3B06B848839B207536C86450531FF198AF8DA93862B92599ACCF741EBA8B9EA706C01D5100B03E7DAAB3BC03451174BD679478276C807E54E509880245421ADB8E865B4B5EC363F394BC13187647AAB15FE75DE99AEAAAA463F7A4DA5BBC56284E0C38AB2B26639E4D0DE494878BBB85E63EC5DB6F517F3C1CC474959354647376A5DC17BCEE66FF0C14499C0964A4EC6565E61CB3FE6B3DCB9405F41DE3495A35AC6D03219EB4A12BA35026011BC0B233352D4506374246884EB49ECEFA3367ED9A0A6C9EAA444BB3DF25C36E66331D848FA38E32BA94ACD67E1E88976B3A9';
		//temp = '0002038D310EC2F50D37562A32312EC773223B4833C454EFB59AAA93B60A6BEDA904C68D71F5E30FDA9A4D4E5021976904F34079B78596A19A1BE1C209EE0D6AE56ED386339134E7856FCA1BDC2F4DD21C2207C3575F9CA94F94816CD132EF2E29515CC22561394483F0B4A57702538749A4867682A80217BEC9FA616997C1015CA2D9E8925840CAF3C122D76A8AC4BAE5C6D8AC4BDF56D5851FE487B113770AF7CB7AA13BFA7EDCD2B1A4FC42BF886CD67E6FA962CC1B812C1D66F356511B30854D587B3F5536289F716302EA8C6EC9E2A7C3F7BBFB51C92A003024041832E52075E33DFE193ECB57E6E9E5F80185D90B4AB33125B304084A4C97BA981E209D';
		var outputrsapin = WPCommonJS.WPRSAEncrypt(modulus,exponent,temp);



		if(debug==1){
			console.log('pin key1:'+k1);
			console.log('pin key2:'+k2);

			if(triDesKeyLen=='3'){
				console.log('pin key3:'+k3);
			}
			console.log('pin input:'+temp);
			console.log('Encrypt Pin RSA:'+outputrsapin);
		}

		//------------------------------------
		//RSA MAC Key Encrypt
		//------------------------------------
		k1=WPCommonJS.HexOdd(window.WPMACKey1);
		k2=WPCommonJS.HexOdd(window.WPMACKey2);
		k3=WPCommonJS.HexOdd(window.WPMACKey3);


		temp='';
		if(rsaKeyLen=='1'){

			temp=window.WP256MACHex;
			temp = temp.replace(/0/g,'F');
			temp=WPCommonJS.setCharAt(temp,0,'0');
			temp=WPCommonJS.setCharAt(temp,1,'0');
			temp=WPCommonJS.setCharAt(temp,2,'0');
			temp=WPCommonJS.setCharAt(temp,3,'2');



			if(triDesKeyLen=='2'){
				temp=WPCommonJS.setCharAt(temp,194,'0');
				temp=WPCommonJS.setCharAt(temp,195,'0');

				temp=WPCommonJS.setCharAt(temp,196,'3');
				temp=WPCommonJS.setCharAt(temp,197,'0');
				temp=WPCommonJS.setCharAt(temp,198,'1');
				temp=WPCommonJS.setCharAt(temp,199,'C');

				temp=WPCommonJS.setCharAt(temp,200,'0');
				temp=WPCommonJS.setCharAt(temp,201,'4');
				temp=WPCommonJS.setCharAt(temp,202,'1');
				temp=WPCommonJS.setCharAt(temp,203,'0');

				temp=WPCommonJS.setCharAt(temp,236,'0');
				temp=WPCommonJS.setCharAt(temp,237,'4');
				temp=WPCommonJS.setCharAt(temp,238,'0');
				temp=WPCommonJS.setCharAt(temp,239,'8');



				for(var i=204; i<220; i++){
					temp=WPCommonJS.setCharAt(temp,i,k1.charAt(i-204));
				}
				for(var i=220; i<236; i++){
					temp=WPCommonJS.setCharAt(temp,i,k2.charAt(i-220));
				}

			}else if(triDesKeyLen =='3'){
				temp=WPCommonJS.setCharAt(temp,178,'0');
				temp=WPCommonJS.setCharAt(temp,179,'0');

				temp=WPCommonJS.setCharAt(temp,180,'3');
				temp=WPCommonJS.setCharAt(temp,181,'0');
				temp=WPCommonJS.setCharAt(temp,182,'2');
				temp=WPCommonJS.setCharAt(temp,183,'4');

				temp=WPCommonJS.setCharAt(temp,184,'0');
				temp=WPCommonJS.setCharAt(temp,185,'4');
				temp=WPCommonJS.setCharAt(temp,186,'1');
				temp=WPCommonJS.setCharAt(temp,187,'8');

				temp=WPCommonJS.setCharAt(temp,236,'0');
				temp=WPCommonJS.setCharAt(temp,237,'4');
				temp=WPCommonJS.setCharAt(temp,238,'0');
				temp=WPCommonJS.setCharAt(temp,239,'8');

				for(var i=188; i<204; i++){
					temp=WPCommonJS.setCharAt(temp,i,k1.charAt(i-188));
				}
				for(var i=204; i<220; i++){
					temp=WPCommonJS.setCharAt(temp,i,k2.charAt(i-204));
				}
				for(var i=220; i<236; i++){
					temp=WPCommonJS.setCharAt(temp,i,k3.charAt(i-220));
				}
			}


			for(var i=240; i<256; i++){
				temp=WPCommonJS.setCharAt(temp,i,iv.charAt(i-240));
			}

		}else if(rsaKeyLen=='2'){
			temp=window.WP512MACHex;
			temp = temp.replace(/0/g,'F');
			temp=WPCommonJS.setCharAt(temp,0,'0');
			temp=WPCommonJS.setCharAt(temp,1,'0');
			temp=WPCommonJS.setCharAt(temp,2,'0');
			temp=WPCommonJS.setCharAt(temp,3,'2');


			if(triDesKeyLen=='2'){
				temp=WPCommonJS.setCharAt(temp,450,'0');
				temp=WPCommonJS.setCharAt(temp,451,'0');

				temp=WPCommonJS.setCharAt(temp,452,'3');
				temp=WPCommonJS.setCharAt(temp,453,'0');
				temp=WPCommonJS.setCharAt(temp,454,'1');
				temp=WPCommonJS.setCharAt(temp,455,'C');

				temp=WPCommonJS.setCharAt(temp,456,'0');
				temp=WPCommonJS.setCharAt(temp,457,'4');
				temp=WPCommonJS.setCharAt(temp,458,'1');
				temp=WPCommonJS.setCharAt(temp,459,'0');

				temp=WPCommonJS.setCharAt(temp,492,'0');
				temp=WPCommonJS.setCharAt(temp,493,'4');
				temp=WPCommonJS.setCharAt(temp,494,'0');
				temp=WPCommonJS.setCharAt(temp,495,'8');



				for(var i=460; i<476; i++){
					temp=WPCommonJS.setCharAt(temp,i,k1.charAt(i-460));
				}
				for(var i=476; i<492; i++){
					temp=WPCommonJS.setCharAt(temp,i,k2.charAt(i-476));
				}

			}else if(triDesKeyLen =='3'){
				temp=WPCommonJS.setCharAt(temp,434,'0');
				temp=WPCommonJS.setCharAt(temp,435,'0');

				temp=WPCommonJS.setCharAt(temp,436,'3');
				temp=WPCommonJS.setCharAt(temp,437,'0');
				temp=WPCommonJS.setCharAt(temp,438,'2');
				temp=WPCommonJS.setCharAt(temp,439,'4');

				temp=WPCommonJS.setCharAt(temp,440,'0');
				temp=WPCommonJS.setCharAt(temp,441,'4');
				temp=WPCommonJS.setCharAt(temp,442,'1');
				temp=WPCommonJS.setCharAt(temp,443,'8');

				temp=WPCommonJS.setCharAt(temp,492,'0');
				temp=WPCommonJS.setCharAt(temp,493,'4');
				temp=WPCommonJS.setCharAt(temp,494,'0');
				temp=WPCommonJS.setCharAt(temp,495,'8');

				for(var i=444; i<460; i++){
					temp=WPCommonJS.setCharAt(temp,i,k1.charAt(i-444));
				}
				for(var i=460; i<476; i++){
					temp=WPCommonJS.setCharAt(temp,i,k2.charAt(i-460));
				}
				for(var i=476; i<492; i++){
					temp=WPCommonJS.setCharAt(temp,i,k3.charAt(i-476));
				}
			}


			for(var i=496; i<512; i++){
				temp=WPCommonJS.setCharAt(temp,i,iv.charAt(i-496));
			}

		}

		var outputrsamac = WPCommonJS.WPRSAEncrypt(modulus,exponent,temp);


		if(debug==1){
			console.log('mac key1:'+k1);
			console.log('mac key2:'+k2);
			if(triDesKeyLen=='3'){
				console.log('mac key3:'+k3);
			}
			console.log('Mac Input:'+temp);
			console.log('Encrypted RSA MAC:'+outputrsamac);
		}

		var anpinlen = 16 - anpin.length ;
		for(var i=0; i<anpinlen; i++){
			anpin = anpin+' ';
		}
		var newanpinlen = 16 - newanpin.length ;
		for(var i=0; i<newanpinlen; i++){
			newanpin = newanpin+' ';
		}
		var anpinHex = WPCommonJS.Ascii2Hex(anpin);
		var newanpinHex = WPCommonJS.Ascii2Hex(newanpin);
		var PINKey1 = WPCommonJS.HexOdd(window.WPPINKey1);
		var PINKey2 = WPCommonJS.HexOdd(window.WPPINKey2);
		var PINKey3 = WPCommonJS.HexOdd(window.WPPINKey3);

		encryptedAnpin = WPCommonJS.WPTriDesEncrypt(anpinHex,'2',triDesKeyLen,PINKey1,PINKey2,PINKey3,iv);
		encryptedNewAnpin = WPCommonJS.WPTriDesEncrypt(newanpinHex,'2',triDesKeyLen,PINKey1,PINKey2,PINKey3,iv);
		//var asciidata = WPCommonJS.Ascii2Hex(data);
		output=output +rsaKeyLen+triDesKeyLen+outputrsapin.toUpperCase()+outputrsamac.toUpperCase()+encryptedAnpin.toUpperCase()+encryptedNewAnpin.toUpperCase()+data;
		var main = output;
		output = WPCommonJS.Ascii2Hex(output);

		if(debug==1){
			console.log('Anpin Hex:'+anpinHex);
			console.log('New Anpin Hex:'+newanpinHex);
			console.log('Encrypt Anpin Hex:'+encryptedAnpin);
			console.log('Encrypt New Anpin Hex:'+encryptedNewAnpin);
			//console.log('Ascii Data to Hex:'+asciidata);
			console.log('output before mac:'+output);
		}

		var outputlen = output.length;
		var pad = 16- outputlen%16;
		if(pad!=16){
			for(var i=0; i<pad; i++){
				output=output+'0';
			}
		}
		if(debug==1){
			console.log('output before mac(padded zero):'+output);
		}
		zeroiv = '0000000000000000';
		var macout1 = WPCommonJS.WPTriDesEncrypt(output,'2','3',k1,k1, k1, zeroiv );
		if(debug==1){
			console.log('Mac First TDES Encrypt Plaintext:'+output);
			console.log('k1:'+k1);
			console.log('iv:'+zeroiv);
			console.log('TDES Encrypt Result:'+macout1);
		}
		outputlen = output.length;
		var plain2 = macout1.substr(outputlen-16,16);

		var key2 = k2+k2+k2;
		var macout2 = WPCommonJS.WPTriDesDecrypt(plain2,'2',key2, zeroiv );
		if(debug==1){
			console.log('Mac Second TDES Decrypt Plaintext:'+plain2);
			console.log('k2:'+k2);
			console.log('iv:'+zeroiv);
			console.log('TDES Encrypt Result:'+macout2);
		}
		var mac ='';

		if(triDesKeyLen=='2'){
			mac = WPCommonJS.WPTriDesEncrypt(macout2,'2','3',k1,k1, k1, zeroiv );
			if(debug==1){
				console.log('Mac Third TDES Encrypt Plaintext:'+macout2);
				console.log('k1:'+k1);
				console.log('iv:'+zeroiv);
				console.log('TDES Encrypt Result:'+mac);
			}
		}else if(triDesKeyLen=='3'){
			mac = WPCommonJS.WPTriDesEncrypt(macout2,'2','3',k3,k3, k3, zeroiv );
			if(debug==1){
				console.log('Mac Third TDES Encrypt Plaintext:'+macout2);
				console.log('k3:'+k3);
				console.log('iv:'+zeroiv);
				console.log('TDES Encrypt Result:'+mac);
			}
		}
		mac = mac.substr(0,8);

		output=main+mac.toUpperCase();
		if(debug==1){
			console.log('MAC:'+mac);
			console.log('OUTPUT:\n'+output);
		}

		return output;
	},
	getEncryptedPINKey:function(input){
		// type=20 , 2 20 2 1 2
		//version (1)+type(2)+RSAkeylen(1)+3DESKeylen(1)+ EncryptedPinKey (256 or 512)+ EncryptedMacKey (256 or 512)
		//+encryped Old anpin (32) + Data (?)+ Mac (8)

		// type=21
		//version (1)+type(2)+RSAkeylen(1)+3DESKeylen(1)+ EncryptedPinKey (256 or 512)+ EncryptedMacKey (256 or 512)
		//+encryped Old anpin (32) +encryped New anpin (32) + Data (?)+ Mac (8)
		var output ='';

		//Error Checking
		var version = input.substr(0,1);
		var type = input.substr(1,2);

		var E0011 = ErrorCheck.E0011(version);
		if(E0011!=''){
			return E0011;
		}
		if((type=='20')||(type=='21')){

		}else{
			return 'E0012';
		}
		//Error Checking

		var RSAkeylen = input.substr(3,1);
		if(RSAkeylen =='1'){
			output = input.substr(5,256);
		}else if(RSAkeylen =='2'){
			output = input.substr(5,512);
		}

		return output;
	},
	getEncryptedMACKey:function(input){
		var output ='';

		//Error Checking
		var version = input.substr(0,1);
		var type = input.substr(1,2);

		var E0011 = ErrorCheck.E0011(version);
		if(E0011!=''){
			return E0011;
		}
		if((type=='20')||(type=='21')){

		}else{
			return 'E0012';
		}
		//Error Checking

		var RSAkeylen = input.substr(3,1);
		if(RSAkeylen =='1'){
			output = input.substr(261,256);
		}else if(RSAkeylen =='2'){
			output = input.substr(517,512);
		}

		return output;
	},
	getEncryptedPINBlock:function(input){
		var output='';

		//Error Checking
		var version = input.substr(0,1);
		var type = input.substr(1,2);

		var E0011 = ErrorCheck.E0011(version);
		if(E0011!=''){
			return E0011;
		}
		if((type=='20')||(type=='21')){

		}else{
			return 'E0012';
		}
		//Error Checking
		var RSAkeylen = input.substr(3,1);
		if(RSAkeylen =='1'){
			output = input.substr(517,32);
		}else if(RSAkeylen =='2'){
			output = input.substr(1029,32);
		}
		return output;
	},
	getEncryptedNewPINBlock:function(input){
		var output='';

		//Error Checking
		var version = input.substr(0,1);
		var type = input.substr(1,2);

		var E0011 = ErrorCheck.E0011(version);
		if(E0011!=''){
			return E0011;
		}
		if(type=='21'){

		}else{
			return 'E0012';
		}
		//Error Checking
		var RSAkeylen = input.substr(3,1);
		if(RSAkeylen =='1'){
			output = input.substr(549,32);
		}else if(RSAkeylen =='2'){
			output = input.substr(1061,32);
		}
		return output;
	},
	getEncryptedKey:function(input){
		var output='';

		//Error Checking
		var version = input.substr(0,1);
		var type = input.substr(1,2);

		var E0011 = ErrorCheck.E0011(version);
		if(E0011!=''){
			return E0011;
		}
		if(type=='22'){

		}else{
			return 'E0012';
		}
		//Error Checking
		var RSAkeylen = input.substr(3,1);
		if(RSAkeylen =='1'){
			output = input.substr(5,256);
		}else if(RSAkeylen =='2'){
			output = input.substr(5,512);
		}
		return output;
	},
	getKey:function(input){
		var output='';

		//Error Checking
		var version = input.substr(0,1);
		var type = input.substr(1,2);
		var tdeslen = input.substr(4,1);
		var E0011 = ErrorCheck.E0011(version);
		if(E0011!=''){
			return E0011;
		}
		if(type=='22'){

		}else{
			return 'E0012';
		}
		//Error Checking
		var RSAkeylen = input.substr(3,1);
		if(RSAkeylen =='1'){
			if(tdeslen=='2'){
				output = input.substr(277,32);
			}else if(tdeslen=='3'){
				output = input.substr(277,48);
			}
		}else if(RSAkeylen =='2'){
			if(tdeslen=='2'){
				output = input.substr(533,32);
			}else if(tdeslen=='3'){
				output = input.substr(533,48);
			}
		}
		return output;
	},
	getEncryptedIVHex:function(input){
		var output='';

		//Error Checking
		var version = input.substr(0,1);
		var type = input.substr(1,2);

		var E0011 = ErrorCheck.E0011(version);
		if(E0011!=''){
			return E0011;
		}
		if(type=='22'){

		}else{
			return 'E0012';
		}
		//Error Checking
		var RSAkeylen = input.substr(3,1);
		if(RSAkeylen =='1'){
			output = input.substr(261,16);
		}else if(RSAkeylen =='2'){
			output = input.substr(517,16);
		}
		return output;
	},
	getEncryptedMessage:function(input){
		var output='';

		//Error Checking
		var version = input.substr(0,1);
		var type = input.substr(1,2);
		var tdeslen = input.substr(4,1);
		var E0011 = ErrorCheck.E0011(version);
		var totallen = input.length;

		if(E0011!=''){
			return E0011;
		}
		if(type=='22'){

		}else{
			return 'E0012';
		}
		//Error Checking
		var RSAkeylen = input.substr(3,1);
		if(RSAkeylen =='1'){
			if(tdeslen=='2'){
				var datalen = totallen-309;
				output = input.substr(309,datalen);
			}else if(tdeslen=='3'){
				var datalen = totallen-325;
				output = input.substr(325,datalen);
			}
		}else if(RSAkeylen =='2'){
			if(tdeslen=='2'){
				var datalen = totallen-565;
				output = input.substr(565,datalen);
			}else if(tdeslen=='3'){
				var datalen = totallen-581;
				output = input.substr(581,datalen);
			}
		}
		return output;
	},
	getVersion:function(){
		return '1.2';
	}
}
