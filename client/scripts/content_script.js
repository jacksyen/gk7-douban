var TYPE = {
    article: 'article',
    gallery: 'gallery'
};

chrome.runtime.onMessage.addListener(function(request, sender, sendRequest){
    var html = $('.gk7-douban-result-msg');
    // 开始处理数据
    if(request.status == 'BEGIN'){
	if (html.length>0){
	    html.find('.content').html('该文章正在推送处理中，请勿重复推送...');
	    return;
	}
	html = $('<div />').addClass('gk7-douban-result-msg');
        var close = $('<div />').addClass('close').click(function (){
            html.remove();
        }).html('关闭');
        var content = $('<div/>').addClass('content').html("正在获取文章信息，请稍候...");
	$('body').append(html.append(close).append(content));

	// 获取文章数据
	getArticleInfo(sendRequest);
	// 异步调用返回true
	return true;
    } 
    // 重试
    else if(request.status == 'TRY'){
	$('.gk7-douban-result-msg').find('.content').html(result.msg);
    }
    // 处理状态码['FAIL', 'SUCCESS', 'ABNORMAL']
    else {
	showResultMsg(request, true)
    }
});

/**
 * 显示结果信息
 * @param result 内容
 * @param hidden [true/false]
 */
function showResultMsg(result, hidden){
    var html = $('.gk7-douban-result-msg');
    html.find('.content').html(result.msg);
    if (hidden != false) {
	html.fadeTo(5000, 0.50, function (){
	    html.remove();
	});
    }
}

/**
   获取文章数据
**/
function getArticleInfo(callback){
    var article = $(".article");
    if(article.length!=1){
	showResultMsg({
	    'msg': '获取文章信息失败，请稍候再试，或联系：hyqiu.syen@gmail.com'
	}, true);
	return;
    }
    // 获取数据
    fetch_book_data(getBookId(), function (book_data){
	var data = book_data.data;
	if (!data) {
	    // 获取文章数据失败
	    showResultMsg({
		'msg': '解析图书数据失败，请稍候再试，或联系：hyqiu.syen@gmail.com'
	    }, true);
	    return;
	}
	data = data.replace(/\n/g, '');
	// 处理推送
	showResultMsg({
	    'msg': '正在推送中，请稍候...'
	}, false);
	callback({
	    title : book_data.title,
	    bookData: data,
	    ebookId: getRequestBookId(),
	    status: 'SUCCESS',
	    sendType: book_data.type || getSendType(), // article, column, gallery
	});	
    });
}

/**
 * 获取推送类型
 * 'article': 文章
 * 'column' : 专栏
 **/
function getSendType(){
    if(location.href.match(/ebook\/(\d+)\//)){
	return 'article';
    }
    if(location.href.match(/column\/(\d+)\//)){
	return 'column';
    }
    return undefined;
}

/**
 * 获取推送时的书籍ID
 **/
function getRequestBookId(){
    var matches = location.href.match(/ebook\/(\d+)\//);
    if (!matches) {
	matches = location.href.match(/column\/(\d+)\//);
    }
    return matches[1];
}

/**
 * 获取书籍ID
 **/
function getBookId(){
    var matches = location.href.match(/ebook\/(\d+)\//);
    if (!matches) {
	matches = location.href.match(/chapter\/(\d+)\//);
    }
    return matches[1];
}

//fetch book信息，调用callback
function fetch_book_data(book_id, callback) {
    var post_data = {
	ck: $.cookie('ck'),
	aid: book_id,
	reader_data_version: localStorage.readerDataVersion || 'v8'
    };
    var url = 'http://read.douban.com/j/article_v2/get_reader_data';
    $.ajax({
        url: url,
        data: post_data,
        dataType: 'json',
        type: 'POST',
        success: function (data){
	    if (!data.title || data.title == undefined) {
		$('.gk7-douban-result-msg').find('.content').html('第一次获取文章信息失败，正在更换连接...');
		tryGetReadData(book_id, callback);
		return;
	    }
            call_result(data, TYPE.article, callback);
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
	    $('.gk7-douban-result-msg').find('.content').html('第一次获取文章信息失败，正在更换连接...');
            // 重新换链接抓取文章数据
            tryGetReadData(book_id, callback);
        }
    });
}


/**
  * 获取数据成功返回数据
  * data: 返回数据
  * callback: 回调函数
  */
function call_result(data, type, callback){
    var book_data = {};
    switch (type){
    case TYPE.article:
	book_data['title'] = data.title;
	book_data['data'] = data.data;
	book_data['price'] = data.price;
	break;
    case TYPE.gallery:
	book_data['title'] = data.meta.title;
	book_data['price'] = data.meta.price;
	book_data['data'] = data.data;
	book_data['type'] = 'gallery';
	break;
    }
    callback(book_data);
}

/**
  * 重新获取文章数据
  * book_id: 文章ID
  * callback: 回调函数
  */
function tryGetReadData(book_id, callback){
    // 更换抓取数据链接
    $.ajax({
        url: 'http://read.douban.com/j/article_v2/gallery/get_reader_data',
        data: {
            works_id: book_id,
            reader_data_version: localStorage.readerDataVersion || 'v8'
        },
        dataType: 'json',
        type: 'POST',
        async: false,
        headers: {'X-CSRF-Token': $.cookie('ck')},
        success: function (data){
            call_result(data, TYPE.gallery, callback);
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
	    $('.gk7-douban-result-msg').find('.content').html('获取文章信息失败，请稍候再试，或联系：hyqiu.syen@gmail.com');
        }
    });
}
