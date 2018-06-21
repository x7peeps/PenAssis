/******************************************************
//*功能描述:生成与JUMP平台一致的数据字典校验
//*Author:lanxb
//公开方法：
//      addForm(name,data)
//      verify(name,values)
//      length(str)
//      parseDate(regxDate) 将JUMP平台数据校验中日期数据格式化为YYYYMMDD
***************************************************** */ 
var Validation=(function(){
		var forms={};
		var alwaysCheck={};
		var charlen=2;
		var errorTip=function(item,e,alwaysAlert){
			var isAlert=true;
			if(item && item.source){
				$(item.source).each(function(index,item){
					if(item.is(":visible")){
						item.attr("title",e.message).tooltip(Util.tooltip).tooltip("close");
						//item.mouseover();
						//isAlert=false;
					}
				});
			}
			if(isAlert || alwaysAlert){
				Util.error(e.message);
				e.isAlert=true;
			}
			throw e;
		}
		return {
			setFormField:function(formName,name,label,optional,rules,safe,args,source){
				var form = forms[formName]?forms[formName]:{};
				var newRule = [];
				form[name]={
						name:label,optional:optional,
						source:source?source:[],
						validate:function(val){
							for(var i=0;i<this.rules.length;i++){
								this.rules[i].validate(val);
							}
						},
						safe:safe==true
				}
				if(rules && rules.length>0){
					for(var i=0;i<rules.length;i++){
						newRule[i]=Validation.rules[rules[i]].call(form[name],args);
					}
				}
				form[name].rules=newRule;
				forms[name]=form;
				var scope=this;
				$(function(){
						var items =$("[validation^='"+name+"']");
						items.each(function(index,item){
							scope.bind(item);
						});
				});
			},
			setAlwaysCheck:function(formName,fieldName,valueFunction){
				var form = alwaysCheck[formName]?alwaysCheck[formName]:{};
				form[fieldName]=valueFunction;
				alwaysCheck[formName]=form;
			},
			addForm:function(name,data){
				var form=forms[name]?forms[name]:{};
				for(var key in data){
					var field=data[key];
					var objs={name:field.name,optional:field.optional,rules:[],source:[],validate:function(val){
						for(var i=0;i<this.rules.length;i++){
							this.rules[i].validate(val);
						}
					}};
					if(field.safe==true){
						objs.rules[objs.rules.length]=Validation.rules["safeinput"].call(objs,key);
						objs.safe=true;
					}else{
						if(field.optional==false){
							objs.rules[objs.rules.length]=Validation.rules["not-empty"].call(objs,null);
						}
						
						if(field.values ){
							objs.rules[objs.rules.length]=Validation.rules["values"].call(objs,field.values);
						}else if(field.rules){
							var rules=field.rules;
							for(var i=0;i<rules.length;i++){
								var rule=rules[i];
								if(Validation.rules[rule.type]){
									objs.rules[objs.rules.length]=Validation.rules[rule.type].call(objs,rule.args);
								}else{
									alert("rule["+rule.type+"] not defined");
								};
							}
						}
					}
					form[key]=objs;
				}
				forms[name]=form;
				var scope=this;
				$(function(){
						var items =$("[validation^='"+name+"']");
						items.each(function(index,item){
							scope.bind(item);
						});
				});
			},
			setItemSource:function(form,field,obj){
				var source=forms[form][field].source;
				source[source.length]=obj;
			},
			getValue:function(item){
				return Util.val(item);
			},
			/**
			 * 为表单元素绑定校验事件
			 * @param name 表单名称
			 * @param values 验证数据集合
			 * @param callBack 验证通过后的回调方法
			 */
			bind:function(item,form,field){
				var _item=$(item);
				var scope=this;
				//增加错误提示
				var validationCallBack=function(e){
					var name=e.data[0];
					var field=e.data[1];
					if(name && field && forms[name][field]){
						var _this=$(this);
						var value=scope.getValue(_this);
						_this.tooltip("close");
						var title=_this.attr("ttitle");
						if(title){
							_this.attr("title",title);
						}
						_this.removeData( "ui-tooltip-title" );
						try{
							forms[name][field].validate(value);
						}catch(e){
							if(_this.is(":visible")){
								_this.attr("title",e.message).tooltip(Util.tooltip).tooltip("enable");
								_this.tooltip("open");
							}
						}
					}
				}
				if(!form || !field){
					var names=_item.attr("validation");
					var index=names.indexOf(".");
					if(index>-1){
						form=names.substr(0,index);
						field=names.substr(index+1);
					}
				}
				if(forms[form][field]){
					var source=forms[form][field].source;
					source[source.length]=_item;
					var data=[form,field];
					_item.tooltip(Util.tooltip);
					var title = _item.attr("title");
					if(title){
						_item.attr("ttitle",title);
					}
					_item.blur(data,validationCallBack);
					_item.click(function(){
						$(this).tooltip("widget").prev("iframe").hide();
						$(this).tooltip("close");
					});
				}
			},
			/**
			 * 提供表单验证方法
			 * @param name 表单名称
			 * @param values 验证数据集合
			 * @param callBack 验证通过后的回调方法
			 * @returns void
			 */
			verify:function(name,values,callBack,failedCallBack){
				var form=forms[name];
				var item = null;
				var mustChk = alwaysCheck[name]?alwaysCheck[name]:{};
				try{
						for(var chk in mustChk){
							var valueHandler = mustChk[chk];
							if(valueHandler && $.isFunction(valueHandler)){
								values[chk]=valueHandler.call();
							}
						}
						for(var key in values){
							item =form[key];
							if(!item||(item.optional==true&&(!Validation.hasText(values[key])))){
								//可选且没值时不校验
								continue;
							}else{
								item.validate(values[key]);
							}
						}
						if(callBack)
						{
							callBack();
						}
				}catch(e){
					var autoTip=true;
					if(failedCallBack){
						autoTip=failedCallBack(e);
					}
					if(autoTip!=false){
						errorTip(item,e);
					}
				}
			},
			/**
			 * 输入并提交一个表单
			 * @param name 表单名称
			 * @param values 验证数据集合
			 * @param callBack 验证通过后的回调方法
			 * @returns
			 */
			submit:function(name,values,callBack){
				var form=forms[name];
				var submitForm=document.forms[name];
				var safe={};
				var hasSafe=false;
				var item = null;
				var mustChk = alwaysCheck[name]?alwaysCheck[name]:{};
				try{
					for(var chk in mustChk){
						var valueHandler = mustChk[chk];
						if(valueHandler && $.isFunction(valueHandler)){
							values[chk]=valueHandler.call();
						}else{
							values[chk]=null;
						}
					}
					for(var key in values){
						if(!submitForm[key])
							continue;//form中没有，忽略
						item =form[key];
						if(!item || (item.optional==true&&(!Validation.hasText(values[key])))){
							//可选且没值时不校验
							if(Validation.hasText(values[key])){
								submitForm[key].value=values[key];
							}
							continue;
						}else{
							item.validate(values[key]);
							if(item.safe==true){
								hasSafe=true;
								Validation.rules.safeinput(key);
								safe[key]=values[key];
							}else{
								if(submitForm[key]==undefined){
									alert("页面中"+key+"未定义！");
								}
								if(values[key]!=null&&values[key]!=undefined){
									submitForm[key].value=values[key];
								}
							}
						}
					}
					var autoSubmit=true;
					if(callBack){
						autoSubmit=callBack(submitForm,safe);
					}
					if(autoSubmit!=false){
						if(hasSafe){
							submitSafeControl(safe,name);
						}else{
							try{
								var tURL = submitForm.action+"";
								if(!submitForm.target && tURL.indexOf(".do")>-1){
									$(window.lastBaseClkBtn).attr("disabled",true).parent().addClass("gray");
									parent.parent.parent.parent.Util.cache.lastButtonId=$(window.lastBaseClkBtn).attr("id");
								}
							}catch(e){
								
							}
							if(submitForm){
								submitForm.submit();
							}
							
						}
					}
				}catch(e){
					errorTip(item,e,true);
				}
			},
			length:function(val){
				var rExp = RegExp(/[^\x00-\xff]/);
				var count = 0;
				for(var i=0;i<val.length;i++)
				{
					if(rExp.test(val.charAt(i))){count +=charlen;}else{count++;};
				};
				return count;
			},
			hasText:function(val){
				return val != undefined && val !=null && val!="";
			},
			/**
			 * 对输入的日期规则,进行转换成目标日期,并进行对应格式处理
			 * @param rule 转换日期规则 使用Validation.parseDate处理rule,获得Date
			 * @param destFormat 要转换的日期格式:yymmdd,yy-mm-dd等,不传则使用yymmdd;关于日期格式请参考$.datepicker
			 * @returns 格式化后的日期
			 */
			getFormatDate:function(rule,destFormat){
				var _date=this.parseDate(rule);
				var _destFormat='yymmdd';
				if(destFormat){
					_destFormat=destFormat;
				}
				return $.datepicker.formatDate(_destFormat,_date);
			},
			/**
			 * 处理JUMP平台数据字典的DATE类型规则的转换<br>
			 * 目前支持到加减到毫秒及偏移到秒的精确度，不支持星期配置<br>
			 * 支持绝对时间配置yyyyMMdd及yyyy-MM-dd及yyyy-MM-dd HH:mm:ss,yyyy-MM-dd HH:mm:ss.SSS,示例： <after date="2009-11-11"/><br>
			 * 支持相对加减时间配置：T[+/-n]S,T[+/-n]s,T[+/-n]m,T[+/-n]H,T[+/-n]d,T[+/-n]M,T[+/-n]y,示例： <after date="T+1y-2M-34d"/>,当前时间加1年减2月减34天<br>
			 * 支持相对偏移时间配置：T[>/<]s,T[>/<]m,T[>/<]H,T[>/<]d,T[>/<]M,T[>/<]y,示例：<after date="T&gt;d"/>,下一天开始时间,注意>要转义为&gt;<br>
			 * 支持以上三种混合配置：其顺序为：绝对＋偏移＋加减，示例：<after date="2009-11-11&gt;y+2M"/><br>
			 * @param str 待转换的字符串
			 * @returns 处理后的date
			 */
			parseDate:function(str){
				var date=null;//要返回的时间
				var flag=true;//date是否为null
				var i=0;//要截取字符串的开始下标
				if(!str&&($.trim(str)).length==0){
					throw new Error("Date string should not be null or blank!");
				}
				//循环处理str
				for(var _str=str;_str.length>0;){
					var _date=null;//每次循环返回的时间
					//循环匹配pattern
					for(var key in Validation.patterns){
						if(new RegExp(key).test(_str)){
							//匹配后进行处理
							if(!date){
								date=Util.getServerDate();//new Date();//
							}
							_date=Validation.patterns[key].call(this,date,_str);
						}
					}
					if(_date!=null){
						date=_date;//赋值，不可省略
						if(flag){
							//第一次不为null
							i=_str.length;//初始化下标
						}else{
							i+=_str.length-1;//往右截取(下标增加)
						}
						_str=new Util.StringBuffer().append("T").append(str.substring(i)).toString();
						flag=false;
					}else{
						_str=_str.substring(0,_str.length-1);//往左截取（每次从最后减少一位）
					}
					if(_str=='T'){
						//退出循环
						if(i!=str.length){
							throw new Error(new Util.StringBuffer().append("Could not parse date string [").append(str).append("]!").toString());
						}
						break;
					}
				}
				if(date==null){
					throw new Error(new Util.StringBuffer().append("Could not parse date string [").append(str).append("]!").toString());
				}else{
					return date;
				}
			},
			formateStr:function(dStr){
				return dStr.substring(0,4)+"-"+dStr.substring(4,6)+"-"+dStr.substring(6,8);
			}
		};
})();
/******************************************************
//*功能描述:实现JUMP-CHECKRULE规则
//*Author:lanxb
***************************************************** */ 
Validation.rules={
		/**
		 * 安全控件验证
		 * @param id 控件ID
		 * @returns 验证实现接口
		 */
		"safeinput":function(id){
			var name=this.name;
			return {
				validate:function(msg){
					try{
						verifySafeControl(id,msg);
					}catch(e){
						if(msg){
							throw new Error(e.message);
						}else{
							throw e;
						}
					}
				}
			};
		},
		"not-empty":function(args){
			var name = this.name;
			return {
				validate:function(value){
					if(!Validation.hasText(value)){
					
						throw new Error(Util.getMessage(Util.Message.rule.notempty,[name]));
					};
				}
			};
		},
		"values":function(args){
			var name = this.name;
			return {
				validate:function(value){
					if(!Validation.hasText(value)){
						return;
					}
					if(args[value]==undefined){
						var data=new Array();
						for(var key in args){
							data[data.length]=args[key];
						}						
						
						throw new Error(Util.getMessage(Util.Message.rule.values,[name,data.join(",")]));
					}
				}
			   
			};
		},
		"min-length":function(args){
			var length=args[0];
			var name = this.name;
			return {
				validate:function(value){
					if(!Validation.hasText(value)){
						return;
					}
					if(Validation.length(value)<length){
						throw new Error(Util.getMessage(Util.Message.rule.minLength,[name,length]));
					};
				}
			};
		},
		"max-length":function(args){
			var length=args[0];
			var name = this.name;
			return {
				validate:function(value){
					if(!Validation.hasText(value)){
						return;
					}
					if(Validation.length(value)>length){
						throw new Error(Util.getMessage(Util.Message.rule.maxLength,[name,length]));
					};
				}
			};
		},
		"length":function(args){
			var minLength=args[0];
			var maxLength=args[1];
			var name = this.name;
			return {
				validate:function(value){
					var len = Validation.length(value);
					var mlen = value.length;
					if(!Validation.hasText(value)){
						return;
					}
					if(minLength==maxLength){
						if(len!=minLength){
							throw new Error(Util.getMessage(Util.Message.rule.length,[name,minLength]));
						}
					}else if(mlen<minLength){
						throw new Error(Util.getMessage(Util.Message.rule.minLength,[name,minLength]));
					}else if(len>maxLength){
						throw new Error(Util.getMessage(Util.Message.rule.maxLength,[name,maxLength]));
					}					
				}
			};
		},
		/**Edit by HAVEN in 2013-07-23**/
		"regex":function(args){
			var patrn=args[0].replace(/\\\\/g,"\\");
			var rExp = new RegExp(patrn);
			var name = this.name;
			return {
				validate:function(value){	
					if(!Validation.hasText(value)){
						return;
					}
					if(!rExp.test(value)){
						throw new Error(Util.getMessage(Util.Message.rule.regex,[name]));
					}
				}			
			};
		},
		"not-null":function(args){
			return {
				validate:function(value){				
				}
			};
		},	
		"not-blank":function(args){
			var name = this.name;
			return {
				validate:function(value){	
					if(value.match(/^[\s| ]*$/)){
						throw new Error(Util.getMessage(Util.Message.rule.notblank,[name]));
					}
				}			
			};
		},
		"min-size":function(args){
			var minsize=args[0];
			var name = this.name;
			return {
				validate:function(value){	
					if(!Validation.hasText(value)){
						return;
					}
					if(value.length<minsize){
						throw new Error(Util.getMessage(Util.Message.rule.minsize,[name,minsize]));
					}
				}			
			};
		},
		"max-size":function(args){
			var maxsize=args[0];
			var name = this.name;
			return {
				validate:function(value){	
					if(!Validation.hasText(value)){
						return;
					}
					if(value.length>maxsize){
						throw new Error(Util.getMessage(Util.Message.rule.maxsize,[name,maxsize]));
					}
				}			
			};
		},
		"size":function(args){
			var minsize=args[0];
			var maxsize= args[1];
			return {
				validate:function(value){	
					if(!Validation.hasText(value)){
						return;
					}
					var size=value.length;
					if(size<minsize||size>maxsize){				
						throw new Error(Util.getMessage(Util.Message.rule.size,[name,minsize,maxsize]));
					}
				}			
			};
		},
		"min":function(args){
			var min=args[0];
			var name = this.name;
			return {
				validate:function(value){	
					if(!Validation.hasText(value)){
						return;
					}
					if(value<min){
						throw new Error(Util.getMessage(Util.Message.rule.min,[name,min]));
					}
				}			
			};
		},
		"max":function(args){
			var max=args[0];
			var name = this.name;
			return {
				validate:function(value){	
					if(!Validation.hasText(value)){
						return;
					}
					if(value>max){
						throw new Error(Util.getMessage(Util.Message.rule.max,[name,max]));
					}
				}			
			};
		},
		"range":function(args){
			var min=args[0];
			var max= args[1];
			var name = this.name;
			return {
				validate:function(value){	
					if(!Validation.hasText(value)){
						return;
					}
					value = value - 0;
				/*	if(value<min||value>max){
						throw new Error(Util.getMessage(Util.Message.rule.range,[name,min,max]));
					}else */
					if(value < min){
						throw new Error(Util.getMessage(Util.Message.rule.rangeMax,[name,min]));
					}else if(value > max){
						throw new Error(Util.getMessage(Util.Message.rule.rangeMin,[name,max]));
					}
				}			
			};
		},
		/**
		 *校验输入日期是否小于终止日期,配置方式：<before date="T+1M"/>
		 * @param args
		 * @returns {___anonymous12378_12591}
		 */
		"before":function(args){
			var before=args[0];
			var name = this.name;
			return {
				validate:function(value){
					if(!Validation.hasText(value)){
						return;
					}
					before=Validation.getFormatDate(before);
					if(value>=before){
						throw new Error(Util.getMessage(Util.Message.rule.before,[name,Validation.formateStr(before)]));
					}
				}			
			};
		},
		/**
		 * 校验输入日期是否大于起始日期，配置方式：<after date="T+1M"/>
		 * @param args
		 * @returns {___anonymous12802_13013}
		 */
		"after":function(args){
			var after=args[0];
			var name = this.name;
			return {
				validate:function(value){	
					if(!Validation.hasText(value)){
						return;
					}
					after=Validation.getFormatDate(after);
					if(value<=after){
						throw new Error(Util.getMessage(Util.Message.rule.after,[name,Validation.formateStr(after)]));
					}
				}			
			};
		},
		/**
		 * 校验输入日期是否在起始日期和终止日期之间（两者均包含），配置方式：<between date="[$(min),$(max)]"/>
		 * @param args
		 * @returns {___anonymous13356_13589}
		 */
		"between":function(args){
			var after=args[0];
			var before= args[1];
			var name = this.name;
			return {
				validate:function(value){	
					if(!Validation.hasText(value)){
						return;
					}
					before=Validation.getFormatDate(before);
					after=Validation.getFormatDate(after);
					if(value<after||value>before){
						throw new Error(Util.getMessage(Util.Message.rule.between,[name,Validation.formateStr(after),Validation.formateStr(before)]));
					}
				}			
			};
		}
};
/******************************************************
//*功能描述:实现JUMP-CHECKRULE规则中DATE类型转换
//*Author:wuby
***************************************************** */ 
Validation.patterns={
		/**
		 * 后台类型yyyyMMdd，绝对时间
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^\\d{8}$":function(date,str){
			return $.datepicker.parseDate('yymmdd',str);
		},
		/**
		 * 后台类型yyyy-MM-dd,绝对时间
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^\\d{4}\\-\\d{2}\\-\\d{2}$":function(date,str){
			return $.datepicker.parseDate('yy-mm-dd',str);
		},
		/**
		 * 后台类型yyyy-MM-dd HH:mm:ss,绝对时间，到秒值
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^\\d{4}\\-\\d{2}\\-\\d{2}\\s+\\d{2}:\\d{2}:\\d{2}$":function(date,str){
			var tempDate= $.datepicker.parseDate('yy-mm-dd',str);
			var _str=$.trim(str.substring(10));
			var arr=_str.split(/\:/);
			tempDate.setHours(arr[0],arr[1],arr[2]);
			return tempDate;
		},
		/**
		 * 后台类型yyyy-MM-dd HH:mm:ss.SSS,绝对时间,到毫秒值
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^\\d{4}\\-\\d{2}\\-\\d{2}\\s+\\d{2}:\\d{2}:\\d{2}\\.\\d{3}$":function(date,str){
			var tempDate= $.datepicker.parseDate('yy-mm-dd',str);
			var _str=$.trim(str.substring(10));
			var arr=_str.split(/\:|\./);
			tempDate.setHours(arr[0],arr[1],arr[2],arr[3]);
			return tempDate;
		},
		/**
		 * 后台类型T,当前时间
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^T$":function(date,str){
			//do nothing
			return date;
		},
		/**
		 * 后台类型T[+/-]S,加减毫秒
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^T[\\+\\-](\\d+)S$":function(date,str){
			var num=str.substring(1,str.length-1);
			date.setMilliseconds(date.getMilliseconds()+parseInt(num));
			return date;
		},
		/**
		 * 后台类型T[+/-]s,加减秒
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^T[\\+\\-](\\d+)s$":function(date,str){
			var num=str.substring(1,str.length-1);
			date.setSeconds(date.getSeconds()+parseInt(num));
			return date;
		},
		/**
		 * 后台类型T[+/-]m,加减分
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^T[\\+\\-](\\d+)m$":function(date,str){
			var num=str.substring(1,str.length-1);
			date.setMinutes(date.getMinutes()+parseInt(num));
			return date;
		},
		/**
		 * 后台类型T[+/-]H,加减小时
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^T[\\+\\-](\\d+)H$":function(date,str){
			var num=str.substring(1,str.length-1);
			date.setHours(date.getHours()+parseInt(num));
			return date;
		},
		/**
		 * 后台类型T[+/-]d,加减n天
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^T[\\+\\-](\\d+)d$":function(date,str){
			var num=str.substring(1,str.length-1);
			date.setDate(date.getDate()+parseInt(num));
			return date;
		},
		/**
		 * 后台类型T[+/-]M,,加减n月
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^T[\\+\\-](\\d+)M$":function(date,str){
			var num=str.substring(1,str.length-1);
			date.setMonth(date.getMonth()+parseInt(num));
			return date;
		},
		/**
		 * 后台类型T[+/-]y,加减n年
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^T[\\+\\-](\\d+)y$":function(date,str){
			var num=str.substring(1,str.length-1);
			date.setFullYear(date.getFullYear()+parseInt(num));
			return date;
		},
		/**
		 * 后台类型T>s,偏移到下一秒开始时间
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^T>s$":function(date,str){
			date.setMilliseconds(0);
			date.setSeconds(date.getSeconds()+1);
			return date;
		},
		/**
		 * 后台类型T<s,偏移到当秒开始时间
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^T<s$":function(date,str){
			date.setMilliseconds(0);
			return date;
		},
		/**
		 * 后台类型T>m,偏移到下一分开始时间
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^T>m$":function(date,str){
			date.setSeconds(0,0);
			date.setMinutes(date.getMinutes()+1);
			return date;
		},
		/**
		 * 后台类型T<m,偏移到当前分钟开始时间
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^T<m$":function(date,str){
			date.setSeconds(0,0);
			return date;
		},
		/**
		 * 后台类型T>H,偏移到下一小时开始时间
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^T>H$":function(date,str){
			date.setMinutes(0,0,0);
			date.setHours(date.getHours()+1);
			return date;
		},
		/**
		 * 后台类型T<H,偏移到当前小时开始时间
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^T<H$":function(date,str){
			date.setMinutes(0,0,0);
			return date;
		},
		/**
		 * 后台类型T>d,偏移到下一天开始时间
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^T>d$":function(date,str){
			date.setHours(0,0,0,0);
			date.setDate(date.getDate()+1);
			return date;
		},
		/**
		 * 后台类型T<d,偏移到当天开始时间
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^T<d$":function(date,str){
			date.setHours(0,0,0,0);
			return date;
		},
		/**
		 * 后台类型T>M,偏移到下一月开始时间
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^T>M$":function(date,str){
			var i=date.getMonth();
			date.setHours(0,0,0,0);
			for(;i==date.getMonth();date.setDate(date.getDate()+1));
			return date;
		},
		/**
		 * 后台类型T<M,偏移到当月开始时间
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^T<M$":function(date,str){
			var i=date.getMonth();
			date.setHours(0,0,0,0);
			for(;i==date.getMonth();date.setDate(date.getDate()-1));
			date.setDate(date.getDate()+1);
			return date;
		},
		/**
		 * 后台类型T>y,偏移到下一年开始时间
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^T>y$":function(date,str){
			var i=date.getFullYear();
			date.setDate(1);
			date.setHours(0,0,0,0);
			for(;i==date.getFullYear();date.setMonth(date.getMonth()+1));
			return date;
		},
		/**
		 * 后台类型T<y,偏移到当年开始时间
		 * @param date 处理中时间
		 * @param str　待处理字符串
		 */
		"^T<y$":function(date,str){
			var i=date.getFullYear();
			date.setDate(1);
			date.setHours(0,0,0,0);
			for(;i==date.getFullYear();date.setMonth(date.getMonth()-1));
			date.setMonth(date.getMonth()+1);
			return date;
		}
};