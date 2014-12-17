$(document).ready(function (){
    var toEmail = localStorage.TO_MAIL;
    if (toEmail){
	var temp = toEmail.split('@');
	if(temp.length > 1){
	    $('#userEmail').val(temp[0]);
	    $('#emailDomain').val(temp[1]);
	}
    }
    
    $('#btn-save').click(function (){
	localStorage.TO_MAIL = $('#userEmail').val() + '@' + $('#emailDomain').val();
	$('.msg').html('保存成功');
	$('.msg').fadeTo(3000, 0.50, function (){
	    $('.msg').html('');
	});
    });
});
