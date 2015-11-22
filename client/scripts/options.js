$(document).ready(function (){
    var toEmail = localStorage.TO_MAIL;
    if (toEmail){
	var temp = toEmail.split('@');
	if(temp.length > 1){
	    $('#userEmail').val(temp[0]);
	    $('#emailDomain').val(temp[1]);
	}
    }
    var privateEmail = localStorage.TO_PRIVATE_MAIL;
    if (privateEmail){
	$('#privateEmail').val(privateEmail);
    }

    function validateEmail(email) { 
	var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	return re.test(email);
    }

    function showMsg(msg) {
	$('.msg').html(msg);
	$('.msg').fadeTo(6000, 0.50, function (){
	    $('.msg').html('');
	});
    }
    
    $('#btn-save').click(function (){
	var email = $('#userEmail').val() + '@' + $('#emailDomain').val();
	var privateEmail = $('#privateEmail');
	if(!validateEmail(email)){
	    showMsg('kindle邮箱格式不正确，请检查，注意，输入框内只需要填邮箱名，后缀点击选择框选择即可。');
	    localStorage.TO_MAIL = '';
	    return;
	}
	localStorage.TO_MAIL = email;

	if (privateEmail.val()) {
	    if (!validateEmail(privateEmail.val())){
		showMsg('个人邮箱格式不正确，请检查');
		localStorage.TO_PRIVATE_MAIL = '';
		privateEmail.focus();
		return;
	    }
	}
	localStorage.TO_PRIVATE_MAIL = privateEmail.val();
	showMsg('保存成功');
    });


});
