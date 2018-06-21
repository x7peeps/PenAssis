<script>
$(document).ready(function(){
  $("#b01").click(function(){//比如再按钮的单击事件中
  htmlobj=$.ajax({url:"/jquery/test1.txt",async:false});//通过ajax读取test1.txt文本文件。
  $("#myDiv").html(htmlobj.responseText.replace(/.+/g,'</br>'));//根据回车换行符进行替换，替换成html换行符
  });
});
</script>
<div id='myDiv'></div>
<input type='button' id='b01' value='读取文本'/>
