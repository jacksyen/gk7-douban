$(document).ready(function (){
    var toEmail = localStorage.TO_MAIL;
    if (toEmail){
	var temp = toEmail.split('@');
	if(temp.length > 1){
	    $('#userEmail').val(temp[0]);
	    $('#emailDomain').val(temp[1]);
	}
    }

    function validateEmail(email) { 
	var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	return re.test(email);
    }
    
    $('#btn-save').click(function (){
	var email = $('#userEmail').val() + '@' + $('#emailDomain').val();
	var msg = '保存成功';
	if(validateEmail(email)){
	    localStorage.TO_MAIL = email;
	}else{
	    msg = '邮箱格式不正确，请检查，注意，输入框内只需要填邮箱名，后缀点击选择框选择即可。'
	    localStorage.TO_MAIL = '';
	}
	$('.msg').html(msg);
	$('.msg').fadeTo(5000, 0.50, function (){
	    $('.msg').html('');
	});
    });


});
