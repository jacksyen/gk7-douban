paceOptions = {
    ajax: false, // disabled
    document: false, // disabled
    eventLag: false, // disabled
    elements: {
        selectors: ['.gk7-douban-send-end']
    }
};
document.addEventListener('DOMContentLoaded', function () {
    
    chrome.extension.sendMessage('id',{'sa':'12312'}, function (response){
	
    });
});

function showHistory(msg){
    var div = $('<div />').addClass('title center large gray');
    if (!msg){
	div.append('您还没有推送任何书籍，点击这里开始：<br/>');
    } else {
	div.append(msg);
    }
    if (!msg){
	var a = $('<a />').attr({
	    'href': 'https://read.douban.com',
	    'target': '_blank'
	}).html('https://read.douban.com');
	div.append(a);
    }
    return div[0];
}

$(document).ready(function (){
    // 初始化加载推送的书籍
    var historyDiv = $('div[data-tab="history"]').find('.list');
    historyDiv.html(showHistory('加载中...'));
    $.ajax({
	//url: 'http://gk7.pw:8000/history',
	//url: 'http://112.124.38.237:8000/history',
        url: 'http://localhost:8000/history',
        //url: 'http://192.168.1.108:8000/history',
	data: {
	    'userId': localStorage.GK7_USER_ID
	},
	method: 'POST',
	dataType: 'json',
	success: function (data){

	    if (data.status == 'WRAN') {
		historyDiv.html(showHistory('请求失败，请联系hyqiu.syen@gmail.com'));
		return;
	    }
	    if (data.status == 'SUCCESS') {
		if (data.code == 'NONE') {
		    historyDiv.html(showHistory());
		    return;
		}
		// success
		//data.data
		var html = $('<div />');
		$(data.data).each(function (){
		    var item = $('<div />').addClass('item');
		    var content = $('<div />').addClass('right floated content');
		    var email_status = this.email_send_status;
		    var status = $('<a />').addClass('ui label');
		    if (email_status == 'wait') {
			status.addClass('blue').html('推送中');
		    } else if (email_status == 'complete') {
			status.addClass('green').html('推送成功');
		    } else if (email_status == 'error') {
			status.addClass('red').html('推送失败');
		    } else {
			status.addClass('red').html('未知状态');
		    }
		    status.appendTo(content);
		    var title = $('<div />').addClass('title');
		    var tc = $('<a />').html(this.email_title).appendTo(title);
		    item.append(content).append(title);
		    html.append(item);
		});
		historyDiv.html(html.html());
		return;
	    }
	    // 异常
	    showHistory(data.msg);
	},
	error: function (){
	    showHistory('请求异常，请联系hyqiu.syen@gmail.com');
	}
    });

    // 生成私有ID
    initUserId();    

    // 菜单项点击事件
    $('.menu .item').click(function (){
	toggleItem($(this));
    });
    
    // 点击设置按钮事件
    $('#btnSetting').click(function (){
	showMenu('setting');
    });
    
    // 点击捐助菜单加载图片
    $('a[data-tab="offer"]').click(function (){
	var img = $('#offerImg');
	if (!img.attr('src')){
	    img.attr('src','https://coding.net/u/jacksyen/p/open/git/raw/master/images/donation.png');
	}
    });
    
    // 初始化加载kindle邮箱
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

    // 保存邮箱按钮事件
    $('#btn-save').click(function (){
	var email = $('#userEmail').val() + '@' + $('#emailDomain').val();
	var privateEmail = $('#privateEmail');
	if(!validateEmail(email)){
	    showMsg('kindle邮箱格式不正确，请检查');
	    localStorage.TO_MAIL = '';
	    return;
	}
	localStorage.TO_MAIL = email;
	// 生成私有ID
	localStorage.GK7_USER_ID = new Date().getTime() + '_' + localStorage.TO_MAIL;

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

function initUserId(){
    // 生成私有ID
    var userId = localStorage.GK7_USER_ID;
    if (!userId){
	localStorage.GK7_USER_ID = new Date().getTime() + '_' + localStorage.TO_MAIL;
    }
}

function toggleItem(self){
    if (self.hasClass('active')){
	return;
    }
    $('.menu').find('.item').each(function (){
	$(this).removeClass('active');
    });
    self.addClass('active');
    var tab = $('div').find('div[data-tab="' + self.attr('data-tab') + '"]');
    $('.tab').css('display', 'none');
    tab.css('display', 'block');
}

/**
 * 显示某一菜单
 * @param item
 */
function showMenu(item) {
    var self = $('.menu').find('a[data-tab="' + item + '"]');
    toggleItem(self);
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