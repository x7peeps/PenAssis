/ 生成随机姓名

function getName(){
var familyNames = new Array(
"赵", "钱", "孙", "李", "周", "吴", "郑", "王", "冯", "陈", 
"褚", "卫", "蒋", "沈", "韩", "杨", "朱", "秦", "尤", "许",
"何", "吕", "施", "张", "孔", "曹", "严", "华", "金", "魏", 
"陶", "姜", "戚", "谢", "邹", "喻", "柏", "水", "窦", "章",
"云", "苏", "潘", "葛", "奚", "范", "彭", "郎", "鲁", "韦", 
"昌", "马", "苗", "凤", "花", "方", "俞", "任", "袁", "柳",
"酆", "鲍", "史", "唐", "费", "廉", "岑", "薛", "雷", "贺", 
"倪", "汤", "滕", "殷", "罗", "毕", "郝", "邬", "安", "常",
"乐", "于", "时", "傅", "皮", "卞", "齐", "康", "伍", "余", 
"元", "卜", "顾", "孟", "平", "黄", "和", "穆", "萧", "尹"
);
var givenNames = new Array(
"子璇", "淼", "国栋", "夫子", "瑞堂", "甜", "敏", "尚", "国贤", "贺祥", "晨涛", 
"昊轩", "易轩", "益辰", "益帆", "益冉", "瑾春", "瑾昆", "春齐", "杨", "文昊", 
"东东", "雄霖", "浩晨", "熙涵", "溶溶", "冰枫", "欣欣", "宜豪", "欣慧", "建政", 
"美欣", "淑慧", "文轩", "文杰", "欣源", "忠林", "榕润", "欣汝", "慧嘉", "新建", 
"建林", "亦菲", "林", "冰洁", "佳欣", "涵涵", "禹辰", "淳美", "泽惠", "伟洋", 
"涵越", "润丽", "翔", "淑华", "晶莹", "凌晶", "苒溪", "雨涵", "嘉怡", "佳毅", 
"子辰", "佳琪", "紫轩", "瑞辰", "昕蕊", "萌", "明远", "欣宜", "泽远", "欣怡", 
"佳怡", "佳惠", "晨茜", "晨璐", "运昊", "汝鑫", "淑君", "晶滢", "润莎", "榕汕", 
"佳钰", "佳玉", "晓庆", "一鸣", "语晨", "添池", "添昊", "雨泽", "雅晗", "雅涵", 
"清妍", "诗悦", "嘉乐", "晨涵", "天赫", "玥傲", "佳昊", "天昊", "萌萌", "若萌"
);
var i = parseInt( * Math.random())* + parseInt( * Math.random());
var familyName = familyNames[i];
var j = parseInt( * Math.random())* + parseInt( * Math.random());
var givenName = givenNames[i];
var name = familyName + givenName;
var x = document.getElementsByName("client_name");
for (var i = ; i < x.length; i++) {
var o = x[i];
o.value = name;
}
} 
//生成随机手机号

function getMoble() {
var prefixArray = new Array("130", "131", "132", "133", "135", "137", "138", "170", "187", "189");
var i = parseInt(10 * Math.random());
var prefix = prefixArray[i];
for (var j = 0; j < 8; j++) {
prefix = prefix + Math.floor(Math.random() * 10);
}
var x = document.getElementsByName("mobile_tel");
for (var i = 0; i < x.length; i++) {
var o = x[i];
o.value = prefix;
}
}
// 生成随机身份证号

function getId_no(){
var coefficientArray = [ "7","9","10","5","8","4","2","1","6","3","7","9","10","5","8","4","2"];// 加权因子
var lastNumberArray = [ "1","0","X","9","8","7","6","5","4","3","2"];// 校验码
var address = "420101"; // 住址
var birthday = "19810101"; // 生日
var s = Math.floor(Math.random()*10).toString() + Math.floor(Math.random()*10).toString() + Math.floor(Math.random()*10).toString();
var array = (address + birthday + s).split(""); 
var total = 0;
for(i in array){
total = total + parseInt(array[i])*parseInt(coefficientArray[i]);
} 
var lastNumber = lastNumberArray[parseInt(total%11)];
var id_no_String = address + birthday + s + lastNumber;
var x = document.getElementsByName("id_no");
for (var i = 0; i < x.length; i++) {
var o = x[i];
o.value = id_no_String;
}
} 
//生成随机银行卡号

function getBank_account() {
var bank_no = document.getElementById("bank_no_select").value; 
var prefix = "";
switch (bank_no) {
case "0102":
prefix = "622202";
break;
case "0103":
prefix = "622848";
break;
case "0105":
prefix = "622700";
break;
case "0301":
prefix = "622262";
break; 
case "104":
prefix = "621661";
break; 
case "0303":
prefix = "622666";
break;
case "305":
prefix = "622622";
break;
case "0306":
prefix = "622556";
break;
case "0308":
prefix = "622588";
break;
case "0410":
prefix = "622155";
break;
case "302":
prefix = "622689";
break;
case "304":
prefix = "622630";
break;
case "309":
prefix = "622908";
break;
case "310":
prefix = "621717";
break;
case "315":
prefix = "622323";
break;
case "316":
prefix = "622309";
break; 
default:
}
for (var j = 0; j < 13; j++) {
prefix = prefix + Math.floor(Math.random() * 10);
}
var x = document.getElementsByName("bank_no");
for (var i = 0; i < x.length; i++) {
var o = x[i];
o.value = bank_no;
}
var y = document.getElementsByName("bank_account");
for (var i = 0; i < y.length; i++) {
var o = y[i];
o.value = prefix;
}
}