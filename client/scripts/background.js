﻿var VERSION = '2.9.1';

function checkForValidUrl (tabId, changeInfo, tab) {
  var regex        = /.*\:\/\/read.douban.com\/reader\/ebook\/([^\/]*).*/;
  var column_regex = /^.*\:\/\/read.douban.com\/reader\/column\/([^\/]*)\/chapter\/[0-9]*\/$/;
  if (changeInfo.status == 'complete') {
    if (regex.test(tab.url) || column_regex.test(tab.url)) {
      chrome.pageAction.show(tabId);
    }
    
  }
};

chrome.tabs.onUpdated.addListener(checkForValidUrl);

chrome.pageAction.onClicked.addListener(function (tab) {
  if (!localStorage.TO_PRIVATE_MAIL) {
    chrome.tabs.create({url: 'options.html'});
    return;
  }
  //var request_id = new Date().getTime();
  chrome.tabs.sendMessage(tab.id, {status: 'BEGIN'}, function (response) {
    // 发送数据
    send(response, function (data) {
      sendResultMessage(tab.id, data);
    });
  });
  
});

/**
 发送结果信息
 **/
function sendResultMessage (tabId, data) {
  chrome.tabs.sendMessage(tabId, data, function (response) {
  
  });
  
}

function set_icon (tab_id, icon) {
  chrome.pageAction.setIcon({
    tabId: tab_id,
    path : 'images/' + icon
  });
}

/**
 推送请求
 **/
function send (request, callback) {
  $.ajax({
    url: 'https://gk7.pw/send',
    // url     : 'http://localhost:8080/send',
    //url: 'http://192.168.1.108:8000/send',
    data    : {
      'tmplId'       : request.tmplId,
      'denum'        : request.denum,
      'bookData'     : request.bookData,
      'bookTitle'    : request.title,
      'toMail'       : localStorage.TO_PRIVATE_MAIL,// 私人邮箱 for v2.9+
      'requestId'    : request.requestId,
      'ebookId'      : request.ebookId,
      'sendType'     : request.sendType,
      'toPrivateMail': localStorage.TO_MAIL,// kindle邮箱 for v2.9+
      'version'      : VERSION
    },
    dataType: 'json',
    type    : 'POST',
    timeout : 100 * 1000// 100秒超时
  }).done(function (response) {
    callback(response);
  }).fail(function () {
    callback({status: 'FAIL', msg: '推送请求失败，请稍候再试，或联系：<a href="mailto:hyqiu.syen@gmail.com">hyqiu.syen@gmail.com</a>'});
  });
}
