chrome.runtime.onMessage.addListener(function(request, sender, sendRequest){
    var html = $('.gk7-douban-result-msg');
    // 开始处理数据
    if(request.status == 'BEGIN'){
        // 添加等待进度条
        if(html.length == 0){
            html = $('<div />').addClass('gk7-douban-result-msg');
            var close = $('<div />').addClass('close').click(function (){
                $('.gk7-douban-result-msg').remove();
            }).html('关闭');
            var content = $('<div/>').addClass('content').attr('content','').html(request.msg);
	    //var loading = $('<iframe/>').attr('id','gk7-douban-send');
            $('body').append(html.append(close).append(content));//.append(loading));
            html.hide().appendTo('body').fadeIn(1000);
            // 添加关闭事件
            $(window).on('popstate', function() {
                html.remove();
            });
        };
        /**content = '<html><head><meta http-equiv="Content-Type" content="text/html;charset=gb2312"/><link rel="stylesheet" href="https://coding.net/u/jacksyen/p/open/git/raw/master/styles/pace-theme-loading-bar.css"/><style>body{background-color:#f5f5f5;}</style><script>paceOptions={ajax:false,document:false,eventLag:false,elements:{selectors:[".end"]}};</script><script src="https://coding.net/u/jacksyen/p/open/git/raw/master/scripts/pace.min.js"></script></head><body></body></html>';
           frames["gk7-douban-send"].contentWindow.document.open();
           frames["gk7-douban-send"].contentWindow.document.write(content);
           frames["gk7-douban-send"].contentWindow.document.close();**/
        // 获取文章数据
        getArticleInfo(sendRequest);
        return;
    }
    showResultMsg(request);
});

/**
 * 显示结果信息
 */
function showResultMsg(result){
    var html = $('.gk7-douban-result-msg');
    // 服务器返回结果处理
    //$(frames["gk7-douban-send"].contentWindow.document).find('body').append($('<div />').addClass('end'));
    // 删除iframe进度条
    //frames["gk7-douban-send"].remove();
    html.find('.content').html(result.msg);//.css('margin', '20px');
    $('.gk7-douban-result-msg').fadeTo(4000, 0.50, function (){
	html.remove();
    });
}

/**
   获取文章数据
**/
function getArticleInfo(callback){
    var article = $(".article");
    var result = {};
    if(article.length!=1){
	result['msg'] = '获取文章信息失败，请稍候再试，或联系：hyqiu.syen@gmail.com';
	result['status'] = 'FAIL';
	showResultMsg(result);
	return;
    }
    // 获取数据
    fetch_book_data(getBookId(), function (book_data){
	result = {
	    title : document.title,
	    //postDate : postInfo.find("#post-date").text(),
	    //author : postInfo.find("a").first().text(),
	    bookData: book_data,
	    status: 'SUCCESS'
	};
	callback(result);
    });
}

function getBookId(){
    var matches = location.href.match(/ebook\/(\d+)\//);
    return matches[1];
}

//fetch book信息，调用callback
function fetch_book_data(book_id, callback) {
    if(('e'+book_id) in localStorage){
	var book_data = localStorage['e' + book_id];
        if(book_data == undefined){
            getReadData(book_id, callback);
            return;
        }
	callback(book_data);
    }else{
	getReadData(book_id, callback);
    }
}

function getReadData(book_id, callback){
    var post_data = {
	ck: $.cookie('ck'),
	aid: book_id,
	reader_data_version: 'v8'
    };
    var url = 'http://read.douban.com/j/article_v2/get_reader_data';
    $.ajax({
        url: url,
        data: post_data,
        dataType: 'json',
        type: 'POST',
        async: false,
        success: function (data){
            var book_data = [
	        data.title,
	        data.data,
	        data.purchase_time,
	        data.is_sample,
	        data.is_gift,
	        data.has_formula,
	        data.has_added,
	        data.price
	    ];
	    callback(book_data.join(':'));
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            var result = {};
	    result['msg'] = '获取文章信息失败，请稍候再试，或联系：hyqiu.syen@gmail.com';
	    result['status'] = 'FAIL';
	    showResultMsg(result);
        }
    });
}
