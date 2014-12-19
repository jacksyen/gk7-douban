function checkForValidUrl(tabId, changeInfo, tab) {
    var regex = /.*\:\/\/read.douban.com\/reader\/ebook\/([^\/]*).*/;
    if (changeInfo.status == 'complete') {
	if (regex.test(tab.url)) {
	    chrome.pageAction.show(tabId);
	}
	
    }
};

chrome.tabs.onUpdated.addListener(checkForValidUrl);

chrome.pageAction.onClicked.addListener(function(tab) {
    if(!localStorage.TO_MAIL){
	chrome.tabs.create({ url: 'options.html' });
	return;
    }
    //var request_id = new Date().getTime();
    chrome.tabs.sendMessage(tab.id, {status: 'BEGIN', msg: '文章较长,处理时间大约一分钟左右,请稍候..'}, function(response) {
        // 发送数据
	send(response, function(data) {
	    sendResultMessage(tab.id, data);
	});
    });

});

/**
   发送结果信息
**/
function sendResultMessage(tabId, data){
    chrome.tabs.sendMessage(tabId, data, function (response){
	
    });

}

function set_icon(tab_id, icon) {
    chrome.pageAction.setIcon({
	tabId: tab_id,
	path: 'images/' + icon
    });
}


/**
   推送请求
**/
function send(request, callback){
    var articleData = {};
    var splitData = request.bookData.split(':');
    var book_data = splitData[1].replace(/\n/g, '');
    articleData['bookData'] = book_data;
    articleData['bookTitle'] = splitData[0];
    articleData['toMail'] = localStorage.TO_MAIL;
    articleData['requestId'] = request.requestId;
    $.ajax({
	//url: 'http://gk7.pw:8000/send',
        //url: 'http://localhost:8000/send',
        url: 'http://192.168.3.167:8000/send',
	data: articleData,
	dataType: 'json',
	type: 'POST',
	timeout: 60*1000// 60秒超时
    }).done(function(response){
	callback(response);
    }).fail(function(){
	callback({status:'FAIL', msg:'推送请求失败，请稍候再试，或联系：<a href="mailto:hyqiu.syen@gmail.com">hyqiu.syen@gmail.com</a>'});
    });
}
